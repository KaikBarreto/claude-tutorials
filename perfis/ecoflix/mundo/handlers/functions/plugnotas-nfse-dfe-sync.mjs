// Sincronização das NFS-e recebidas (T17 cap08; supabase/functions/plugnotas-nfse-dfe-sync): o ambiente nacional simulado devolve
// as duas notas de serviço emitidas contra o CNPJ da Recicla Vale (tomador), que ainda não estão na base: os honorários de outubro
// da Contabilidade Manacá Ltda (R$ 1.650,00) e a aferição da balança rodoviária da Balanças Tremembé Manutenção Ltda (R$ 980,00).
// Nenhum dos dois é fornecedor cadastrado. Só com o recurso ligado (como a função real).
import { nowIso } from '../../../fakebase/core/util.mjs';

const dv11 = (s) => { let t = 0; let w = 2; for (let i = s.length - 1; i >= 0; i--) { t += Number(s[i]) * w; w = w === 9 ? 2 : w + 1; } const r = t % 11; return r < 2 ? 0 : 11 - r; };
const chave = (ibge, cnpj, num, aamm, cnum) => { const b = `${ibge}21${cnpj}${String(num).padStart(13, '0')}${aamm}${String(cnum).padStart(9, '0')}`; return b + dv11(b); };

const NOTAS = [
  { numero: '318', prestador_nome: 'Contabilidade Manacá Ltda', prestador_documento: '47291836000156', prestador_municipio_ibge: '3554102',
    prestador_im: '38.214', data_emissao: '2026-11-05T13:40:00.000Z', competencia: '2026-10-01', valor_servico: 1650, valor_iss: 33,
    codigo_tributacao_nacional: '171901', discriminacao: 'Honorários contábeis de outubro de 2026', nsu: '1022', cnum: 318204 },
  { numero: '1207', prestador_nome: 'Balanças Tremembé Manutenção Ltda', prestador_documento: '39506417000166', prestador_municipio_ibge: '3554805',
    prestador_im: '9.471', data_emissao: '2026-11-07T14:15:00.000Z', competencia: '2026-11-01', valor_servico: 980, valor_iss: 29.4,
    codigo_tributacao_nacional: '140101', discriminacao: 'Aferição e manutenção preventiva da balança rodoviária', nsu: '1023', cnum: 120779 },
];

export default (body, { db, companyId }) => {
  const cid = body?.companyId || companyId;
  const cfg = (body?.fiscalConfigId && db.first('company_fiscal_config', { id: body.fiscalConfigId, company_id: cid }))
    || db.first('company_fiscal_config', (c) => c.company_id === cid && c.is_default) || db.first('company_fiscal_config', { company_id: cid });
  if (!cfg || !cfg.nfse_dfe_ativo) return { synced: 0, error: 'Ative as NFS-e Recebidas antes de sincronizar.' };
  const cnpj = String(cfg.cnpj).replace(/\D/g, '');
  let n = 0;
  for (const x of NOTAS) {
    const ch = chave(x.prestador_municipio_ibge, x.prestador_documento, x.numero, `${x.data_emissao.slice(2, 4)}${x.data_emissao.slice(5, 7)}`, x.cnum);
    if (db.first('inbound_nfse', { company_id: cid, chave_acesso: ch })) continue;
    const { cnum, ...linha } = x;
    db.insert('inbound_nfse', { ...linha, company_id: cid, fiscal_config_id: cfg.id, chave_acesso: ch, chave_natural: ch, serie: '1',
      tomador_documento: cnpj, tomador_nome: cfg.razao_social, municipio_incidencia_ibge: x.prestador_municipio_ibge, iss_retido: false,
      valor_liquido: x.valor_servico, situacao: 'autorizada', fonte: 'plugnotas', fonte_ref: `pn-dfe-${x.nsu}`, resumo: false,
      created_at: nowIso(), updated_at: nowIso() }, { companyId: cid });
    n++;
  }
  db.update('company_fiscal_config', { id: cfg.id }, { nfse_dfe_last_sync_at: nowIso(), nfse_dfe_ultimo_erro: null });
  return { synced: n, ignoradas: 0, detalhesPreenchidos: n, janelas: 1, cursor: null };
};
