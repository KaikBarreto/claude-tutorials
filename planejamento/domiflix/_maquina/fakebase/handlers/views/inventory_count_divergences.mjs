// VIEW inventory_count_divergences · 20260721170000_inventario_e_posicao_de_estoque.sql
// Uma linha por item do inventário (a tela filtra os que têm `diff` ≠ 0 e já contados): esperado, contado, diferença, custo unitário
// (o da contagem, senão o cadastrado) e valor da divergência (diferença × custo). Alimenta a aba "Divergências" e a faixa amarela.
export default function inventoryCountDivergences(store) {
  const cont = new Map(store.rows('inventory_counts').map((c) => [c.id, c]));
  const mat = new Map(store.rows('inventory').map((i) => [i.id, i]));
  const loc = new Map(store.rows('stocks').map((s) => [s.id, s]));
  const out = [];
  for (const ci of store.rows('inventory_count_items')) {
    const c = cont.get(ci.count_id);
    const i = mat.get(ci.inventory_id);
    const s = loc.get(ci.stock_id);
    if (!c || !i || !s) continue;
    const custo = ci.unit_cost ?? i.cost_price ?? 0;
    out.push({
      item_id: ci.id, company_id: ci.company_id, count_id: ci.count_id, count_numero: c.numero, count_status: c.status,
      inventory_id: ci.inventory_id, material_name: i.name, material_sku: i.sku ?? null, material_unit: i.unit ?? null,
      stock_id: ci.stock_id, stock_name: s.name, expected_qty: ci.expected_qty, counted_qty: ci.counted_qty, diff: ci.diff ?? null,
      unit_cost: Number(custo), diff_value: ci.diff === null || ci.diff === undefined ? null : Number(ci.diff) * Number(custo),
    });
  }
  return out;
}
