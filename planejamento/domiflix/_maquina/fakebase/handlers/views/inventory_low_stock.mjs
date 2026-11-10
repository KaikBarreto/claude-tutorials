// VIEW inventory_low_stock · 20261013150000_customer_paid_expenses_and_customer_stock.sql
// Um registro por (material, local) ABAIXO DO MÍNIMO: mínimo > 0, saldo < mínimo e material PRESENTE no local (ausente não conta).
// Alimenta a faixa vermelha "N materiais abaixo do mínimo" da aba Compras de Material e a janela "Itens abaixo do mínimo"
// ("Deficit" = mínimo − saldo). Só materiais e locais gerais (sem cliente), material não arquivado. Ordem: local, material.
export default function inventoryLowStock(store) {
  const mat = new Map(store.rows('inventory').map((i) => [i.id, i]));
  const loc = new Map(store.rows('stocks').map((s) => [s.id, s]));
  const out = [];
  for (const l of store.rows('inventory_stock_levels')) {
    const i = mat.get(l.inventory_id);
    const s = loc.get(l.stock_id);
    if (!i || !s || i.customer_id || s.customer_id || i.archived_at) continue;
    const min = l.min_quantity;
    if (min === null || min === undefined || !(Number(min) > 0)) continue;
    if (!(Number(l.quantity) < Number(min)) || !l.is_present) continue;
    out.push({
      company_id: l.company_id, inventory_id: i.id, material_name: i.name, material_sku: i.sku ?? null, stock_id: s.id, stock_name: s.name,
      quantity: Number(l.quantity), min_quantity: Number(min), unit: i.unit, deficit: Math.round((Number(min) - Number(l.quantity)) * 1e6) / 1e6,
      cost_price: i.cost_price ?? null,
    });
  }
  return out.sort((a, b) => String(a.stock_name).localeCompare(String(b.stock_name), 'pt-BR') || String(a.material_name).localeCompare(String(b.material_name), 'pt-BR'));
}
