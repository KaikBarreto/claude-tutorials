// reconcile_create_transaction (T14 cap09, "Criar despesa"): lançamento novo na conta da linha, na data dela (deposit ou expense), e o vínculo
// (match_type created). Categoria obrigatória, salvo "Não é receita nem despesa".
import { num } from '../../lib/eco.mjs';
import { linha, pendente, casar } from '../../lib/conciliacao.mjs';
import { inserir } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const e = linha(ctx, a.p_entry_id);
  pendente(ctx, e);
  if (!a.p_category_id && a.p_excluded_from_dre !== true) throw new RpcError('Categoria obrigatória.');
  if (a.p_category_id && !store.rows('financial_categories').some((c) => c.id === a.p_category_id)) throw new RpcError('Categoria não encontrada.');
  const bt = inserir(ctx, 'bank_transactions', {
    company_id: e.company_id, bank_account_id: e.bank_account_id, type: num(e.amount) >= 0 ? 'deposit' : 'expense', amount: Math.abs(num(e.amount)),
    description: a.p_description ?? null, category_id: a.p_category_id ?? null, cost_center_id: a.p_cost_center_id ?? null, created_by: ctx.userId,
    transaction_at: e.posted_at, source: 'manual', partner_id: a.p_partner_id ?? null, partner_type: a.p_partner_type ?? null,
    excluded_from_dre: a.p_excluded_from_dre === true,
  });
  casar(ctx, e, bt, { tipo: 'created' });
  return bt.id;
};
