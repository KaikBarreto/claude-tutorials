// Totais dos tickets de pesagem valorizados no período (os pendentes não somam).
import { num, r2 } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const ini = a.p_start ? new Date(a.p_start).getTime() : -Infinity, fim = a.p_end ? new Date(a.p_end).getTime() : Infinity;
  const tipos = Array.isArray(a.p_types) && a.p_types.length ? a.p_types : null;
  const lst = store.rows('weighing_tickets').filter((t) => t.company_id === cid && !t.deleted_at && t.status === 'valorized' && (!tipos || tipos.includes(t.type))
    && new Date(t.created_at).getTime() >= ini && new Date(t.created_at).getTime() <= fim);
  let total = 0;
  for (const t of lst) {
    const o = t.valorized_order_id && (store.rows('purchases').find((p) => p.id === t.valorized_order_id) || store.rows('sales').find((p) => p.id === t.valorized_order_id));
    total += num(o?.total_amount);
  }
  return [{ valorized_count: lst.length, valorized_total: r2(total) }];
};
