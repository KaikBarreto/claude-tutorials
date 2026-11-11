// RPC get_group_stock_balance_at_date (20261011202500): a Posição de Estoque do grupo numa data: por empresa, o saldo e o custo médio de cada
// material no instante (a mesma conta da _stock_balance_at_date_unchecked). Autoriza qualquer unidade do grupo.
import { empresaDoUsuario, empresasDoGrupo, nomeEmpresa, saldoNaData } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  if (!a._at) throw new ctx.RpcError('_at é obrigatório');
  const membros = empresasDoGrupo(store, a._group_id);
  if (!membros.length) return [];
  if (!membros.includes(empresaDoUsuario(store, ctx.userId))) throw new ctx.RpcError('Access denied', '42501', 403);
  const alvo = Array.isArray(a._company_ids) && a._company_ids.length ? membros.filter((c) => a._company_ids.includes(c)) : membros;
  const t = new Date(a._at).getTime();
  const out = [];
  for (const cid of alvo) {
    for (const l of saldoNaData(store, cid, t)) {
      out.push({ company_id: cid, company_name: nomeEmpresa(store, cid), material_id: l.material_id, code: l.code, name: l.name, unit: l.unit, saldo: l.saldo,
        avg_cost: l.avg_cost, sale_price: l.sale_price, currency: 'BRL', sale_price_currency: 'BRL', moedas_misturadas: false });
    }
  }
  return out;
};
