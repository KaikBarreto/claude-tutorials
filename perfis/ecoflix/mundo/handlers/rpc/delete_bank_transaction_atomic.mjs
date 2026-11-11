// delete_bank_transaction_atomic (T15 cap10, "Excluir lançamento" do Histórico): lançamento avulso do banco. Ramos da função usados
// nas aulas: conciliado -> recusa (transacao_conciliada_desfaca_primeiro); perna em pedido ou no Cofre -> recusa; com group_id -> apaga as
// pernas do grupo (3c); sem group_id -> apaga a própria linha (3c'). O saldo gravado da conta se recalcula (gatilho de bank_transactions).
// Baixa de conta a pagar/receber (2c/2d) não é usada nas aulas: recusa em vez de fingir o estorno.
import { remover } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const tx = store.rows('bank_transactions').find((b) => b.id === a.p_tx_id);
  if (!tx || tx.company_id !== ctx.companyId) throw new RpcError('Lançamento bancário não encontrado');
  const grupo = tx.group_id ? store.rows('bank_transactions').filter((b) => b.group_id === tx.group_id) : [tx];
  const ids = new Set(grupo.map((b) => b.id));
  if (store.rows('reconciliation_matches').some((m) => ids.has(m.bank_transaction_id))) throw new RpcError('transacao_conciliada_desfaca_primeiro');
  if (store.rows('bill_payments').some((p) => ids.has(p.bank_transaction_id))) throw new RpcError('BILL_PAYMENT_TRANSACTION: desfaça a baixa pela conta');
  const contas = new Map(store.rows('bank_accounts').map((b) => [b.id, b]));
  if (grupo.some((b) => contas.get(b.bank_account_id)?.kind === 'cash')) throw new RpcError('Não é possível excluir transferência envolvendo a conta Dinheiro');
  if (grupo.some((b) => b.order_id)) throw new RpcError('Lançamento vinculado a pedido: exclua pelo pedido');
  remover(ctx, 'bank_transactions', (b) => ids.has(b.id));
  return { deleted: ids.size };
};
