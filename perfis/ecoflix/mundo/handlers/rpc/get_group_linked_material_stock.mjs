// RPC get_group_linked_material_stock: o saldo (materials.current_stock) de cada material VINCULADO ao catálogo do grupo, por unidade (o que a
// transferência debita). Dona ou unidade ativa. Ordem: material do grupo e empresa.
import { exigeMembro, empresasDoGrupo, nomeEmpresa } from '../../lib/grupo.mjs';
import { num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  exigeMembro(ctx, a._group_id);
  const ids = empresasDoGrupo(store, a._group_id);
  const gms = new Map(store.rows('group_materials').filter((g) => g.group_id === a._group_id).map((g) => [g.id, g]));
  const out = [];
  for (const l of store.rows('material_group_links')) {
    const gm = gms.get(l.group_material_id);
    const m = store.rows('materials').find((x) => x.id === l.company_material_id);
    if (!gm || !m || !ids.includes(m.company_id) || m.is_archived) continue;
    out.push({ group_material_id: gm.id, company_id: m.company_id, company_name: nomeEmpresa(store, m.company_id), material_id: m.id, material_name: m.name,
      current_stock: num(m.current_stock), unit: m.unit || 'kg', _o: gm.name });
  }
  return out.sort((x, y) => String(x._o).localeCompare(String(y._o)) || String(x.company_name).localeCompare(String(y.company_name))).map(({ _o, ...r }) => r);
};
