// Edição de pedido (T9): religa o ticket de pesagem do pedido antigo ao novo. Os pedidos da T9 não vêm de ticket: nada a religar.
export default (a, { store }) => {
  const t = store.rows('weighing_tickets').filter((w) => w.order_id === a.p_old_order_id);
  for (const w of t) w.order_id = a.p_new_order_id;
  if (t.length) store.table('weighing_tickets').touch();
  return { tickets_relinked: t.length };
};
