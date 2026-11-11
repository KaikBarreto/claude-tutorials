// Edge plugnotas-emit (hooks/usePlugNotas.tsx, emitInvoice): reserva o número da série (o próximo de get_next_invoice_number), marca a
// nota "aguardando_sefaz" com o id do provedor e devolve { success, plugnotasId }. A autorização chega pela consulta de status
// (plugnotas-status), ~4 s depois, como o retorno assíncrono da SEFAZ. Sem SEFAZ, sem provedor, sem cota real.
import { configFiscal, proximoNumero, avancaSerie, agoraIso } from '../../lib/nfe.mjs';

export default (body, { store, db, FunctionError }) => {
  const n = db.first('invoices', { id: body?.invoiceId });
  if (!n) throw new FunctionError('Nota fiscal não encontrada', 404, { success: false, error: 'Nota fiscal não encontrada' });
  const cfg = (n.fiscal_config_id && db.first('company_fiscal_config', { id: n.fiscal_config_id })) || configFiscal(store, n.company_id);
  if (!cfg?.plugnotas_certificate_uploaded || !cfg?.plugnotas_company_registered) {
    return { success: false, error: 'Empresa não habilitada para emitir NF-e. Conclua a Configuração Fiscal.' };
  }
  if (['emitida', 'cancelada', 'inutilizada'].includes(n.status)) return { success: false, error: 'Esta nota já foi processada' };
  const serie = Number(n.serie) || 1;
  const numero = n.invoice_number ?? proximoNumero(store, n.company_id, serie, cfg.id);
  const pid = `pn-${String(numero).padStart(6, '0')}`;
  db.update('invoices', { id: n.id }, {
    invoice_number: numero, serie, modelo: n.modelo || 55, fiscal_config_id: cfg.id, issue_date: n.issue_date || agoraIso(),
    plugnotas_id: pid, status: 'aguardando_sefaz', environment: 'producao', error_message: null,
  });
  avancaSerie(db, store, n.company_id, cfg.id, serie, numero);
  db.update('company_fiscal_config', { id: cfg.id }, { last_invoice_number: numero, last_invoice_serie: String(serie) });
  return { success: true, plugnotasId: pid, protocol: null, message: 'Nota fiscal enviada para processamento na SEFAZ' };
};
