// get_clients_suppliers_inactive_count(p_company_id, p_start_date, p_end_date): "<n> clientes sem venda / fornecedores sem compra no
// período" da Visão geral de Clientes e Fornecedores (EntitiesSummaryTab.tsx; T4 cap01). Datas AAAA-MM-DD, inclusive.
import { pedidos } from '../../lib/eco.mjs';

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const j = { d1: a.p_start_date ? String(a.p_start_date).slice(0, 10) : '0000-01-01', d2: a.p_end_date ? String(a.p_end_date).slice(0, 10) : '9999-12-31' };
  const comVenda = new Set(pedidos(store, cid, 'sale', j).map((p) => p.customer_id));
  const comCompra = new Set(pedidos(store, cid, 'purchase', j).map((p) => p.supplier_id));
  const inativos = (tab, set) => store.rows(tab).filter((x) => x.company_id === cid && !set.has(x.id)).length;
  return [{ inactive_customers: inativos('customers', comVenda), inactive_suppliers: inativos('suppliers', comCompra) }];
};
