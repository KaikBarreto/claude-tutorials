// RPC link_own_material_to_group_catalog (T22, 1.60.18): liga o material da empresa do usuário ao catálogo do grupo (cria o item no catálogo se
// não houver um de mesmo nome) e devolve o id do item do grupo. Usada pela venda (estoque de outra unidade) e pela transferência da filial.
import { exigeMembro } from '../../lib/grupo.mjs';
import { agora } from '../../lib/grupo.mjs';
const k = (s) => String(s ?? '').trim().toLowerCase();
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const cid = exigeMembro(ctx, a._group_id);
  const m = store.rows('materials').find((x) => x.id === a._material_id && x.company_id === cid);
  if (!m) throw new RpcError('Material not found');
  const ex = store.rows('material_group_links').find((l) => l.company_material_id === m.id);
  if (ex) return ex.group_material_id;
  const iso = new Date(agora()).toISOString();
  let gm = store.rows('group_materials').find((x) => x.group_id === a._group_id && k(x.name) === k(m.name));
  if (!gm) gm = db.insert('group_materials', { group_id: a._group_id, name: m.name, unit: m.unit || 'KG', code: m.code ?? null, ncm: m.ncm ?? null, created_at: iso, updated_at: iso });
  db.insert('material_group_links', { company_material_id: m.id, group_material_id: gm.id, company_id: cid, created_at: iso });
  return gm.id;
};
