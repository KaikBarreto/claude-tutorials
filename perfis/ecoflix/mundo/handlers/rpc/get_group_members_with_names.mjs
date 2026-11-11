// RPC get_group_members_with_names (20260405120000): só a dona; os membros ATIVOS com o nome da empresa.
import { exigeDono, nomeEmpresa } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  exigeDono(ctx, a._group_id);
  return ctx.store.rows('company_group_members').filter((m) => m.group_id === a._group_id && m.status === 'active')
    .map((m) => ({ id: m.id, group_id: m.group_id, company_id: m.company_id, joined_at: m.joined_at, status: m.status, company_name: nomeEmpresa(ctx.store, m.company_id) }));
};
