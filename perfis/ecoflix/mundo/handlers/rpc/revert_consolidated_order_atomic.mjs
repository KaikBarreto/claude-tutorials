// Desfaz o pedido inteiro antes de gravar a versão editada (T9, Editar pedido): com o caixa de origem aberto o pedido some (estoque,
// dinheiro, banco, saldo, itens) e a tela recria com o mesmo número no mesmo caixa; com a origem fechada vira estorno compensado no
// caixa de hoje (origin_register_closed). Sem linha no Histórico de Exclusões. Lógica em lib/pedido_estorno.mjs.
import { desfaz } from '../../lib/pedido_estorno.mjs';
export default (a, ctx) => {
  const tipo = a.p_order_type === 'sale' ? 'sale' : 'purchase';
  const r = desfaz(ctx, tipo, a.p_order_id, a.p_compensation_register_id || null);
  if (r.modo === 'ausente' || r.modo === 'ja_revertido') return { success: true, already_reverted: true, origin_register_closed: false };
  const p = r.pedido;
  return { success: true, already_reverted: false, order_number: p.order_number, order_seq: p.order_seq ?? null, order_period: p.order_period ?? null,
    order_ref: p.order_ref ?? null, origin_register_closed: r.modo === 'compensated', reverted_mode: r.modo };
};
