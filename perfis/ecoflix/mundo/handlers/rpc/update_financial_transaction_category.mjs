// update_financial_transaction_category(p_table, p_transaction_id, p_category_id): troca a categoria de UM lançamento do caixa ou do banco
// (lápis "Editar categoria" do Histórico, T15 cap14). Só categoria: valores e saldos não mudam. p_table: cash_transactions | bank_transactions.
import { atualizar } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  if (!['cash_transactions', 'bank_transactions'].includes(a.p_table)) throw new RpcError('Tabela inválida para troca de categoria.', '22023');
  const l = store.rows(a.p_table).find((r) => r.id === a.p_transaction_id && r.company_id === ctx.companyId);
  if (!l) throw new RpcError('NOT_FOUND: lançamento não encontrado.', 'P0002');
  if (a.p_category_id && !store.rows('financial_categories').some((c) => c.id === a.p_category_id && c.company_id === ctx.companyId)) throw new RpcError('NOT_FOUND: categoria não encontrada.', 'P0002');
  atualizar(ctx, a.p_table, { id: l.id }, { category_id: a.p_category_id || null });
  return null;
};
