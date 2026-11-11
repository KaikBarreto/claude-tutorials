// Depois de excluir/editar um pedido, o app pede para recalcular os saldos "antes/depois" dos movimentos do material (T9). Aqui os
// movimentos já saem coerentes do desfazer (lib/pedido_estorno.mjs): refaz a corrente a partir do saldo atual do material.
import { num } from '../../lib/eco.mjs';
export default (a, { store }) => {
  const m = store.rows('materials').find((x) => x.id === a.p_material_id);
  if (!m) return { material_id: a.p_material_id, updated: 0 };
  const movs = store.rows('stock_movements').filter((s) => s.material_id === m.id).sort((x, y) => String(y.transaction_at || y.created_at).localeCompare(String(x.transaction_at || x.created_at)));
  let depois = num(m.current_stock), n = 0;
  for (const s of movs) {
    const antes = Math.round((depois - num(s.quantity)) * 1000) / 1000;
    if (num(s.stock_after) !== depois || num(s.stock_before) !== antes) { s.stock_after = depois; s.stock_before = antes; n++; }
    depois = antes;
  }
  if (n) store.table('stock_movements').touch();
  return { material_id: m.id, updated: n };
};
