// update_balance(p_company_id, p_entity_type, p_entity_id, p_amount): soma p_amount ao saldo do parceiro e devolve o id da linha de
// `balances` (components/BalancePaymentModal.tsx, passo 2 da Nova Movimentação; T4 cap09). Parceiro duplo vai para a linha `party`
// (lib/eco.mjs, atualizaSaldo: a mesma conta que os pedidos usam).
import { atualizaSaldo, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const b = atualizaSaldo(ctx, a.p_company_id || ctx.companyId, a.p_entity_type, a.p_entity_id, num(a.p_amount));
  return b.id;
};
