// RPC import_owner_price_table_to_group (20260320015543): os preços de uma tabela da matriz (a indicada ou a padrão) entram na tabela do grupo,
// material a material (vínculo da matriz ou nome no catálogo), com upsert por (tabela, material do grupo). Devolve quantos itens.
import { exigeDono, agora } from '../../lib/grupo.mjs';
import { num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const g = exigeDono(ctx, a._group_id);
  const fonte = a._source_price_table_id
    ? store.rows('price_tables').find((t) => t.id === a._source_price_table_id && t.company_id === g.owner_company_id)
    : store.rows('price_tables').find((t) => t.company_id === g.owner_company_id && t.is_default);
  if (!fonte) throw new RpcError('Tabela de preço da matriz não encontrada');
  const iso = new Date(agora()).toISOString();
  let n = 0;
  for (const m of store.rows('materials').filter((x) => x.company_id === g.owner_company_id && !x.is_archived)) {
    const pti = store.rows('price_table_items').find((i) => i.price_table_id === fonte.id && i.material_id === m.id);
    const compra = num(pti?.purchase_price ?? m.purchase_price ?? 0);
    const venda = num(pti?.sale_price ?? m.sale_price ?? 0);
    const link = store.rows('material_group_links').find((l) => l.company_material_id === m.id && l.company_id === g.owner_company_id);
    const gm = (link && store.rows('group_materials').find((x) => x.id === link.group_material_id))
      || store.rows('group_materials').find((x) => x.group_id === g.id && String(x.name).trim().toLowerCase() === String(m.name).trim().toLowerCase());
    if (!gm) continue;
    const ex = store.rows('group_price_table_items').find((i) => i.group_price_table_id === a._group_price_table_id && i.group_material_id === gm.id);
    if (ex) Object.assign(ex, { purchase_price: compra, sale_price: venda, updated_at: iso });
    else db.insert('group_price_table_items', { group_price_table_id: a._group_price_table_id, group_material_id: gm.id, purchase_price: compra, sale_price: venda, created_at: iso, updated_at: iso });
    n += 1;
  }
  store.table('group_price_table_items').touch();
  return n;
};
