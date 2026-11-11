// adjust_cash_register_balance (utils/cashRegisterUtils.ts, depois do vale/recebimento/pagamento em dinheiro, T19 caps 5 e 6): na
// 1.59.154 o saldo da gaveta é derivado do razão (migration 20260926164000_saldo_do_caixa_derivado_do_razao.sql); no banco falso o
// "trigger" de cash_transactions já recalculou (lib/eco.mjs), então só devolve o saldo da gaveta.
import { recalculaCaixa, saldoCaixa } from '../../lib/eco.mjs';

export default (a, { store, RpcError }) => {
  const c = store.rows('cash_register').find((x) => x.id === a.p_register_id);
  if (!c) throw new RpcError('Caixa não encontrado');
  recalculaCaixa(store, c.id);
  return saldoCaixa(store, c);
};
