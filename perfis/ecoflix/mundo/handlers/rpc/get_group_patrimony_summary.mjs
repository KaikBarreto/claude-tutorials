// RPC get_group_patrimony_summary (20260315235425): o patrimônio de cada empresa do grupo (o mesmo get_company_patrimony da unidade).
import { empresasDoGrupo, nomeEmpresa } from '../../lib/grupo.mjs';
import patrimonio from './get_company_patrimony.mjs';
export default (a, ctx) => empresasDoGrupo(ctx.store, a._group_id).map((cid) => {
  const p = patrimonio({ p_company_id: cid }, ctx);
  return { company_id: cid, company_name: nomeEmpresa(ctx.store, cid), cash_balance: p.cashBalance, bank_balance: p.bankBalance, receivables: p.receivables,
    payables: p.payables, stock_value: p.stockValue };
});
