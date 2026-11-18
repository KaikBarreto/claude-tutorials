// get_cash_register_other_order_ids(p_company_id, p_cash_register_id, p_created_since) — app 1.60.10, migration
// 20261113230300_cash_register_other_order_candidates.sql. A tela do Caixa (pages/Caixa.tsx:969-989) só liga "Total Comprado",
// "Total Vendido" e os cartões por forma de pagamento do "Fechar Caixa" depois que esta RPC responde: ela devolve os pedidos
// (compras e vendas, criados a partir de p_created_since) que têm lançamento de dinheiro em OUTRO caixa que não o pedido, para a tela
// não somar no caixa aberto o pedido que passou pela gaveta de outro operador. Como a função SQL: TABLE(order_id), em ordem de id;
// caixa de outra empresa ou inexistente dá erro. Com um caixa só no dia sai [] (T03, T06 até o #86, T07); com o #85 e o #86 abertos
// saem os pedidos pagos no outro.
export default (a, { store, companyId, RpcError }) => {
  const cid = a.p_company_id || companyId;
  const cx = store.rows('cash_register').find((r) => r.id === a.p_cash_register_id && r.company_id === cid);
  if (!cx) throw new RpcError('Cash register not found');
  const desde = a.p_created_since ? Date.parse(a.p_created_since) : null;
  const candidatos = new Set();
  for (const t of ['purchases', 'sales']) {
    for (const p of store.rows(t)) {
      if (p.company_id !== cid) continue;
      if (desde !== null && !(Date.parse(p.created_at) >= desde)) continue;
      candidatos.add(p.id);
    }
  }
  const emOutro = new Set();
  for (const ct of store.rows('cash_transactions')) {
    if (ct.company_id === cid && ct.order_id && ct.cash_register_id && ct.cash_register_id !== cx.id && candidatos.has(ct.order_id)) emOutro.add(ct.order_id);
  }
  return [...emOutro].sort().map((order_id) => ({ order_id }));
};
