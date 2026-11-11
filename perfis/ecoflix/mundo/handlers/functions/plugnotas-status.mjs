// Edge plugnotas-status (polling da lista de NF-e a cada 5 s, NotasFiscais.tsx): a nota "aguardando_sefaz" há >= 3,5 s volta autorizada,
// com chave de 44 dígitos, protocolo de 15, authorized_at, a prova oficial (fiscal_status_confirmation) e o XML autorizado
// (invoices.xml_content, a aba XML do Visualizar). Resposta no formato da edge real.
import { configFiscal, chaveNfe, protocolo, xmlNfe, prova, agoraIso } from '../../lib/nfe.mjs';
import { agoraMs } from '../../lib/eco.mjs';

export default (body, { store, db, FunctionError }) => {
  const n = db.first('invoices', { id: body?.invoiceId });
  if (!n) throw new FunctionError('Nota fiscal não encontrada', 404, { success: false, error: 'Nota fiscal não encontrada' });
  const antes = n.status;
  if (['aguardando_sefaz', 'processando'].includes(antes) && agoraMs() - Date.parse(n.updated_at || n.created_at) >= 3500) {
    const cfg = (n.fiscal_config_id && db.first('company_fiscal_config', { id: n.fiscal_config_id })) || configFiscal(store, n.company_id) || {};
    const key = n.nfe_key || chaveNfe(cfg.cnpj || '47318506000107', n.invoice_number, n.serie || 1, n.issue_date || agoraIso());
    const prot = n.nfe_protocol || protocolo(key);
    db.update('invoices', { id: n.id }, {
      status: 'emitida', nfe_key: key, nfe_protocol: prot, authorized_at: agoraIso(), error_message: null,
      fiscal_status_confirmation: prova('authorized', key, prot, '100'),
    });
    db.update('invoices', { id: n.id }, { xml_content: xmlNfe(store, db.first('invoices', { id: n.id })) });
  }
  const m = db.first('invoices', { id: n.id });
  return {
    success: true, status: m.status, fiscalStatusConfirmation: m.fiscal_status_confirmation ?? null, environment: m.environment,
    statusChanged: m.status !== antes, previousStatus: antes, nfeKey: m.nfe_key ?? null, nfeProtocol: m.nfe_protocol ?? null,
    errorMessage: null, cancellationRejected: false, cancellationPending: m.status === 'cancelamento_pendente',
    hasXml: !!m.xml_content, hasPdf: !!m.danfe_storage_path,
  };
};
