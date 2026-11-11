// RPC search_orders_for_invoice (ImportarPedidoModal, "Importar de Pedido de Venda/Compra"): pedidos concluídos SEM NF-e ligada (nem por
// invoice_orders nem por invoices.order_id, contando só nota não cancelada), do mais recente para o mais antigo; busca por número,
// referência ou parceiro; período inclusivo. Cada linha leva o total da busca (total_count), para a paginação.
const semAcento = (s) => String(s ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const venda = a.p_order_type !== 'purchase';
  const tab = venda ? 'sales' : 'purchases';
  const parc = venda ? 'customers' : 'suppliers';
  const pid = venda ? 'customer_id' : 'supplier_id';
  const vivas = new Set(store.rows('invoices').filter((n) => n.company_id === cid && !['cancelada', 'inutilizada'].includes(n.status) && !n.archived_at).map((n) => n.id));
  const comNota = new Set(store.rows('invoice_orders').filter((l) => vivas.has(l.invoice_id)).map((l) => l.order_id));
  for (const n of store.rows('invoices')) if (vivas.has(n.id) && n.order_id) comNota.add(n.order_id);
  const q = semAcento(a.p_query || '').replace(/^#/, '');
  let rows = store.rows(tab).filter((p) => p.company_id === cid && !p.deleted_at && (p.status ?? 'completed') !== 'cancelled' && !comNota.has(p.id))
    .map((p) => {
      const pr = p[pid] && store.rows(parc).find((x) => x.id === p[pid]);
      return { id: p.id, order_number: p.order_number, order_ref: p.order_ref ?? null, order_date: p.transaction_at || p.created_at,
        total_amount: Number(p.total_amount) || 0, partner_id: p[pid] ?? null, partner_name: pr?.name ?? null, payment_method: p.payment_method ?? null };
    });
  if (q) rows = rows.filter((r) => String(r.order_number).includes(q) || semAcento(r.order_ref).includes(q) || semAcento(r.partner_name).includes(q));
  if (a.p_date_from) rows = rows.filter((r) => String(r.order_date) >= String(a.p_date_from));
  if (a.p_date_to) rows = rows.filter((r) => String(r.order_date) <= String(a.p_date_to));
  rows.sort((x, y) => String(y.order_date).localeCompare(String(x.order_date)));
  const total = rows.length;
  const lim = Math.min(200, Number(a.p_limit) || 20);
  return rows.slice(Number(a.p_offset) || 0, (Number(a.p_offset) || 0) + lim).map((r) => ({ ...r, total_count: total }));
};
