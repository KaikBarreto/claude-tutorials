// RPC get_group_branch_stock_settings (20261016210100): a matriz e as filiais ativas (matriz primeiro, filiais por nome) com a chave
// "Usar estoque de outras unidades na venda" (companies.allow_branch_stock_on_sale). Autoriza a matriz ou uma unidade ativa.
import { empresaDoUsuario, empresasDoGrupo, grupoPorId } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const g = grupoPorId(store, a._group_id);
  if (!g) throw new RpcError('Grupo de empresas nao encontrado.');
  const cid = empresaDoUsuario(store, ctx.userId);
  if (!cid) throw new RpcError('Acao nao permitida: seu usuario nao esta vinculado a nenhuma unidade.');
  const ids = empresasDoGrupo(store, a._group_id);
  if (!ids.includes(cid)) throw new RpcError('Acao nao permitida: a sua empresa nao faz parte deste grupo.');
  const comp = (id) => store.rows('companies').find((c) => c.id === id) || {};
  const matriz = { company_id: g.owner_company_id, company_name: comp(g.owner_company_id).name, is_matriz: true, allow_branch_stock_on_sale: !!comp(g.owner_company_id).allow_branch_stock_on_sale };
  const filiais = ids.filter((id) => id !== g.owner_company_id).map((id) => ({ company_id: id, company_name: comp(id).name, is_matriz: false, allow_branch_stock_on_sale: !!comp(id).allow_branch_stock_on_sale }))
    .sort((x, y) => String(x.company_name).localeCompare(String(y.company_name)));
  return [matriz, ...filiais];
};
