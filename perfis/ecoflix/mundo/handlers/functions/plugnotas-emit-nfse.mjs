// Emissão da NFS-e (T17 cap07; supabase/functions/plugnotas-emit-nfse): a nota recebe o próximo número da série (a 14 depois das
// 12 e 13 de outubro), vai para "processando" com o plugnotas_id e o protocolo; a autorização chega pela consulta
// (plugnotas-nfse-status, a cada 8 s depois de emitir). Prefeitura simulada: nada sai para fora.
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (body, { db, FunctionError }) => {
  const n = db.first('nfse_invoices', { id: body?.nfseInvoiceId });
  if (!n) throw new FunctionError('NFS-e não encontrada', 404, { success: false });
  if (['emitida', 'processando'].includes(n.status)) return { success: true, status: n.status, nfseNumber: n.nfse_number };
  const serie = Number(n.serie) || 1;
  const numero = n.nfse_number || 1 + Math.max(0, ...db.find('nfse_invoices', (r) => r.company_id === n.company_id && Number(r.serie || 1) === serie).map((r) => Number(r.nfse_number) || 0));
  const plugnotasId = `pn-nfse-${String(numero).padStart(6, '0')}`;
  db.update('nfse_invoices', { id: n.id }, { status: 'processando', nfse_number: numero, serie, id_integracao: n.id_integracao || `rv-nfse-${numero}`,
    plugnotas_id: plugnotasId, protocol: `NFSE${String(numero).padStart(10, '0')}`, environment: 'producao', issue_date: n.issue_date || nowIso(),
    error_message: null, updated_at: nowIso() });
  return { success: true, status: 'processando', nfseNumber: numero, plugnotasId };
};
