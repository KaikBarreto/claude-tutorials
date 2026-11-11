// RPC get_group_financial_categories (20261106143500): as categorias financeiras das empresas do grupo (ou das pedidas), para o filtro do
// Histórico e os ícones da DRE do Financeiro Gerencial.
import { escopo } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  if (!a.p_group_id) throw new ctx.RpcError('Grupo obrigatorio');
  const cids = escopo(ctx, a.p_group_id, a.p_company_ids);
  const lista = ctx.store.rows('financial_categories').filter((c) => cids.includes(c.company_id))
    .sort((x, y) => String(x.name).localeCompare(String(y.name)))
    .map((c) => ({ id: c.id, name: c.name, type: c.type, color: c.color, icon: c.icon ?? null }));
  const off = Number(a.p_offset) || 0;
  return lista.slice(off, off + (Number(a.p_limit) || 1000));
};
