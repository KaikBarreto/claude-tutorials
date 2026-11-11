// RPC dfe_inbound_import_enqueue (ImportInboundNfeDialog, "Importar nota" pela chave ou pelo XML): põe o pedido na fila
// dfe_inbound_import_jobs. A fila "anda" na leitura (handlers/views/dfe_inbound_import_jobs.mjs): queued, processing e, ~3 s depois,
// succeeded com a nota em inbound_nfe.
import { configFiscal, agoraIso } from '../../lib/nfe.mjs';

export default (a, { store, db, companyId, RpcError }) => {
  const cfg = configFiscal(store, companyId, a.p_fiscal_config_id);
  if (!cfg) throw new RpcError('Configuração fiscal não encontrada', 'P0002', 404);
  const kind = a.p_kind === 'xml' ? 'xml' : 'access_key';
  const xml = kind === 'xml' ? String(a.p_xml_content || '') : null;
  const chave = kind === 'xml' ? ((xml.match(/Id="NFe(\d{44})"/) || xml.match(/<chNFe>(\d{44})<\/chNFe>/) || [])[1] || null) : String(a.p_access_key || '').replace(/\D/g, '');
  if (!chave || chave.length !== 44) throw new RpcError('Chave de acesso inválida', '22023', 400);
  const agora = agoraIso();
  const job = db.insert('dfe_inbound_import_jobs', {
    company_id: cfg.company_id, fiscal_config_id: cfg.id, kind, access_key: chave, status: 'queued', attempts: 0, available_at: agora,
    inbound_nfe_id: null, error_code: null, error_message: null, xml_content: xml, created_at: agora, updated_at: agora,
  }, { companyId: cfg.company_id });
  return { id: job.id, kind, status: 'queued', access_key: chave, available_at: agora, created_at: agora };
};
