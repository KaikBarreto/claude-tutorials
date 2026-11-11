// Encerramento do MDF-e (T17 cap05; supabase/functions/plugnotas-mdfe-enclose): o pedido vai para a SEFAZ simulada e o
// manifesto fica "encerramento_pendente" (enclosed_at nulo: só a confirmação grava); a consulta seguinte (plugnotas-mdfe-status)
// confirma. A mensagem é a da função real para o pedido ainda não confirmado (_shared/mdfe-event.ts).
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (body, { db, FunctionError }) => {
  const m = db.first('mdfe_manifests', { id: body?.mdfeId });
  if (!m) throw new FunctionError('MDF-e não encontrado', 404, { success: false });
  if (m.status === 'encerrado') return { success: true, status: 'encerrado', confirmed: true, message: 'MDF-e já está encerrado.' };
  if (m.status !== 'autorizado') return { success: false, error: 'Apenas MDF-e autorizados podem ser encerrados' };
  db.update('mdfe_manifests', { id: m.id }, { status: 'encerramento_pendente', enclosed_at: null, error_message: null, updated_at: nowIso() });
  db.insert('nfe_events', { invoice_id: null, company_id: m.company_id, event_type: 'mdfe_encerramento', status: 'encerramento_pendente',
    message: `MDF-e #${m.mdfe_number}: encerramento enviado, aguardando confirmação da SEFAZ`, plugnotas_response: { message: 'Evento em processamento' }, created_at: nowIso() });
  return { success: true, status: 'encerramento_pendente', confirmed: false, outcome: 'pendente',
    message: 'Encerramento enviado. Aguardando confirmação da SEFAZ — o status é atualizado automaticamente.' };
};
