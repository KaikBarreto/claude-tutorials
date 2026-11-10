// Edge function `dfe-sync` falsa (T14, 1.38.24). Contrato da real (supabase/functions/dfe-sync + _shared/dfe-sync-core.ts):
//   { tipo: 'nfe' | 'nfse' } -> { ok, motivo, novas, total, parcial, aviso? } (+ `message` = aviso quando o HTTP não é 200)
//   - sem config fiscal -> 422 sem_config · recebimento desligado -> 200 ok:false desativado · sem A1 -> 422 sem_certificado;
//   - TRAVA DA SEFAZ: uma consulta por CNPJ a cada 65 min (`dfe_sync_claim` com ESPERA_CHEIA_MIN): dentro da janela,
//     200 ok:false em_espera "A SEFAZ permite uma consulta por hora para cada CNPJ...";
//   - rodada: entrega os documentos com NSU acima do último lido, grava inbound_nfe (resNFe = só o resumo; procNFe completa a
//     nota da mesma chave), atualiza dfe_sync_state (próxima consulta = agora + 65 min) e registra a decifra
//     "dfe_distribuicao" na trilha do certificado. Sem nota nova: aviso "Nenhuma nota nova foi encontrada.".
// Os documentos que a "Receita" tem para o CNPJ vêm da tabela de semente `fake_sefaz_dfe` (o app não a lê):
//   { company_id, tipo, nsu (15 dígitos), requer_ciencia?, nota: { colunas de inbound_nfe } }
// Documento com `requer_ciencia` (a nota completa) só sai depois da ciência registrada na nota de mesma chave.
import { erro, fiscalDe, custodiaCompleta, certificadoValido, decifrar } from './_fiscal/comum.mjs';
import { now, nowIso } from '../../core/util.mjs';

export const ESPERA_CHEIA_MIN = 65;

function resposta(status, corpo) {
  if (status === 200) return corpo;
  throw erro(status, corpo.motivo, corpo.aviso, { ok: false, motivo: corpo.motivo, novas: 0, total: 0, parcial: false, aviso: corpo.aviso });
}

export default async function dfeSync(body, { db, companyId }) {
  const tipo = body?.tipo === 'nfse' ? 'nfse' : body?.tipo === 'nfe' ? 'nfe' : null;
  if (!tipo) throw erro(400, 'tipo_invalido', 'Tipo de nota inválido.', { ok: false });
  const fiscal = fiscalDe(db, companyId);
  const vazio = { novas: 0, total: 0, parcial: false };
  if (!fiscal) return resposta(422, { ok: false, motivo: 'sem_config', ...vazio, aviso: 'Configure os dados fiscais da empresa antes de buscar notas recebidas.' });
  const ativo = tipo === 'nfe' ? fiscal.dfe_nfe_ativo : fiscal.dfe_nfse_ativo;
  if (ativo !== true) {
    return {
      ok: false, motivo: 'desativado', ...vazio,
      aviso: tipo === 'nfe'
        ? 'A busca automática de notas recebidas está desligada. Ative nas configurações fiscais.'
        : 'A busca automática de notas de serviço recebidas está desligada. Ative nas configurações fiscais.',
    };
  }
  if (!custodiaCompleta(fiscal) || !certificadoValido(fiscal)) {
    return resposta(422, { ok: false, motivo: 'sem_certificado', ...vazio, aviso: 'Envie o certificado digital A1 da empresa nas configurações fiscais. Sem ele a SEFAZ não entrega as notas recebidas.' });
  }

  // ---- claim da rodada (janela de 65 min por CNPJ)
  const agora = now().getTime();
  let st = db.first('dfe_sync_state', { company_id: companyId, tipo });
  if (st?.proxima_consulta_em && Date.parse(st.proxima_consulta_em) > agora) {
    return { ok: false, motivo: 'em_espera', ...vazio, aviso: 'A SEFAZ permite uma consulta por hora para cada CNPJ. A próxima busca acontece automaticamente.' };
  }
  if (!st) st = db.insert('dfe_sync_state', { company_id: companyId, tipo, ultimo_nsu: '000000000000000', ciclos_sem_documento: 0 }, { companyId });

  // ---- distribuição
  decifrar(db, companyId, fiscal, tipo === 'nfe' ? 'dfe_distribuicao' : 'dfe_nfse_distribuicao');
  const tabela = tipo === 'nfe' ? 'inbound_nfe' : 'inbound_nfse';
  const chaveCol = tipo === 'nfe' ? 'chave' : 'chave_natural';
  const ultimo = String(st.ultimo_nsu || '0').padStart(15, '0');
  const todos = db.find('fake_sefaz_dfe', { company_id: companyId, tipo }).sort((a, b) => String(a.nsu).localeCompare(String(b.nsu)));
  const lote = todos.filter((d) => String(d.nsu).padStart(15, '0') > ultimo).filter((d) => {
    if (!d.requer_ciencia) return true;
    const n = db.first(tabela, { company_id: companyId, [chaveCol]: d.nota?.[chaveCol] });
    return n && ['ciencia', 'confirmada'].includes(n.manifestacao);
  });
  let novas = 0;
  for (const d of lote) {
    const existente = db.first(tabela, { company_id: companyId, [chaveCol]: d.nota?.[chaveCol] });
    if (existente) db.update(tabela, (r) => r === existente, { ...d.nota, updated_at: nowIso() });
    else {
      db.insert(tabela, { manifestacao: 'nenhuma', origem: 'distribuicao', ...d.nota, company_id: companyId, nsu: d.nsu }, { companyId });
      novas += 1;
    }
  }
  const lidoAte = lote.length ? String(lote[lote.length - 1].nsu) : st.ultimo_nsu;
  const maxNsu = todos.length ? String(todos[todos.length - 1].nsu) : st.max_nsu ?? lidoAte;
  db.update('dfe_sync_state', (r) => r === st, {
    ultimo_nsu: lidoAte, max_nsu: maxNsu, ultima_consulta_em: nowIso(), proxima_consulta_em: new Date(agora + ESPERA_CHEIA_MIN * 60000).toISOString(),
    ultimo_cstat: lote.length ? '138' : '137', ultimo_erro: null, documentos_ultimo_lote: lote.length,
    ciclos_sem_documento: lote.length ? 0 : Number(st.ciclos_sem_documento || 0) + 1, janela_fim: new Date(agora + ESPERA_CHEIA_MIN * 60000).toISOString(),
  });
  const out = { ok: true, motivo: 'sincronizado', novas, total: lote.length, parcial: false };
  if (novas === 0) out.aviso = tipo === 'nfe' ? 'Nenhuma nota nova foi encontrada.' : 'Nenhuma nota de serviço nova foi encontrada.';
  return out;
}
