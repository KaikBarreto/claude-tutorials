// RPC set_allow_branch_stock_on_sale (20261016210100), as chaves de "Usar estoque de outras unidades na venda" (Configurações do grupo ›
// Transferências): a dona do grupo mexe em qualquer unidade; a filial só na dela. Grava companies.allow_branch_stock_on_sale.
import { empresaDoUsuario, empresasDoGrupo } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const meu = empresaDoUsuario(store, ctx.userId);
  const alvo = store.rows('companies').find((c) => c.id === a._company_id);
  if (!meu || !alvo) throw new RpcError('Acao nao permitida');
  const grupo = store.rows('company_groups').find((g) => empresasDoGrupo(store, g.id).includes(alvo.id));
  const dona = grupo && grupo.owner_company_id === meu;
  if (!(dona || meu === alvo.id)) throw new RpcError('Acao nao permitida: apenas a matriz ou a propria unidade pode alterar esta regra.');
  alvo.allow_branch_stock_on_sale = !!a._enabled;
  store.table('companies').touch();
  return null;
};
