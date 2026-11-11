// Prévia da exclusão de um pedido ("Vou desfazer tudo que este pedido criou:"): estoque, faturas e pagamentos que somem ou são
// estornados, como a função SQL da 1.59.154 (20261002250000). A lógica mora em lib/pedido_estorno.mjs (T9).
import { previa } from '../../lib/pedido_estorno.mjs';
export default (a, ctx) => previa(ctx, a.p_order_type === 'sale' ? 'sale' : 'purchase', a.p_order_id);
