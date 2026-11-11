// Edge plugnotas-manifestar (Notas Recebidas, grupo "Manifestar"): confirmação (sem justificativa), desconhecimento e operação não
// realizada (justificativa >= 15). Sem fila: grava a manifestação na hora e responde { success: true, queued: false } (o app mostra
// "Operação confirmada junto à SEFAZ").
import { agoraIso } from '../../lib/nfe.mjs';

const TIPOS = { confirmacao: 'confirmada', confirmar: 'confirmada', confirmada: 'confirmada', desconhecimento: 'desconhecida',
  desconhecer: 'desconhecida', desconhecida: 'desconhecida', nao_realizada: 'nao_realizada', operacao_nao_realizada: 'nao_realizada',
  ciencia: 'ciencia' };

export default (body, { db, FunctionError }) => {
  const nota = db.first('inbound_nfe', { chave: body?.chave });
  if (!nota) throw new FunctionError('Nota não encontrada', 404, { success: false, error: 'Nota não encontrada' });
  const m = TIPOS[String(body?.tipo || '').toLowerCase()];
  if (!m) return { success: false, error: 'Tipo de manifestação inválido' };
  if (['desconhecida', 'nao_realizada'].includes(m) && String(body?.justificativa || '').trim().length < 15) {
    return { success: false, error: 'A justificativa precisa de pelo menos 15 caracteres' };
  }
  db.update('inbound_nfe', { id: nota.id }, { manifestacao: m, manifestacao_data: agoraIso(), manifestacao_pendente: null,
    manifestacao_pendente_em: null, manifestacao_erro: null });
  return { success: true, queued: false };
};
