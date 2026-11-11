// Consulta da NFS-e na prefeitura simulada (T17 cap07; supabase/functions/plugnotas-nfse-status): na 1ª consulta a nota
// "processando" é autorizada ("emitida": número oficial, código de verificação, authorized_at).
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (body, { db, FunctionError }) => {
  const n = db.first('nfse_invoices', { id: body?.nfseInvoiceId });
  if (!n) throw new FunctionError('NFS-e não encontrada', 404, { success: false });
  if (n.status !== 'processando') return { success: true, status: n.status, statusChanged: false };
  const agora = nowIso();
  db.update('nfse_invoices', { id: n.id }, { status: 'emitida', nfse_numero_oficial: String(n.nfse_number), authorized_at: agora,
    codigo_verificacao: `RV${String(100000 + Number(n.nfse_number) * 6311).slice(-6)}`, error_message: null, updated_at: agora });
  return { success: true, status: 'emitida', statusChanged: true };
};
