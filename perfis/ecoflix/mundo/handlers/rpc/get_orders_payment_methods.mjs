// Formas de pagamento de vários pedidos de uma vez (Histórico de Transações do Caixa, T9): por pedido, o total em dinheiro, no
// banco (com a conta) e no saldo do parceiro, como a função SQL (agregação de cash/bank/balance_movements).
import { pagamentosDoPedido, num, r2 } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const ids = new Set(Array.isArray(a.p_order_ids) ? a.p_order_ids : []);
  const contas = new Map(store.rows('bank_accounts').map((b) => [b.id, b]));
  const out = [];
  for (const tipo of ['purchase', 'sale']) {
    for (const p of store.rows(tipo === 'sale' ? 'sales' : 'purchases')) {
      if (!ids.has(p.id) || p.company_id !== cid) continue;
      const pg = pagamentosDoPedido(store, p, tipo);
      const b = pg.bank[0];
      const conta = b ? contas.get(b.bank_account_id) : null;
      out.push({
        order_id: p.id, order_type: tipo,
        cash_total: r2(pg.cash.reduce((s, c) => s + Math.abs(num(c.amount)), 0)),
        bank_total: r2(pg.bank.reduce((s, x) => s + Math.abs(num(x.amount)), 0)),
        balance_total: r2(pg.bal.reduce((s, x) => s + Math.abs(num(x.amount)), 0)),
        bank_account_id: conta?.id || null, bank_account_name: conta?.name || null, bank_account_color: conta?.color || null,
        bank_balance_after: b ? (b.balance_after ?? null) : null,
      });
    }
  }
  return out;
};
