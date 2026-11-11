// cancel_bank_reconciliation (T14 cap13 só abre a janela e mantém): desfaz todas as linhas e marca o extrato como cancelado.
import { atualizar } from '../../lib/eco.mjs';
import { extrato, linhasDo, casamentosDa, desfazer, agoraIso } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const imp = extrato(ctx, a.p_import_id);
  if (imp.status !== 'open') throw new ctx.RpcError('Só uma conciliação em aberto pode ser cancelada.');
  const es = linhasDo(ctx.store, imp.id);
  const r = { import_id: imp.id, total_entries: es.length, ignored_entries: 0, existing_links_removed: 0, created_transactions: 0, bills_reopened: 0,
    employee_movements: 0, partner_balance_payments: 0, account_moves_restored: 0 };
  for (const e of es) {
    if (e.status === 'ignored') { r.ignored_entries++; atualizar(ctx, 'bank_statement_entries', { id: e.id }, { status: 'pending' }); continue; }
    if (e.status !== 'matched' || !casamentosDa(ctx.store, e.id).length) continue;
    for (const m of desfazer(ctx, e)) {
      if (m.match_type === 'existing') r.existing_links_removed++;
      if (m.match_type === 'created') r.created_transactions++;
      if (m.match_type === 'bill_settlement') r.bills_reopened++;
    }
  }
  atualizar(ctx, 'bank_statement_imports', { id: imp.id }, { status: 'cancelled', cancelled_at: agoraIso(), cancelled_by: ctx.userId });
  return r;
};
