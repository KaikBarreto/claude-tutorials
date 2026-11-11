// Venda com transferência de estoque entre materiais numa transação só, como a função SQL
// (20261006130000_venda_com_transferencia_repassa_o_caixa_escolhido.sql): idempotência pelo client_request_id da venda; cada
// transferência local chama transfer_material_stock(origem, destino, quantidade, id da transferência) e, no fim, a venda
// (create_sale_atomic) com o jsonb p_sale. Transferência entre unidades (scope 'group') não existe no mundo falso. T07 cap14:
// 18 kg de Cobre misto para o Cobre mel na finalização da venda à Fundição Bandeira do Vale.
import { criarPedido } from '../../lib/eco.mjs';
import transferir from './transfer_material_stock.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const venda = a.p_sale || {};
  const args = Object.fromEntries(Object.entries(venda).map(([k, v]) => [`p_${k}`, v]));
  const cid = args.p_company_id || ctx.companyId;
  if (args.p_client_request_id) {
    const ja = store.rows('sales').find((p) => p.company_id === cid && p.client_request_id === args.p_client_request_id);
    if (ja) return criarPedido(ctx, 'sale', args);   // devolve o pedido que já existe, sem transferir de novo
  }
  const lista = Array.isArray(a.p_stock_transfers) ? a.p_stock_transfers : [];
  for (const t of lista) {
    const scope = t.scope || 'local';
    const q = Number(t.quantity) || 0;
    if (!t.id || !t.source_material_id || !t.target_material_id || q <= 0) throw new RpcError('Transferência inválida', 'P0001');
    if (scope !== 'local') throw new RpcError(`Tipo de transferência inválido no mundo falso: ${scope}`, 'P0001');
    transferir({ p_source_id: t.source_material_id, p_target_id: t.target_material_id, p_quantity: q, p_client_request_id: t.id }, ctx);
  }
  return criarPedido(ctx, 'sale', args);
};
