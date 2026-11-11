// create_manual_bank_transaction (utils/bankAccountUtils.ts, insertBankTransaction): lançamento avulso numa conta bancária, como o
// pagamento por Pix da Nova Movimentação de Saldo (T4 cap09). Sem p_bank_account_id usa a conta padrão (não arquivada) e, sem ela, a
// mais antiga que não é cartão nem o cofre. O sinal e o saldo corrido saem dos "triggers" de bank_transactions (lib/eco.mjs).
import { inserir, contas, agoraMs, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const cid = a.p_company_id || ctx.companyId;
  const lista = contas(ctx.store, cid).filter((b) => b.kind !== 'card' && b.kind !== 'cash');
  const padrao = lista.find((b) => b.is_default) || [...lista].sort((x, y) => String(x.created_at).localeCompare(String(y.created_at)))[0];
  const conta = a.p_bank_account_id || padrao?.id;
  if (!conta) throw new ctx.RpcError('Empresa sem conta bancária para o lançamento');
  const txAt = a.p_transaction_at || (a.p_transaction_date ? `${a.p_transaction_date}T03:00:00.000Z` : new Date(agoraMs()).toISOString());
  const r = inserir(ctx, 'bank_transactions', {
    company_id: cid, type: a.p_type, amount: num(a.p_amount), description: a.p_description || null, bank_account_id: conta,
    category_id: a.p_category_id || null, cost_center_id: a.p_cost_center_id || null, cash_register_id: a.p_cash_register_id || null,
    transaction_at: txAt, group_id: a.p_group_id || null, order_id: a.p_order_id || null, excluded_from_dre: !!a.p_excluded_from_dre,
    partner_id: a.p_partner_id || null, partner_type: a.p_partner_type || null, payment_method: a.p_payment_method || null,
    employee_movement_id: a.p_employee_movement_id || null, created_by: a.p_created_by || ctx.userId, source: 'manual', origin_company_id: cid,
  });
  return [{ id: r.id, balance_after: r.balance_after, company_id: cid, origin_company_id: cid }];
};
