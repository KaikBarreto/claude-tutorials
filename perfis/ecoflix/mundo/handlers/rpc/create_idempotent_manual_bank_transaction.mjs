// create_idempotent_manual_bank_transaction (utils/bankAccountUtils.ts, insertBankTransaction com client_request_id): igual ao create_manual_bank_transaction,
// com a chave de idempotência (client_request_id), o vínculo com a fatura do cartão (p_credit_card_bill_date) e o parcelamento. Usado pela Nova Despesa
// com o cartão na origem (T14 cap03). Devolve already_existed.
import { inserir, agoraMs, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const cid = a.p_company_id || ctx.companyId;
  if (!a.p_bank_account_id) throw new ctx.RpcError('Conta bancária obrigatória');
  if (a.p_client_request_id) {
    const ja = ctx.store.rows('bank_transactions').find((b) => b.client_request_id === a.p_client_request_id && b.installment_number === (a.p_installment_number ?? null));
    if (ja) return [{ id: ja.id, balance_after: ja.balance_after, company_id: cid, origin_company_id: null, already_existed: true }];
  }
  const txAt = a.p_transaction_at || (a.p_transaction_date ? `${a.p_transaction_date}T15:00:00.000Z` : new Date(agoraMs()).toISOString());
  const r = inserir(ctx, 'bank_transactions', {
    company_id: cid, type: a.p_type, amount: num(a.p_amount), description: a.p_description || null, bank_account_id: a.p_bank_account_id,
    category_id: a.p_category_id || null, cost_center_id: a.p_cost_center_id || null, cash_register_id: a.p_cash_register_id || null,
    transaction_at: txAt, group_id: a.p_group_id || null, order_id: a.p_order_id || null, excluded_from_dre: !!a.p_excluded_from_dre,
    partner_id: a.p_partner_id || null, partner_type: a.p_partner_type || null, payment_method: a.p_payment_method || null,
    employee_movement_id: a.p_employee_movement_id || null, credit_card_bill_date: a.p_credit_card_bill_date || null,
    installment_group_id: a.p_installment_group_id || null, installment_number: a.p_installment_number ?? null, installment_total: a.p_installment_total ?? null,
    client_request_id: a.p_client_request_id || null, created_by: a.p_created_by || ctx.userId, source: 'manual', origin_company_id: null,
  });
  return [{ id: r.id, balance_after: r.balance_after, company_id: cid, origin_company_id: null, already_existed: false }];
};
