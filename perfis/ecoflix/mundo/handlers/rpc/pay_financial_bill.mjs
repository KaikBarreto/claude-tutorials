// pay_financial_bill (app 1.59.154: supabase/migrations/20261012093000_moeda_no_titulo_na_baixa_e_no_saldo_de_parceiro.sql), caminho de UMA
// forma (p_tenders nulo), o da tela "Pagar conta"/"Receber conta" e do "Já paguei essa conta": lança o dinheiro no caixa aberto
// (dinheiro) ou na conta bancária (Pix/transferência) com a categoria e o centro de custo da conta, descrição "Pagamento: <descrição>",
// às 12:00 (Brasília) do dia pago (v_tx_at); grava bill_payments (com o vencimento anterior); soma paid_amount; "paid" quando quita,
// senão "partial" com o vencimento do restante (p_remainder_due_date); paid_at = a maior data de baixa (coluna date). Conta de pedido
// (order_id) também abate o saldo do parceiro ("Baixa de título (...)"). Devolve a conta. Tarifa, juros e várias formas não entram na
// trilha: recusados com aviso (nada inventado). T13 caps 05 e 09.
import { inserir, r2, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const bill = store.rows('financial_bills').find((b) => b.id === a.p_bill_id);
  if (!bill) throw new RpcError('Conta não encontrada.');
  if (bill.status === 'paid') throw new RpcError('Esta conta já está paga.');
  if (Array.isArray(a.p_tenders) && a.p_tenders.length) throw new RpcError('Mundo falso: várias formas de pagamento não simuladas.');
  if (num(a.p_fee_amount) > 0 || num(a.p_interest_amount) > 0) throw new RpcError('Mundo falso: tarifa e juros na baixa não simulados.');
  const valor = r2(num(a.p_amount));
  if (!(valor > 0)) throw new RpcError('Informe um valor maior que zero em pelo menos uma forma de pagamento.');
  const restante = r2(num(bill.amount) - num(bill.paid_amount));
  const aplicado = Math.min(valor, restante);
  if (valor > restante + 0.01) throw new RpcError('Mundo falso: pagamento acima do restante (crédito ao parceiro) não simulado.');
  const pagar = bill.direction === 'payable';
  const tipo = pagar ? 'withdrawal' : 'deposit';
  const txAt = `${a.p_paid_date}T15:00:00.000Z`;   // 12:00 em Brasília (v_tx_at da RPC)
  let cashTx = null, bankTx = null;
  if (a.p_payment_method === 'cash') {
    const caixa = store.rows('cash_register').find((c) => c.id === a.p_cash_register_id && c.status === 'open');
    if (!caixa) throw new RpcError(`CASH_REGISTER_NOT_OPEN: caixa ${a.p_cash_register_id} nao esta aberto (ja fechado ou inexistente)`);
    cashTx = inserir(ctx, 'cash_transactions', {
      type: tipo, amount: valor, description: `Pagamento: ${bill.description}`, category_id: bill.category_id || null,
      cost_center_id: bill.cost_center_id || null, cash_register_id: caixa.id, company_id: bill.company_id, created_by: ctx.userId || null,
      transaction_at: txAt, group_id: null,
    });
  } else {
    if (!a.p_bank_account_id) throw new RpcError('Conta bancária obrigatória para pagamento por transferência.');
    bankTx = inserir(ctx, 'bank_transactions', {
      type: tipo, amount: valor, description: `Pagamento: ${bill.description}`, category_id: bill.category_id || null,
      cost_center_id: bill.cost_center_id || null, bank_account_id: a.p_bank_account_id, cash_register_id: a.p_cash_register_id || null,
      company_id: bill.company_id, created_by: ctx.userId || null, transaction_at: txAt, group_id: null, origin_company_id: bill.company_id,
    });
  }
  const bp = db.insert('bill_payments', {
    bill_id: bill.id, company_id: bill.company_id, amount: aplicado, paid_date: a.p_paid_date, payment_method: a.p_payment_method,
    bank_account_id: a.p_bank_account_id || null, cash_register_id: a.p_cash_register_id || null, fee_amount: 0, interest_amount: 0,
    created_by: ctx.userId || null, notes: a.p_notes || null, cash_transaction_id: cashTx?.id || null, bank_transaction_id: bankTx?.id || null,
    group_id: null, previous_due_date: bill.due_date, currency: 'BRL',
  }, { companyId: bill.company_id });
  const pago = r2(num(bill.paid_amount) + aplicado);
  const quitou = pago >= num(bill.amount) - 0.01;
  const patch = {
    paid_amount: quitou ? num(bill.amount) : pago, status: quitou ? 'paid' : 'partial',
    due_date: quitou ? bill.due_date : (a.p_remainder_due_date || bill.due_date),
    paid_at: bill.paid_at && String(bill.paid_at).slice(0, 10) > a.p_paid_date ? String(bill.paid_at).slice(0, 10) : a.p_paid_date,
  };
  db.update('financial_bills', (r) => r === bill, patch);
  if (bill.order_id && ['customer', 'supplier'].includes(bill.partner_type) && bill.partner_id) {
    let et = bill.partner_type, eid = bill.partner_id;
    if (et === 'customer') { if (store.rows('customers').find((c) => c.id === eid)?.linked_supplier_id) et = 'party'; }
    else { const s = store.rows('suppliers').find((x) => x.id === eid); if (s?.linked_customer_id) { et = 'party'; eid = s.linked_customer_id; } }
    const bal = store.rows('balances').find((b) => b.company_id === bill.company_id && b.entity_type === et && b.entity_id === eid);
    if (bal && num(bal.balance) !== 0) {
      let delta = num(bal.balance) > 0 ? -aplicado : aplicado;
      if (Math.abs(delta) > Math.abs(num(bal.balance)) + 0.01) delta = -num(bal.balance);
      const mov = inserir(ctx, 'balance_movements', {
        balance_id: bal.id, company_id: bill.company_id, entity_type: et, entity_id: eid, movement_type: 'payment', amount: r2(delta),
        description: `Baixa de título (${bill.description})`, order_id: bill.order_id, payment_method: a.p_payment_method,
        created_by: ctx.userId || null, transaction_at: txAt, group_id: null,
      });
      db.update('bill_payments', { id: bp.id }, { ledger_movement_id: mov.id });
      db.update('balances', { id: bal.id }, { balance: r2(num(bal.balance) + delta) });
    }
  }
  return store.rows('financial_bills').find((b) => b.id === bill.id);
};
