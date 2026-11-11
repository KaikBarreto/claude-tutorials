// reconcile_ignore_entries_batch (T14 cap11, "Ignorar (n)"): as linhas pendentes saem do cálculo do saldo (status ignored).
import { atualizar } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const ids = new Set(a.p_entry_ids || []);
  const alvo = ctx.store.rows('bank_statement_entries').filter((e) => ids.has(e.id) && e.status === 'pending' && (!a.p_import_id || e.import_id === a.p_import_id));
  for (const e of alvo) atualizar(ctx, 'bank_statement_entries', { id: e.id }, { status: 'ignored' });
  return { ignored_count: alvo.length, requested_count: ids.size };
};
