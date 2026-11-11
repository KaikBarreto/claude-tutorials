// Edge plugnotas-cancel (CancelarNotaDialog): cancela a NF-e autorizada dentro do prazo, grava motivo, cancelled_at e a prova oficial
// "cancelled" (sem ela o selo viraria "Conferir status na SEFAZ") e responde { success, status: 'cancelada', confirmed: true }.
import { protocolo, prova, agoraIso } from '../../lib/nfe.mjs';

export default (body, { db, FunctionError }) => {
  const n = db.first('invoices', { id: body?.invoiceId });
  if (!n) throw new FunctionError('Nota fiscal não encontrada', 404, { success: false, error: 'Nota fiscal não encontrada' });
  const motivo = String(body?.motivo || '').trim();
  if (motivo.length < 15) return { success: false, error: 'O motivo do cancelamento precisa de pelo menos 15 caracteres' };
  if (n.status !== 'emitida') return { success: false, error: 'Só nota autorizada pode ser cancelada' };
  const prot = protocolo(`canc-${n.nfe_key}`);
  db.update('invoices', { id: n.id }, {
    status: 'cancelada', cancelled_at: agoraIso(), cancellation_reason: motivo, cancellation_protocol: prot,
    fiscal_status_confirmation: prova('cancelled', n.nfe_key, prot, '135'),
  });
  db.insert('nfe_events', { company_id: n.company_id, invoice_id: n.id, event_type: 'cancelamento', status: 'success',
    message: motivo, payload: { protocolo: prot } });
  return { success: true, status: 'cancelada', confirmed: true, protocol: prot, message: 'Nota fiscal cancelada' };
};
