// reconcile_unmatch_entry (T14 cap13, "Desfazer"): devolve a linha (ou o grupo) para pendente; Criada apaga o lançamento, Baixada estorna a baixa.
import { atualizar } from '../../lib/eco.mjs';
import { linha, desfazer } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const e = linha(ctx, a.p_entry_id);
  const imp = ctx.store.rows('bank_statement_imports').find((i) => i.id === e.import_id);
  if (imp && imp.status !== 'open') throw new ctx.RpcError('Este extrato ja foi finalizado.');
  if (e.status === 'ignored') { atualizar(ctx, 'bank_statement_entries', { id: e.id }, { status: 'pending' }); return null; }
  if (e.status !== 'matched') throw new ctx.RpcError('Esta linha não está conciliada.');
  desfazer(ctx, e);
  return null;
};
