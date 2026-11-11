// reconcile_unignore_entries_batch (T14): linhas ignoradas voltam a pendentes.
import { atualizar } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const ids = new Set(a.p_entry_ids || []);
  const alvo = ctx.store.rows('bank_statement_entries').filter((e) => ids.has(e.id) && e.status === 'ignored');
  for (const e of alvo) atualizar(ctx, 'bank_statement_entries', { id: e.id }, { status: 'pending' });
  return { restored_count: alvo.length, requested_count: ids.size };
};
