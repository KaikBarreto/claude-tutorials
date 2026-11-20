// update_financial_transaction_categories_batch(p_cash_ids, p_bank_ids, p_category_id) (app 1.60.18, BulkEditFinancialCategoryDialog): troca a categoria de
// até 100 lançamentos manuais do caixa e do banco de uma vez (T15 cap14). Tudo ou nada; só receitas OU só despesas; valores e saldos não mudam.
import { atualizar } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const cash = [...new Set(a.p_cash_ids || [])], bank = [...new Set(a.p_bank_ids || [])];
  if (cash.length + bank.length > 100) throw new RpcError('LIMIT: selecione no máximo 100 lançamentos por vez.', '22023');
  const achar = (tab, ids) => ids.map((id) => {
    const r = store.rows(tab).find((x) => x.id === id && x.company_id === ctx.companyId);
    if (!r) throw new RpcError('NOT_FOUND: um dos lançamentos não existe mais.', 'P0002');
    return r;
  });
  const sel = [...achar('cash_transactions', cash).map((r) => ({ tab: 'cash_transactions', r, in: ['deposit', 'sale'].includes(r.type) })),
    ...achar('bank_transactions', bank).map((r) => ({ tab: 'bank_transactions', r, in: r.type === 'deposit' }))];
  if (new Set(sel.map((s) => s.in)).size > 1) throw new RpcError('DIRECTION_MISMATCH: selecione somente receitas ou somente despesas.', '22023');
  if (a.p_category_id && !store.rows('financial_categories').some((c) => c.id === a.p_category_id && c.company_id === ctx.companyId)) throw new RpcError('NOT_FOUND: categoria não encontrada.', 'P0002');
  for (const s of sel) atualizar(ctx, s.tab, { id: s.r.id }, { category_id: a.p_category_id || null });
  return null;
};
