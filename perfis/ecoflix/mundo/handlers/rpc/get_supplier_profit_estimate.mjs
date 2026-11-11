// get_supplier_profit_estimate(p_company_id, p_supplier_id, p_start_date, p_end_date): a aba "Lucro estimado" da ficha do fornecedor
// (pages/SupplierProfitEstimate.tsx; T4 cap10). Por material comprado DESSE fornecedor no período: quantidade líquida e valor pago
// (preço médio de compra) e o preço médio de venda do material no mesmo período, de TODAS as vendas da empresa (sucata é fungível);
// sem venda no período, o preço de venda do cadastro com sale_price_is_fallback (o "*" da tela). Margem/kg = venda − compra;
// margem total = margem/kg × quantidade comprada. Ordem: código do material (a migration do app não está nesta cópia).
import { janela, pedidos, itensDe, liquido, materiais, num, r2, r3 } from '../../lib/eco.mjs';

const r4 = (n) => Math.round((Number(n) || 0) * 10000) / 10000;

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const j = janela(a.p_start_date, a.p_end_date);
  const compras = pedidos(store, cid, 'purchase', j).filter((p) => p.supplier_id === a.p_supplier_id);
  const somar = (lista, tipo) => {
    const its = itensDe(store, tipo, lista);
    const m = new Map();
    for (const p of lista) for (const it of its.get(p.id) || []) {
      const e = m.get(it.material_id) || { q: 0, v: 0 };
      e.q += liquido(it);
      e.v += num(it.total_price);
      m.set(it.material_id, e);
    }
    return m;
  };
  const comprado = somar(compras, 'purchase');
  const vendido = somar(pedidos(store, cid, 'sale', j), 'sale');
  const mats = new Map(materiais(store, cid).map((m) => [m.id, m]));
  return [...comprado.entries()].map(([mid, e]) => {
    const m = mats.get(mid) || {};
    const v = vendido.get(mid);
    const compra = e.q ? e.v / e.q : 0;
    const fallback = !(v && v.q > 0);
    const venda = fallback ? (m.sale_price != null ? num(m.sale_price) : null) : v.v / v.q;
    const unit = venda != null ? venda - compra : null;
    return {
      material_id: mid, material_name: m.name || null, material_code: m.code ?? null, currency: 'BRL', moedas_misturadas: false,
      qty_bought: r3(e.q), buy_value: r2(e.v), buy_value_by_currency: { BRL: r2(e.v) }, avg_buy_price: r4(compra),
      qty_sold: r3(v?.q || 0), avg_sale_price: venda != null ? r4(venda) : null, sale_price_is_fallback: fallback,
      est_margin_unit: unit != null ? r4(unit) : null, est_margin_total: unit != null ? r2(unit * e.q) : null,
    };
  }).sort((x, y) => (Number(x.material_code) || 0) - (Number(y.material_code) || 0));
};
