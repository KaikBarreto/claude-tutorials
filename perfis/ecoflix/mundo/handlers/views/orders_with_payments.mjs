// VIEW orders_with_payments (T10, 20/11/2026, app 1.60.18): o Kardex abre a linha de compra/venda lendo
// total_amount, cash_payments, bank_payments, balance_payments, payment_method, partner_name e currency (pages/MaterialHistory.tsx:442-450).
// Uma linha por compra e por venda, com os pagamentos de pagamentosDoPedido (dinheiro, banco, saldo) como listas de {amount}.
import { pagamentosDoPedido } from '../../lib/eco.mjs';

export default function ordersWithPayments(store) {
  const sup = new Map(store.rows('suppliers').map((s) => [s.id, s]));
  const cus = new Map(store.rows('customers').map((c) => [c.id, c]));
  const out = [];
  for (const [tabela, tipo] of [['purchases', 'purchase'], ['sales', 'sale']]) {
    for (const p of store.rows(tabela)) {
      const { cash, bank, bal } = pagamentosDoPedido(store, p, tipo);
      const parte = tipo === 'sale' ? cus.get(p.customer_id) : sup.get(p.supplier_id);
      const metodo = bank.length ? 'bank' : cash.length ? 'cash' : bal.length ? 'balance' : (p.payment_method ?? null);
      out.push({
        ...p,
        order_type: tipo,
        partner_name: parte?.name ?? null,
        currency: p.currency ?? 'BRL',
        payment_method: metodo,
        cash_payments: cash.map((c) => ({ amount: Number(c.amount) || 0 })),
        bank_payments: bank.map((b) => ({ amount: Math.abs(Number(b.amount) || 0) })),
        balance_payments: bal.map((b) => ({ amount: Math.abs(Number(b.amount) || 0) })),
      });
    }
  }
  return out;
}
