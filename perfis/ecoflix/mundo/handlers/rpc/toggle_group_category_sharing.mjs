// RPC toggle_group_category_sharing (T22, 1.60.18), o marcar/desmarcar da aba "Categorias Financeiras" do grupo: só a dona; a categoria é da MATRIZ.
// Já compartilhada (mesmo nome e tipo em group_financial_categories) = desmarca e devolve false; senão marca e devolve true. As obrigatórias do DRE
// (Ganhos, Prejuízos, Impostos) o app nem deixa clicar.
import { exigeDono, agora } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const g = exigeDono(ctx, a._group_id);
  const c = store.rows('financial_categories').find((x) => x.id === a._category_id && x.company_id === g.owner_company_id);
  if (!c) throw new RpcError('Category not found');
  const ja = store.rows('group_financial_categories').find((x) => x.group_id === g.id && x.name === c.name && x.type === c.type);
  if (ja) {
    db.remove('group_financial_categories', { id: ja.id });
    return false;
  }
  const iso = new Date(agora()).toISOString();
  db.insert('group_financial_categories', { group_id: g.id, name: c.name, type: c.type, color: c.color ?? null, is_system: false, created_at: iso, updated_at: iso });
  return true;
};
