// RPC pay_credit_card_bill(p_bill_id, p_payment_account_id, p_payment_date, p_amount, p_notes) → jsonb
// 20260912130000_dre_caixa_pagamento_parcial_de_fatura.sql (T13, cap. 9). Pagar fatura é operação de DUAS pernas com o mesmo `transfer_pair_id`:
// saída "Pagamento de fatura — MM/YYYY" na conta que paga e entrada na conta do cartão (a que devolve o limite), ambas na categoria
// "Pagamento de Fatura", amarradas à fatura (`bill_id`). A fatura vira 'paid' (quando o pago cobre o total) ou 'partial', com `amount_paid`,
// `paid_at` e `payment_transaction_id`. Fatura 'paid': as compras dela (saídas do cartão com o `credit_card_bill_date` da fatura) ficam quitadas
// na data do pagamento; 'partial': quita as compras inteiras que cabem no valor pago, na ordem da data.
// Recusas do banco (mensagens em PT-BR, que o app repassa): fatura que ainda não fechou, valor maior que o restante, pagar com outro cartão.
import { RpcError } from '../../http/rest.mjs';
import { now, uuid, dateBR } from '../../core/util.mjs';

const r2 = (n) => Math.round(Number(n) * 100) / 100;
const dia = (iso) => String(iso).slice(0, 10);

export default async function payCreditCardBill(a, { userId, db }) {
  const bill = db.first('credit_card_bills', { id: a.p_bill_id });
  const card = bill && db.first('financial_accounts', { id: bill.account_id });
  if (!bill || !card || card.type !== 'cartao') throw new RpcError('Você não tem acesso a esta fatura.', '42501');
  const payer = db.first('financial_accounts', { id: a.p_payment_account_id });
  if (!payer) throw new RpcError('Conta de pagamento não encontrada.', '42501');
  if (payer.type === 'cartao') throw new RpcError('Não é possível pagar uma fatura com outro cartão.', 'P0001');

  const ref = dia(bill.reference_month);
  const compras = db.rows('financial_transactions').filter((t) => t.account_id === card.id && t.transaction_type === 'saida' && t.credit_card_bill_date && dia(t.credit_card_bill_date) === ref);
  const total = r2(compras.reduce((s, t) => s + Number(t.amount), 0));
  const jaPago = Number(bill.amount_paid || 0);
  const restante = total - jaPago;
  const hoje = dateBR(0, now());
  if (!(hoje >= dia(bill.closing_date))) {
    const [y, m, d] = dia(bill.closing_date).split('-');
    throw new RpcError(`Esta fatura ainda não fechou. O pagamento é liberado a partir de ${d}/${m}/${y}.`, 'P0001');
  }
  const valor = Number(a.p_amount);
  if (valor > restante + 0.01) throw new RpcError('O valor informado é maior que o saldo restante da fatura.', 'P0001');
  if (!(valor > 0)) throw new RpcError('O valor do pagamento precisa ser maior que zero.', 'P0001');

  const data = a.p_payment_date || hoje;
  const par = uuid();
  const [y, m] = ref.split('-');
  const descricao = `Pagamento de fatura — ${m}/${y}`;
  const base = { company_id: bill.company_id, transaction_date: data, paid_date: data, is_paid: true, category: 'Pagamento de Fatura', notes: a.p_notes ?? null,
    transfer_pair_id: par, credit_card_bill_date: null, bill_id: bill.id, created_by: userId, amount: valor, description: descricao, amount_received: 0 };
  const saida = db.insert('financial_transactions', { ...base, account_id: a.p_payment_account_id, transaction_type: 'saida' });
  const entrada = db.insert('financial_transactions', { ...base, account_id: card.id, transaction_type: 'entrada' });

  const novoPago = r2(jaPago + valor);
  const status = novoPago >= total - 0.01 ? 'paid' : 'partial';
  const pagoEm = status === 'paid' ? now().toISOString() : null;
  db.update('credit_card_bills', { id: bill.id }, { amount_paid: novoPago, status, payment_transaction_id: saida.id, paid_at: pagoEm });

  let quitadas = 0;
  let quitadasValor = 0;
  const abertas = compras.filter((t) => !t.is_paid).sort((x, y) => String(x.transaction_date).localeCompare(String(y.transaction_date)) || String(x.created_at).localeCompare(String(y.created_at)));
  if (status === 'paid') {
    for (const t of abertas) { db.update('financial_transactions', (r) => r === t, { is_paid: true, paid_date: data }); quitadas += 1; quitadasValor += Number(t.amount); }
  } else {
    let verba = novoPago - compras.filter((t) => t.is_paid).reduce((s, t) => s + Number(t.amount), 0);
    for (const t of abertas) {
      if (verba <= 0.01) break;
      if (Number(t.amount) <= verba + 0.01) { db.update('financial_transactions', (r) => r === t, { is_paid: true, paid_date: data }); verba -= Number(t.amount); quitadas += 1; quitadasValor += Number(t.amount); }
    }
  }
  return {
    bill_id: bill.id, status, amount_paid: novoPago, bill_total: total, paid_at: pagoEm, transfer_pair_id: par,
    payment_transaction_id: saida.id, card_leg_transaction_id: entrada.id, purchases_settled: quitadas,
    purchases_settled_amount: r2(quitadasValor), unallocated_amount: 0,
  };
}
