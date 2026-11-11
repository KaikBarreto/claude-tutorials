// RPC get_group_destinations_for_member: as empresas do grupo (dona e membros ativos) por nome, para Origem/Destino da transferência.
import { exigeMembro, empresasDoGrupo, nomeEmpresa } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  exigeMembro(ctx, a._group_id);
  return empresasDoGrupo(ctx.store, a._group_id).map((id) => ({ company_id: id, company_name: nomeEmpresa(ctx.store, id) }))
    .sort((x, y) => String(x.company_name).localeCompare(String(y.company_name)));
};
