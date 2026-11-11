// "Cupom sem valor" / "Mostrar valores no comprovante" (T9): liga ou desliga o comprovante sem valores do pedido, como a função SQL.
import { atualizar } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const tab = a.p_order_type === 'sale' ? 'sales' : 'purchases';
  const alvo = atualizar(ctx, tab, { id: a.p_order_id }, { hide_financial_details: !!a.p_value });
  if (!alvo.length) throw new ctx.RpcError('Pedido não encontrado');
  return true;
};
