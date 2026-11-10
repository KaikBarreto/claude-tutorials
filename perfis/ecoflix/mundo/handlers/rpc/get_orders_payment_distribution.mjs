// Formas de pagamento dos pedidos do período (dinheiro, banco, saldo), uma linha por tipo de pedido.
import { janela, pedidos, pagamentosDoPedido, num, r2 } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const j = janela(a.p_start_date, a.p_end_date);
  const filtro = (ids) => (Array.isArray(ids) && ids.length ? new Set(ids) : null);
  const fs = filtro(a.p_supplier_ids), fc = filtro(a.p_customer_ids), fu = filtro(a.p_creator_ids);
  const linhas = [];
  for (const tipo of ['purchase', 'sale']) {
    const lista = pedidos(store, cid, tipo, j).filter((p) => (!fu || fu.has(p.created_by)) && (tipo === 'purchase' ? !fs || fs.has(p.supplier_id) : !fc || fc.has(p.customer_id)));
    if (!lista.length) continue;
    let cash = 0, bank = 0, bal = 0, tot = 0;
    for (const p of lista) {
      const pg = pagamentosDoPedido(store, p, tipo);
      cash += pg.cash.reduce((s, c) => s + num(c.amount), 0);
      bank += pg.bank.reduce((s, b) => s + Math.abs(num(b.amount)), 0);
      bal += pg.bal.reduce((s, b) => s + Math.abs(num(b.amount)), 0);
      tot += num(p.total_amount);
    }
    const by = (v) => (v ? [{ currency: 'BRL', total: r2(v) }] : []);
    linhas.push({
      order_type: tipo, cash_total: r2(cash), bank_total: r2(bank), balance_total: r2(bal), orders_total: r2(tot), orders_count: lista.length,
      currency: 'BRL', cash_by_currency: by(cash), bank_by_currency: by(bank), balance_by_currency: by(bal), orders_by_currency: [{ currency: 'BRL', total: r2(tot), count: lista.length }],
    });
  }
  return linhas;
};
