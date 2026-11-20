// pay_financial_bills_batch (app 1.60.18: supabase/migrations/20260923200000_pay_financial_bills_batch.sql): quita N contas por UM lançamento só.
// Um lançamento (caixa ou banco) com o total do restante de cada conta, categoria da conta se todas forem da mesma (senão sem categoria),
// descrição = p_description; uma baixa em bill_payments por conta, todas com o mesmo group_id do lançamento. Cada conta fica "paid". Tarifa, juros e
// linhas de saldo não entram na trilha do mundo falso (recusados com aviso). Devolve { group_id, transaction_id, transaction_kind, total, ... }. T13 cap13.
import { randomUUID } from 'node:crypto';
import { inserir, r2, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  if (Array.isArray(a.p_balance_targets) && a.p_balance_targets.length) throw new RpcError('Mundo falso: linhas de saldo no lote não simuladas.');
  if (num(a.p_fee_amount) > 0 || num(a.p_interest_amount) > 0) throw new RpcError('Mundo falso: tarifa e juros no lote não simulados.');
  const ids = a.p_bill_ids || [];
  const contas = ids.map((id) => store.rows('financial_bills').find((b) => b.id === id)).filter(Boolean);
  if (contas.length < 2) throw new RpcError('Marque ao menos 2 linhas para pagar em lote');
  const pagar = contas[0].direction === 'payable';
  const itens = contas.map((b) => ({ b, resto: r2(num(b.amount) - num(b.paid_amount)) })).filter((x) => x.resto > 0);
  const total = r2(itens.reduce((s, x) => s + x.resto, 0));
  const cats = new Set(contas.map((b) => b.category_id || null));
  const categoria = cats.size === 1 ? [...cats][0] : null;
  const ccs = new Set(contas.map((b) => b.cost_center_id || null));
  const centro = ccs.size === 1 ? [...ccs][0] : null;
  const desc = String(a.p_description || '').trim() || 'Pagamento agrupado';
  const tipo = pagar ? 'withdrawal' : 'deposit';
  const txAt = `${a.p_paid_date}T15:00:00.000Z`;   // 12:00 em Brasília
  const grupo = randomUUID();
  let cashTx = null, bankTx = null;
  if (a.p_payment_method === 'cash') {
    const caixa = store.rows('cash_register').find((c) => c.id === a.p_cash_register_id && c.status === 'open');
    if (!caixa) throw new RpcError(`CASH_REGISTER_NOT_OPEN: caixa ${a.p_cash_register_id} nao esta aberto (ja fechado ou inexistente)`);
    cashTx = inserir(ctx, 'cash_transactions', { type: tipo, amount: total, description: desc, category_id: categoria, cost_center_id: centro,
      cash_register_id: caixa.id, company_id: contas[0].company_id, created_by: ctx.userId || null, transaction_at: txAt, group_id: grupo });
  } else {
    if (!a.p_bank_account_id) throw new RpcError('Conta bancária obrigatória para pagamento por transferência.');
    bankTx = inserir(ctx, 'bank_transactions', { type: tipo, amount: total, description: desc, category_id: categoria, cost_center_id: centro,
      bank_account_id: a.p_bank_account_id, cash_register_id: a.p_cash_register_id || null, company_id: contas[0].company_id,
      created_by: ctx.userId || null, transaction_at: txAt, group_id: grupo, origin_company_id: contas[0].company_id });
  }
  for (const { b, resto } of itens) {
    db.insert('bill_payments', { bill_id: b.id, company_id: b.company_id, amount: resto, paid_date: a.p_paid_date, payment_method: a.p_payment_method,
      bank_account_id: a.p_bank_account_id || null, cash_register_id: a.p_cash_register_id || null, fee_amount: 0, interest_amount: 0,
      created_by: ctx.userId || null, notes: a.p_notes || null, cash_transaction_id: cashTx?.id || null, bank_transaction_id: bankTx?.id || null,
      group_id: grupo, previous_due_date: b.due_date, currency: 'BRL' }, { companyId: b.company_id });
    db.update('financial_bills', (r) => r === b, { paid_amount: num(b.amount), status: 'paid', paid_at: a.p_paid_date });
  }
  return { group_id: grupo, transaction_id: (cashTx || bankTx).id, transaction_kind: cashTx ? 'cash' : 'bank', fee_transaction_id: null, total,
    bill_count: itens.length, balance_count: 0, description: desc, category_id: categoria, excluded_from_dre: false };
};
