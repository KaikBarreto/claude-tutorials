// RPC import_owner_materials_to_group (20260320014424) + o gatilho trg_autolink_owner_on_group_material (20260727181000): copia para o catálogo
// do grupo os materiais ativos da matriz que ainda não estão lá (um por nome; nome, unidade, NCM e código) e vincula cada material da matriz
// ao item do catálogo de mesmo nome. Devolve quantos entraram ("n material(is) importado(s) do estoque").
import { exigeDono, agora } from '../../lib/grupo.mjs';
export function autolinkMatriz(store, db, gid) {
  const g = store.rows('company_groups').find((x) => x.id === gid);
  if (!g) return 0;
  let n = 0;
  const links = store.rows('material_group_links');
  for (const gm of store.rows('group_materials').filter((x) => x.group_id === gid)) {
    if (links.some((l) => l.group_material_id === gm.id && l.company_id === g.owner_company_id)) continue;
    const m = store.rows('materials').find((x) => x.company_id === g.owner_company_id && !x.is_archived && String(x.name).trim().toLowerCase() === String(gm.name).trim().toLowerCase()
      && !links.some((l) => l.company_material_id === x.id));
    if (!m) continue;
    db.insert('material_group_links', { group_material_id: gm.id, company_material_id: m.id, company_id: m.company_id, created_at: new Date(agora()).toISOString() });
    n += 1;
  }
  return n;
}
export default (a, ctx) => {
  const { store, db } = ctx;
  const g = exigeDono(ctx, a._group_id);
  const ja = new Set(store.rows('group_materials').filter((x) => x.group_id === g.id).map((x) => String(x.name).trim().toLowerCase()));
  const vistos = new Set();
  const lista = store.rows('materials').filter((m) => m.company_id === g.owner_company_id && !m.is_archived)
    .sort((x, y) => String(x.name).trim().toLowerCase().localeCompare(String(y.name).trim().toLowerCase()) || String(x.created_at).localeCompare(String(y.created_at)));
  let n = 0;
  const iso = new Date(agora()).toISOString();
  for (const m of lista) {
    const k = String(m.name).trim().toLowerCase();
    if (ja.has(k) || vistos.has(k)) continue;
    vistos.add(k);
    db.insert('group_materials', { group_id: g.id, name: m.name, unit: m.unit, ncm: m.ncm ?? null, code: m.code ?? null, created_at: iso, updated_at: iso });
    n += 1;
  }
  autolinkMatriz(store, db, g.id);
  return n;
};
