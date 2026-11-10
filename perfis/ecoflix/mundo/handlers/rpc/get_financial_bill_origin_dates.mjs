// Data de origem de cada conta a pagar/receber: a nota fiscal (se houver), senão o pedido, senão a criação do título.
import { diaBR } from '../../lib/eco.mjs';
export default (a, { store }) => {
  const ids = new Set(a.p_bill_ids || []);
  const pedido = (t, id) => store.rows(t === 'sale' ? 'sales' : 'purchases').find((p) => p.id === id);
  return store.rows('financial_bills').filter((b) => ids.has(b.id)).map((b) => {
    const p = b.order_id ? pedido(b.order_type, b.order_id) : null;
    if (p) return { bill_id: b.id, issue_date: p.transaction_date || diaBR(p.transaction_at || p.created_at), date_source: 'order' };
    return { bill_id: b.id, issue_date: diaBR(b.created_at), date_source: 'bill' };
  });
};
