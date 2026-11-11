// RPC get_group_inventory_report_data (20261011202500): por empresa e material canônico, o saldo do cadastro (materials.current_stock) e as
// compras (quantidade líquida e valor) e vendas do intervalo (instante do pedido > fim da véspera do início e <= fim do último dia, BRT).
// Autoriza qualquer unidade do grupo. A Visão Geral chama com início = fim (só o cadastro) e o Relatório de Estoque com o período.
import { empresaDoUsuario, empresasDoGrupo, canonicos, nomeEmpresa, diaDoInstante, fimDoDia, vespera } from '../../lib/grupo.mjs';
import { num, r2, r3 } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  const membros = empresasDoGrupo(store, a._group_id);
  if (!membros.length) return [];
  if (!membros.includes(empresaDoUsuario(store, ctx.userId))) throw new ctx.RpcError('Access denied', '42501', 403);
  const alvo = Array.isArray(a._company_ids) && a._company_ids.length ? membros.filter((c) => a._company_ids.includes(c)) : membros;
  const usuarios = Array.isArray(a._user_ids) && a._user_ids.length ? new Set(a._user_ids) : null;
  const abre = fimDoDia(vespera(diaDoInstante(a._start_date)));
  const fecha = fimDoDia(diaDoInstante(a._end_date));
  const can = canonicos(store, a._group_id, alvo);
  const dentro = (p) => { const t = new Date(p.transaction_at || p.created_at).getTime(); return t > abre && t <= fecha && p.status === 'completed' && alvo.includes(p.company_id) && (!usuarios || usuarios.has(p.created_by)); };
  const agg = (pedidosTab, itensTab, chave, liquida) => {
    const ped = new Set(store.rows(pedidosTab).filter(dentro).map((p) => p.id));
    const m = new Map();
    for (const it of store.rows(itensTab)) {
      if (!ped.has(it[chave])) continue;
      const e = m.get(it.material_id) || { q: 0, v: 0 };
      e.q += num(it.quantity) - (liquida ? num(it.impurity) : 0);
      e.v += num(it.total_price);
      m.set(it.material_id, e);
    }
    return m;
  };
  const comp = agg('purchases', 'purchase_items', 'purchase_id', true);
  const vend = agg('sales', 'sale_items', 'sale_id', false);
  const cel = new Map();
  for (const m of store.rows('materials')) {
    const k = can.get(m.id);
    if (!k) continue;
    const chave = `${m.company_id}|${k.id}`;
    const e = cel.get(chave) || { cid: m.company_id, k, est: 0, qc: 0, vc: 0, qv: 0, vv: 0 };
    e.est += num(m.current_stock);
    const c = comp.get(m.id); if (c) { e.qc += c.q; e.vc += c.v; }
    const v = vend.get(m.id); if (v) { e.qv += v.q; e.vv += v.v; }
    cel.set(chave, e);
  }
  return [...cel.values()].map((e) => ({
    company_id: e.cid, company_name: nomeEmpresa(store, e.cid), material_id: e.k.id, material_name: e.k.name, material_code: e.k.code, material_unit: e.k.unit,
    current_stock: r3(e.est), total_purchased: r3(e.qc), total_purchase_value: r2(e.vc), total_sold: r3(e.qv), total_sale_value: r2(e.vv), currency: 'BRL',
    sale_price_currency: 'BRL', moedas_misturadas: false, total_purchase_value_by_currency: e.vc ? [{ currency: 'BRL', total: r2(e.vc) }] : [],
    total_sale_value_by_currency: e.vv ? [{ currency: 'BRL', total: r2(e.vv) }] : [],
  }));
};
