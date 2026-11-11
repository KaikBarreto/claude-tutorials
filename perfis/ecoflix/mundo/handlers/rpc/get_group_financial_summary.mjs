// RPC get_group_financial_summary (20261011202500): uma linha por empresa do grupo com vendas, compras e as receitas/despesas de caixa e de
// banco pelos critérios da DRE (filtros de descrição verbatim, lib/grupo.mjs). O Dashboard Gerencial soma estas linhas: nenhum total escrito.
import { exigeDono, empresasDoGrupo, resumoFinanceiro } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  exigeDono(ctx, a._group_id);
  const d1 = String(a._start_date).slice(0, 10);
  const d2 = String(a._end_date).slice(0, 10);
  return empresasDoGrupo(ctx.store, a._group_id).map((cid) => resumoFinanceiro(ctx.store, cid, d1, d2));
};
