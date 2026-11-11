// create_installment_bills (app 1.59.154: supabase/migrations/20260904100200_payment_method_boleto_cheque.sql; chamada em hooks/useBills.ts
// createInstallmentBills): uma conta por parcela, "<descrição> (parcela i/N)", pendente, com installment_number/installment_total, a
// condição de pagamento e o pagamento previsto. Confere a soma com p_expected_total (tolerância de 1 centavo). Devolve
// { created_count, bill_ids }. Parcelamento não leva centro de custo (a RPC não recebe o campo). T13 cap06.
import { r2, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { db, RpcError } = ctx;
  const cid = a.p_company_id || ctx.companyId;
  if (!['payable', 'receivable'].includes(a.p_direction)) throw new RpcError(`p_direction deve ser payable ou receivable, recebido: ${a.p_direction}`);
  const parcelas = Array.isArray(a.p_installments) ? a.p_installments : [];
  if (!parcelas.length) throw new RpcError('p_installments vazio — informe ao menos 1 parcela');
  const soma = r2(parcelas.reduce((s, p) => s + num(p.amount), 0));
  if (a.p_expected_total != null && Math.abs(soma - num(a.p_expected_total)) > 0.01) {
    throw new RpcError(`Soma das parcelas (R$ ${soma}) diverge do total (R$ ${a.p_expected_total})`);
  }
  const n = parcelas.length;
  const ids = parcelas.map((p) => db.insert('financial_bills', {
    company_id: cid, direction: a.p_direction, description: `${a.p_description} (parcela ${num(p.number) || 1}/${n})`,
    category_id: a.p_category_id || null, amount: r2(p.amount), paid_amount: 0, currency: 'BRL', due_date: p.due_date || null, status: 'pending',
    partner_type: a.p_partner_type || null, partner_id: a.p_partner_id || null, payment_condition_id: a.p_payment_condition_id || null,
    installment_number: num(p.number) || 1, installment_total: n, notes: a.p_notes || null, created_by: a.p_user_id || ctx.userId || null,
    expected_payment_method: a.p_expected_payment_method || null, expected_bank_account_id: a.p_expected_bank_account_id || null,
  }, { companyId: cid }).id);
  return { created_count: n, bill_ids: ids };
};
