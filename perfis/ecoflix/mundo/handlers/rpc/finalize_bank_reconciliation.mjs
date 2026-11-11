// finalize_bank_reconciliation (T14 cap14): só com nenhuma linha pendente e diferença zero; o extrato fica somente leitura.
import { atualizar } from '../../lib/eco.mjs';
import { extrato, estado } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const imp = extrato(ctx, a.p_import_id);
  if (imp.status === 'finalized') throw new ctx.RpcError('Este extrato ja foi finalizado.');
  if (imp.status === 'cancelled') throw new ctx.RpcError('Esta conciliacao foi cancelada e nao pode ser finalizada.');
  const st = estado(ctx.store, imp);
  if (st.pending_count > 0 || Math.abs(st.difference) > 0.01) throw new ctx.RpcError('reconciliacao_incompleta');
  atualizar(ctx, 'bank_statement_imports', { id: imp.id }, { status: 'finalized' });
  return null;
};
