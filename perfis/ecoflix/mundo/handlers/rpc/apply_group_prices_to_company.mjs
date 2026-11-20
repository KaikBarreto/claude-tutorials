// RPC apply_group_prices_to_company (20260315220327), o "Aplicar" da Vinculação por Unidade: só a dona; a unidade tem de estar vinculada à tabela
// do grupo (company_group_price_links.is_linked); para cada item da tabela com material ligado na unidade, grava na tabela PRINCIPAL da unidade o
// preço do grupo com a variação (percentual ou R$ fixo, acima ou abaixo) na compra E na venda, e no cadastro do material. Devolve quantos preços aplicou.
import { grupoPorId, empresasDoGrupo } from '../../lib/grupo.mjs';
import { agora } from '../../lib/grupo.mjs';
import { exigeDono } from '../../lib/grupo.mjs';
import { num, r2 } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const tab = store.rows('group_price_tables').find((t) => t.id === a._group_price_table_id);
  if (!tab) throw new RpcError('Access denied', '42501', 403);
  const g = exigeDono(ctx, tab.group_id);
  if (!empresasDoGrupo(store, g.id).includes(a._company_id)) throw new RpcError('Company not in group');
  const link = store.rows('company_group_price_links').find((l) => l.group_price_table_id === tab.id && l.company_id === a._company_id);
  if (!link || link.is_linked === false) return 0;
  const principal = store.rows('price_tables').find((t) => t.company_id === a._company_id && t.is_default);
  if (!principal) return 0;
  const sinal = link.variation_direction === 'negative' ? -1 : 1;
  const v = num(link.variation_amount);
  const calc = (p) => r2(link.variation_type === 'percentage' ? num(p) * (1 + sinal * v / 100) : num(p) + sinal * v);
  const iso = new Date(agora()).toISOString();
  let n = 0;
  for (const it of store.rows('group_price_table_items').filter((i) => i.group_price_table_id === tab.id)) {
    const l = store.rows('material_group_links').find((x) => x.group_material_id === it.group_material_id && x.company_id === a._company_id);
    const m = l && store.rows('materials').find((x) => x.id === l.company_material_id);
    if (!m) continue;
    const pc = calc(it.purchase_price), pv = calc(it.sale_price);
    const ex = store.rows('price_table_items').find((i) => i.price_table_id === principal.id && i.material_id === m.id);
    if (ex) Object.assign(ex, { purchase_price: pc, sale_price: pv, updated_at: iso });
    else db.insert('price_table_items', { price_table_id: principal.id, material_id: m.id, purchase_price: pc, sale_price: pv, is_override: false, created_at: iso, updated_at: iso });
    m.purchase_price = pc; m.sale_price = pv; m.updated_at = iso;
    n += 1;
  }
  store.table('price_table_items').touch();
  store.table('materials').touch();
  return n;
};
