// RPC get_group_stock_summary (20261011202500): por empresa e material CANÔNICO (vínculo do grupo -> nome no catálogo -> o próprio), o saldo
// = Σ stock_movements (não o cadastro), o custo médio = Σ valor / Σ quantidade líquida de TODAS as compras concluídas do material e
// stock_value = saldo × custo médio. Só linhas com saldo diferente de zero, por empresa e nome.
import { exigeDono, empresasDoGrupo, canonicos, nomeEmpresa } from '../../lib/grupo.mjs';
import { num, r3 } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  exigeDono(ctx, a._group_id);
  const cids = empresasDoGrupo(store, a._group_id);
  const can = canonicos(store, a._group_id, cids);
  const saldo = new Map();
  for (const s of store.rows('stock_movements')) if (can.has(s.material_id)) saldo.set(s.material_id, (saldo.get(s.material_id) || 0) + num(s.quantity));
  const compras = new Map(store.rows('purchases').filter((p) => cids.includes(p.company_id) && p.status === 'completed').map((p) => [p.id, p]));
  const custo = new Map();
  for (const it of store.rows('purchase_items')) {
    const p = compras.get(it.purchase_id);
    if (!p || !can.has(it.material_id)) continue;
    const c = custo.get(it.material_id) || { v: 0, q: 0 };
    c.v += num(it.total_price);
    c.q += num(it.quantity) - num(it.impurity);
    custo.set(it.material_id, c);
  }
  const celulas = new Map();
  for (const m of store.rows('materials')) {
    const k = can.get(m.id);
    if (!k) continue;
    const chave = `${m.company_id}|${k.id}`;
    const e = celulas.get(chave) || { company_id: m.company_id, k, saldo: 0, v: 0, q: 0, sale: 0, ids: [] };
    e.saldo += saldo.get(m.id) || 0;
    const c = custo.get(m.id);
    if (c) { e.v += c.v; e.q += c.q; }
    e.sale = Math.max(e.sale, num(m.sale_price));
    e.ids.push(m.id);
    celulas.set(chave, e);
  }
  return [...celulas.values()].filter((e) => Math.abs(e.saldo) > 1e-9).map((e) => ({
    company_id: e.company_id, company_name: nomeEmpresa(store, e.company_id), material_name: e.k.name, material_unit: e.k.unit, current_stock: r3(e.saldo),
    sale_price: e.sale, stock_value: e.saldo * (e.q ? e.v / e.q : 0), material_ids: e.ids, currency: 'BRL', sale_price_currency: 'BRL', moedas_misturadas: false,
  })).sort((x, y) => String(x.company_name).localeCompare(String(y.company_name)) || String(x.material_name).localeCompare(String(y.material_name)));
};
