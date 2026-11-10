// RPC sync_service_order_service_types(p_service_order_id, p_service_type_ids) · 20261018231000_orcamento_da_os_e_gerar_os.sql:292-373
// Regrava os tipos de serviço da OS (só tipos ativos da empresa, no máximo 50) e copia o 1º para service_orders.service_type_id
// (por isso o "Tipo" do cartão, a cor e o prefixo do código seguem o primeiro tipo escolhido).
import { RpcError } from '../../http/rest.mjs';

export default async function syncServiceOrderServiceTypes({ p_service_order_id, p_service_type_ids }, { db, companyId }) {
  const ids = Array.isArray(p_service_type_ids) ? p_service_type_ids.map(String) : [];
  if (ids.length > 50) throw new RpcError('Uma OS aceita no máximo 50 tipos de serviço.');
  const os = db.first('service_orders', { id: p_service_order_id });
  if (!os) throw new RpcError('Ordem de serviço não encontrada ou sem permissão.');
  for (const id of ids) {
    const st = db.first('service_types', { id });
    if (!st || st.company_id !== os.company_id || st.is_active === false) {
      throw new RpcError('Um dos tipos de serviço não pertence a esta empresa ou está inativo.');
    }
  }
  db.remove('service_order_service_types', { service_order_id: p_service_order_id });
  const seen = new Set();
  ids.forEach((id, position) => {
    if (seen.has(id)) return;
    seen.add(id);
    db.insert('service_order_service_types', { service_order_id: p_service_order_id, service_type_id: id, company_id: os.company_id || companyId, position });
  });
  db.update('service_orders', { id: p_service_order_id }, { service_type_id: ids[0] ?? null });
  return { service_order_id: p_service_order_id, service_type_ids: ids };
}
