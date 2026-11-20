// pay_recurring_financial_bill (app 1.60.18: supabase/migrations/20261117180000_recurring_bill_realized_amount.sql): baixa de uma ocorrência de
// recorrência pelo VALOR REAL do mês ("Valor desta ocorrência"). Troca o `amount` da conta (e, com p_update_future_amounts, o do molde e o das
// próximas pendentes ainda no valor do molde) e depois faz a baixa normal (pay_financial_bill). T13 cap12.
import { r2, num } from '../../lib/eco.mjs';
import pagar from './pay_financial_bill.mjs';

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const bill = store.rows('financial_bills').find((b) => b.id === a.p_bill_id);
  if (!bill) throw new RpcError('Conta não encontrada.');
  const molde = bill.recurring_template_id && store.rows('recurring_bill_templates').find((t) => t.id === bill.recurring_template_id);
  if (!molde) throw new RpcError('Somente contas recorrentes permitem ajustar o valor na baixa.');
  const novo = r2(num(a.p_occurrence_amount));
  if (!(novo > 0)) throw new RpcError('Informe um valor positivo com a precisão da moeda da conta.');
  if (bill.status !== 'pending' || num(bill.paid_amount) !== 0 || bill.source_type || bill.order_id) {
    throw new RpcError('Esta ocorrência já possui pagamento ou vínculo gerenciado e não permite alterar o valor.');
  }
  if (novo !== num(bill.amount)) {
    if (a.p_update_future_amounts) {
      for (const b of store.rows('financial_bills')) {
        if (b.recurring_template_id === molde.id && b.due_date > bill.due_date && b.status === 'pending' && num(b.paid_amount) === 0 && num(b.amount) === num(molde.amount)) {
          db.update('financial_bills', (r) => r === b, { amount: novo });
        }
      }
      db.update('recurring_bill_templates', { id: molde.id }, { amount: novo });
    }
    db.update('financial_bills', (r) => r === bill, { amount: novo });
  }
  const { p_occurrence_amount, p_update_future_amounts, ...resto } = a;
  return pagar(resto, ctx);
};
