// reconcile_find_distant_exact_candidates (T14): para cada linha pendente, os lançamentos de valor exato da conta, livres, fora da janela de 3 dias.
import { linhasDo, distantes, extrato } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const imp = extrato(ctx, a.p_import_id);
  const T = (x) => new Date(x).getTime();
  return linhasDo(ctx.store, imp.id).filter((e) => e.status === 'pending').sort((x, y) => T(x.posted_at) - T(y.posted_at) || String(x.id).localeCompare(String(y.id)))
    .map((e) => ({ entry_id: e.id, ...distantes(ctx.store, e) })).filter((r) => r.candidate_count > 0);
};
