// RPC import_company_categories_to_group (20260315220327): as categorias financeiras de TODAS as empresas do grupo que ainda não estão no
// grupo (uma por nome e tipo, a mais antiga) entram em group_financial_categories. Devolve quantas.
import { exigeDono, empresasDoGrupo, agora } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  const { store, db } = ctx;
  exigeDono(ctx, a._group_id);
  const cids = empresasDoGrupo(store, a._group_id);
  const chave = (c) => `${String(c.name).trim().toLowerCase()}|${c.type}`;
  const ja = new Set(store.rows('group_financial_categories').filter((c) => c.group_id === a._group_id).map(chave));
  const iso = new Date(agora()).toISOString();
  let n = 0;
  const lista = store.rows('financial_categories').filter((c) => cids.includes(c.company_id))
    .sort((x, y) => chave(x).localeCompare(chave(y)) || String(x.created_at).localeCompare(String(y.created_at)));
  for (const c of lista) {
    const k = chave(c);
    if (ja.has(k)) continue;
    ja.add(k);
    db.insert('group_financial_categories', { group_id: a._group_id, name: c.name, type: c.type, color: c.color ?? null, is_system: false, created_at: iso, updated_at: iso });
    n += 1;
  }
  return n;
};
