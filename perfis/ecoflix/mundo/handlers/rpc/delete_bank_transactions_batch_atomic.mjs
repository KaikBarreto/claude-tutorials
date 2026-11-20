// delete_bank_transactions_batch_atomic(p_tx_ids) (app 1.60.18: supabase/migrations/20261116143500_delete_bank_transactions_batch_atomic.sql): exclusão em
// massa do histórico da conta (T14, "Excluir selecionados"). Tudo ou nada: valida o lote inteiro (até 100, uma conta bancária só, só avulso de tipo
// deposit/withdrawal/expense/transfer, nada conciliado nem de pedido nem ligado a baixa de conta) e só então apaga; lançamento com group_id leva o grupo
// junto (como a exclusão individual). O saldo gravado se recalcula pelo gatilho de bank_transactions. Devolve { deleted_count }.
import { remover } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const ids = [...new Set((a.p_tx_ids || []).filter(Boolean))];
  if (!ids.length) throw new RpcError('BANK_BATCH_EMPTY: selecione pelo menos um lançamento.');
  if (ids.length > 100) throw new RpcError('BANK_BATCH_LIMIT: selecione no máximo 100 lançamentos por vez.');
  const todas = store.rows('bank_transactions');
  const sel = ids.map((id) => todas.find((b) => b.id === id));
  if (sel.some((b) => !b || b.company_id !== ctx.companyId)) throw new RpcError('BANK_BATCH_TRANSACTION_NOT_FOUND: um ou mais lançamentos não existem mais. Atualize a tela e tente novamente.');
  if (new Set(sel.map((b) => b.bank_account_id)).size > 1) throw new RpcError('BANK_BATCH_ACCOUNT_MISMATCH: selecione lançamentos de uma única conta bancária.');
  const grupos = new Set(sel.map((b) => b.group_id).filter(Boolean));
  const alvo = todas.filter((b) => ids.includes(b.id) || (b.group_id && grupos.has(b.group_id)));
  const alvoIds = new Set(alvo.map((b) => b.id));
  const ok = ['deposit', 'withdrawal', 'expense', 'transfer'];
  if (sel.some((b) => b.order_id || !ok.includes(b.type))) throw new RpcError('BANK_BATCH_INELIGIBLE: a seleção contém lançamento vinculado ou de tipo não excluível.');
  if (store.rows('reconciliation_matches').some((m) => alvoIds.has(m.bank_transaction_id))) throw new RpcError('transacao_conciliada_desfaca_primeiro');
  if (store.rows('bill_payments').some((p) => alvoIds.has(p.bank_transaction_id))) throw new RpcError('BANK_BATCH_INELIGIBLE: a seleção contém lançamento vinculado ou de tipo não excluível.');
  remover(ctx, 'bank_transactions', (b) => alvoIds.has(b.id));
  return { deleted_count: alvo.length, requested_count: ids.length };
};
