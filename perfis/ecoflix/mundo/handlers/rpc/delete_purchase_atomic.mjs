// Exclui uma compra numa transação só (T9): caixa de origem aberto = some de vez (estoque, dinheiro, banco, saldo, faturas, itens);
// fechado = estorno compensado no caixa de hoje (p_compensation_register_id). Grava a linha do Histórico de Exclusões
// (destructive_actions_audit, rótulo = nome do fornecedor). Lógica em lib/pedido_estorno.mjs.
import { desfaz, auditoria } from '../../lib/pedido_estorno.mjs';
export default (a, ctx) => {
  const r = desfaz(ctx, 'purchase', a.p_purchase_id, a.p_compensation_register_id || null);
  if (r.modo === 'ausente') throw new ctx.RpcError('Pedido não encontrado');
  if (r.modo === 'ja_revertido') return { success: true, already_reverted: true, reverted_mode: 'compensated', order_number: r.pedido.order_number };
  auditoria(ctx, 'purchase', r.pedido, r.modo);
  return { success: true, reverted_mode: r.modo, order_number: r.pedido.order_number };
};
