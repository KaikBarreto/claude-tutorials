// get_bank_reconciliation_state (T14): rodapé, linhas, sugestões e diferenças casadas (lib/conciliacao.mjs, a fórmula da função SQL).
import { estado, extrato } from '../../lib/conciliacao.mjs';

export default (a, ctx) => estado(ctx.store, extrato(ctx, a.p_import_id));
