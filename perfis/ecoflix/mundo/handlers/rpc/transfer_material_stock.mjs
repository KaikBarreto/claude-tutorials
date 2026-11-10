// Transferência de saldo entre dois materiais da empresa, como a função SQL (20260908233000_matriz_transfere_entre_materiais_da_filial.sql):
// idempotência pelo client_request_id, recusa quantidade maior que o saldo, e os DOIS stock_movements TRANSFERENCIA ("Transferência para
// <destino>" no de origem, com o client_request_id; "Transferência de <origem>" no de destino, ligado por related_movement_id). T03 cap08:
// 8 kg do Radiador de cobre para o Ferro misto.
import { inserir, agoraMs, r3, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const q = num(a.p_quantity);
  if (!(q > 0)) throw new RpcError('Quantidade deve ser maior que zero', 'P0001');
  if (a.p_source_id === a.p_target_id) throw new RpcError('Material de destino não pode ser o mesmo que o de origem', 'P0001');
  const o = store.rows('materials').find((x) => x.id === a.p_source_id);
  if (!o) throw new RpcError('Material de origem não encontrado', 'P0001');
  const d = store.rows('materials').find((x) => x.id === a.p_target_id);
  if (!d) throw new RpcError('Material de destino não encontrado', 'P0001');
  if (o.company_id !== d.company_id) throw new RpcError('Materiais de empresas diferentes', 'P0001');
  const oAntes = num(o.current_stock);
  const dAntes = num(d.current_stock);
  const cri = a.p_client_request_id || null;
  if (cri && store.rows('stock_movements').some((s) => s.company_id === o.company_id && s.client_request_id === cri)) {
    return { source_before: oAntes, source_after: oAntes, target_before: dAntes, target_after: dAntes, source_name: o.name, target_name: d.name,
      quantity: q, idempotent_skip: true };
  }
  if (q > oAntes) throw new RpcError('Quantidade a transferir maior que o estoque disponível', 'P0001');
  const oDepois = r3(oAntes - q);
  const dDepois = r3(dAntes + q);
  const agora = new Date(agoraMs()).toISOString();
  o.current_stock = oDepois;
  d.current_stock = dDepois;
  store.table('materials').touch();
  const sai = inserir(ctx, 'stock_movements', {
    company_id: o.company_id, material_id: o.id, type: 'TRANSFERENCIA', quantity: -q, stock_before: oAntes, stock_after: oDepois,
    description: `Transferência para ${d.name}`, created_by: ctx.userId || null, client_request_id: cri, transaction_at: agora,
  });
  inserir(ctx, 'stock_movements', {
    company_id: o.company_id, material_id: d.id, type: 'TRANSFERENCIA', quantity: q, stock_before: dAntes, stock_after: dDepois,
    description: `Transferência de ${o.name}`, created_by: ctx.userId || null, related_movement_id: sai.id, transaction_at: agora,
  });
  return { source_before: oAntes, source_after: oDepois, target_before: dAntes, target_after: dDepois, source_name: o.name, target_name: d.name,
    quantity: q, via_group: false };
};
