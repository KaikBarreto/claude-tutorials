// Finaliza uma compra numa transação só (cabeçalho, itens, estoque, dinheiro/banco/saldo e parcelas), como a função SQL.
import { criarPedido } from '../../lib/eco.mjs';
export default (a, ctx) => criarPedido(ctx, 'purchase', a);
