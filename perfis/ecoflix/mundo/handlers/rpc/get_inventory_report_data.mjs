// Relatório de estoque do período por material: comprado, vendido, custo médio, CMV e saldo atual.
import { janela, pedidos, itensDe, liquido, num, r2, r3, diaDe, custoMedio } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const j = janela(a.p_start_date, a.p_end_date);
  const fs = Array.isArray(a.p_supplier_ids) && a.p_supplier_ids.length ? new Set(a.p_supplier_ids) : null;
  const fc = Array.isArray(a.p_customer_ids) && a.p_customer_ids.length ? new Set(a.p_customer_ids) : null;
  const fu = Array.isArray(a.p_creator_ids) && a.p_creator_ids.length ? new Set(a.p_creator_ids) : null;
  const compras = pedidos(store, cid, 'purchase', j).filter((p) => (!fs || fs.has(p.supplier_id)) && (!fu || fu.has(p.created_by)));
  const vendas = pedidos(store, cid, 'sale', j).filter((p) => (!fc || fc.has(p.customer_id)) && (!fu || fu.has(p.created_by)));
  const acc = new Map();
  const get = (id) => acc.get(id) || acc.set(id, { qc: 0, vc: 0, qv: 0, vv: 0 }).get(id);
  for (const its of itensDe(store, 'purchase', compras).values()) for (const it of its) { const e = get(it.material_id); e.qc += liquido(it); e.vc += num(it.total_price); }
  for (const its of itensDe(store, 'sale', vendas).values()) for (const it of its) { const e = get(it.material_id); e.qv += liquido(it); e.vv += num(it.total_price); }
  const cm = custoMedio(store, cid, j.d2);
  return store.rows('materials').filter((m) => m.company_id === cid && !m.is_archived).map((m) => {
    const e = acc.get(m.id) || { qc: 0, vc: 0, qv: 0, vv: 0 };
    const custo = cm.get(m.id) || 0;
    return {
      material_id: m.id, material_name: m.name, material_code: m.code, unit: m.unit, current_stock: r3(m.current_stock),
      total_purchased: r3(e.qc), total_purchase_value: r2(e.vc), total_sold: r3(e.qv), total_sale_value: r2(e.vv),
      avg_cost: r2(custo), cogs: r2(e.qv * custo), cost_unreliable: false, sale_price: m.sale_price, currency: 'BRL', sale_price_currency: 'BRL',
      moedas_misturadas: false,
      total_purchase_value_by_currency: e.vc ? [{ currency: 'BRL', total: r2(e.vc) }] : [],
      total_sale_value_by_currency: e.vv ? [{ currency: 'BRL', total: r2(e.vv) }] : [],
    };
  }).sort((x, y) => String(x.material_code).localeCompare(String(y.material_code)));
};
