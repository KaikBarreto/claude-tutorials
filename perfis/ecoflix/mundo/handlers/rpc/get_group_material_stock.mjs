// RPC get_group_material_stock (T22, 1.60.18): o saldo de um material do catálogo do grupo em CADA unidade que o tem vinculado (o "Outras unidades"
// da janela "Estoque insuficiente" da venda). Só quem é do grupo; materiais ativos ligados por material_group_links.
import { exigeMembro, empresasDoGrupo, nomeEmpresa } from '../../lib/grupo.mjs';
import { num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  exigeMembro(ctx, a._group_id);
  const cids = empresasDoGrupo(store, a._group_id);
  const links = store.rows('material_group_links').filter((l) => l.group_material_id === a._group_material_id && cids.includes(l.company_id));
  const out = [];
  for (const l of links) {
    const m = store.rows('materials').find((x) => x.id === l.company_material_id);
    if (!m || m.is_archived) continue;
    out.push({ company_id: l.company_id, company_name: nomeEmpresa(store, l.company_id), current_stock: num(m.current_stock), material_id: m.id, material_name: m.name, unit: m.unit || 'KG' });
  }
  return out.sort((x, y) => String(x.company_name).localeCompare(String(y.company_name)));
};
