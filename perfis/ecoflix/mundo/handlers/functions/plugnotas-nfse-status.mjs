// Consulta da NFS-e na prefeitura simulada (T17 cap07; supabase/functions/plugnotas-nfse-status): na 1ª consulta a nota
// "processando" é autorizada ("emitida": número oficial, código de verificação, authorized_at).
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (body, { db, url, FunctionError }) => {
  const n = db.first('nfse_invoices', { id: body?.nfseInvoiceId });
  if (!n) throw new FunctionError('NFS-e não encontrada', 404, { success: false });
  if (n.status !== 'processando') return { success: true, status: n.status, statusChanged: false };
  const agora = nowIso();
  // a função real guarda o PDF da prefeitura no Storage (nfe-danfes) e grava o endereço em pdf_url: é o que acende "Baixar PDF" no menu
  const origem = (() => { try { return new URL(url).origin; } catch { return ''; } })();
  db.update('nfse_invoices', { id: n.id }, { status: 'emitida', nfse_numero_oficial: String(n.nfse_number), authorized_at: agora,
    codigo_verificacao: `RV${String(100000 + Number(n.nfse_number) * 6311).slice(-6)}`, error_message: null, updated_at: agora,
    pdf_url: `${origem}/storage/v1/object/public/nfe-danfes/${n.company_id}/nfse/NFSe-${n.nfse_number}.pdf` });
  return { success: true, status: 'emitida', statusChanged: true };
};
