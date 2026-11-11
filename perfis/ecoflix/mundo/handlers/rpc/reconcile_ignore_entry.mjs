// reconcile_ignore_entry (T14): uma linha pendente vira ignorada.
import { atualizar } from '../../lib/eco.mjs';
import { linha, pendente } from '../../lib/conciliacao.mjs';

export default (a, ctx) => { const e = linha(ctx, a.p_entry_id); pendente(ctx, e); atualizar(ctx, 'bank_statement_entries', { id: e.id }, { status: 'ignored' }); return null; };
