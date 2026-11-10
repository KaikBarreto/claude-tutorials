// Edge function `dfe-manifestar` falsa (T14, 1.38.24). Contrato da real (supabase/functions/dfe-manifestar + RPC
// dfe_enfileirar_manifestacao): { inboundNfeId, tipo: 'ciencia'|'confirmada'|'desconhecida'|'nao_realizada', justificativa? }
//   -> 200 { ok: true, status: 'enfileirada' } · já manifestada / em andamento -> 200 ok:false com `message` (não é erro).
// Só enfileira: grava `manifestacao_pendente` na nota ("Ciência em processamento" na tela). Quem transmite à Receita é o
// worker (cron) e quem traz a nota completa é a sincronização seguinte, uma hora depois: no T14 isso acontece no "corte"
// do capítulo 12 (semente t14/corte-cap12, aplicada pelo robô).
import { erro, limpo } from './_fiscal/comum.mjs';
import { nowIso } from '../../core/util.mjs';

const ROTULO = {
  ciencia: 'Ciência da operação',
  confirmada: 'Confirmação da operação',
  desconhecida: 'Desconhecimento da operação',
  nao_realizada: 'Operação não realizada',
};

export default async function dfeManifestar(body, { db, companyId, userId }) {
  const id = limpo(body?.inboundNfeId);
  if (!id) throw erro(400, 'nota_invalida', 'Nota fiscal não informada.', { ok: false });
  const tipo = limpo(body?.tipo);
  if (!ROTULO[tipo]) throw erro(400, 'tipo_invalido', 'Tipo de manifestação inválido.', { ok: false });
  const just = limpo(body?.justificativa);
  if (tipo === 'nao_realizada' && (just.length < 15 || just.length > 255)) {
    throw erro(400, 'justificativa_invalida', 'Informe a justificativa (entre 15 e 255 caracteres) para "Operação não realizada".', { ok: false });
  }
  const nota = db.first('inbound_nfe', { id, company_id: companyId });
  if (!nota) throw erro(404, 'nota_nao_encontrada', 'Nota fiscal não encontrada.', { ok: false });
  if (nota.manifestacao === tipo) return { ok: false, status: 'ja_manifestada', message: `Esta nota já está com "${ROTULO[tipo]}" registrada na SEFAZ.` };
  if (nota.manifestacao_pendente) return { ok: false, status: 'em_andamento', message: 'Já existe uma manifestação em envio para esta nota. Aguarde a confirmação da SEFAZ.' };
  const agora = nowIso();
  db.update('inbound_nfe', (r) => r === nota, { manifestacao_pendente: tipo, manifestacao_pendente_em: agora, manifestacao_erro: null });
  db.insert('dfe_manifestacao_jobs', {
    company_id: companyId, inbound_nfe_id: nota.id, chave: nota.chave, tipo, justificativa: just || null, status: 'pendente',
    tentativas: 0, criado_por: userId || null, created_at: agora, updated_at: agora,
  }, { companyId });
  return { ok: true, status: 'enfileirada' };
}
