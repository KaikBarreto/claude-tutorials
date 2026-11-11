// update_bank_account_balance (saque para o cofre, 2 pernas): recalcula o saldo gravado da conta (cofre: a fórmula única do lib/eco.mjs).
import { recalculaConta } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const conta = ctx.store.rows('bank_accounts').find((b) => b.id === a.p_bank_account_id);
  if (!conta) return null;
  recalculaConta(ctx.store, conta);
  return conta.id;
};
