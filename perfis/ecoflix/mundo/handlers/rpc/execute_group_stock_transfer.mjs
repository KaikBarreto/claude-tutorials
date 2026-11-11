// RPC execute_group_stock_transfer (20260908213000), o "Executar" / "Confirmar e Executar" da lista de transferências: só a dona do grupo;
// _execute_group_transfer_row: recusa a que não está pendente e saldo insuficiente na origem; tira da origem e põe no destino
// (materials.current_stock) e grava os dois stock_movements TRANSFERENCIA ("Transferência entre unidades (saída)" / "(entrada)", ligados por
// related_movement_id); a linha vira 'completed' com completed_at.
import { exigeDono, agora } from '../../lib/grupo.mjs';
import { inserir, num, r3 } from '../../lib/eco.mjs';
export function executaTransferencia(ctx, id) {
  const { store, RpcError } = ctx;
  const t = store.rows('group_stock_transfers').find((x) => x.id === id);
  if (!t) throw new RpcError('Transfer not found');
  if (t.status !== 'pending') throw new RpcError('Transfer already processed');
  if (!t.from_material_id || !t.to_material_id) throw new RpcError('Both source and destination materials must be set');
  const o = store.rows('materials').find((m) => m.id === t.from_material_id);
  const d = store.rows('materials').find((m) => m.id === t.to_material_id);
  const q = num(t.quantity);
  const oA = num(o?.current_stock);
  if (oA < q) throw new RpcError(`Estoque insuficiente (disponível: ${oA})`);
  const dA = num(d?.current_stock);
  o.current_stock = r3(oA - q);
  d.current_stock = r3(dA + q);
  store.table('materials').touch();
  const iso = new Date(agora()).toISOString();
  const sai = inserir(ctx, 'stock_movements', { company_id: o.company_id, material_id: o.id, type: 'TRANSFERENCIA', quantity: -q, stock_before: oA, stock_after: r3(oA - q),
    description: 'Transferência entre unidades (saída)', created_by: ctx.userId || null, transaction_at: iso, created_at: iso });
  inserir(ctx, 'stock_movements', { company_id: d.company_id, material_id: d.id, type: 'TRANSFERENCIA', quantity: q, stock_before: dA, stock_after: r3(dA + q),
    description: 'Transferência entre unidades (entrada)', related_movement_id: sai.id, created_by: ctx.userId || null, transaction_at: iso, created_at: iso });
  t.status = 'completed';
  t.completed_at = iso;
  store.table('group_stock_transfers').touch();
  return { transfer_id: t.id, status: 'completed', quantity: q, from_material_id: o.id, to_material_id: d.id, from_stock_after: r3(oA - q), to_stock_after: r3(dA + q) };
}
export default (a, ctx) => {
  const t = ctx.store.rows('group_stock_transfers').find((x) => x.id === a._transfer_id);
  if (!t) throw new ctx.RpcError('Transfer not found');
  exigeDono(ctx, t.group_id);
  executaTransferencia(ctx, t.id);
  return null;
};
