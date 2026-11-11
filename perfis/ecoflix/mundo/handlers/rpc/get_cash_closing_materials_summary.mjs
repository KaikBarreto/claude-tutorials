// Material por material, o que os pedidos de um caixa compraram e venderam (Relatório de estoque do Histórico do Caixa e o resumo do
// fechamento, T9), como a função SQL: soma o peso líquido (quantidade - impureza) e o valor dos itens dos pedidos pedidos.
import { num, r2, r3 } from '../../lib/eco.mjs';
export default (a, { store }) => {
  const compras = new Set(Array.isArray(a.p_purchase_ids) ? a.p_purchase_ids : []);
  const vendas = new Set(Array.isArray(a.p_sale_ids) ? a.p_sale_ids : []);
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const por = new Map();
  const linha = (mid, nome) => {
    if (!por.has(mid)) {
      const m = mats.get(mid) || {};
      por.set(mid, { material_id: mid, material_code: m.code != null ? String(m.code) : null, material_name: m.name || nome, unit: m.unit || 'Kg',
        total_purchased_qty: 0, total_purchased_value: 0, total_sold_qty: 0, total_sold_value: 0 });
    }
    return por.get(mid);
  };
  for (const i of store.rows('purchase_items')) {
    if (!compras.has(i.purchase_id)) continue;
    const l = linha(i.material_id, i.material_name);
    l.total_purchased_qty = r3(l.total_purchased_qty + num(i.quantity) - num(i.impurity));
    l.total_purchased_value = r2(l.total_purchased_value + num(i.total_price));
  }
  for (const i of store.rows('sale_items')) {
    if (!vendas.has(i.sale_id)) continue;
    const l = linha(i.material_id, i.material_name);
    l.total_sold_qty = r3(l.total_sold_qty + num(i.quantity) - num(i.impurity));
    l.total_sold_value = r2(l.total_sold_value + num(i.total_price));
  }
  return [...por.values()].sort((x, y) => String(x.material_name).localeCompare(String(y.material_name), 'pt-BR'));
};
