// delete_installment_bill_group (app 1.60.18: supabase/migrations/20261117234500_financial_installment_groups.sql): exclusão em grupo das parcelas
// pendentes de um parcelamento (single, future, all_pending). Parcela paga, parcial ou com baixa fica no histórico e volta em `skipped`.
// Devolve { deleted, skipped: [{ id, description, due_date }], installment_group_id }. T13 cap10 (o robô só cancela a janela).
import { num } from '../../lib/eco.mjs';

export default (a, { store, db, RpcError }) => {
  const ancora = store.rows('financial_bills').find((b) => b.id === a.p_bill_id);
  if (!ancora) throw new RpcError('bill_not_found');
  if (!ancora.installment_group_id) throw new RpcError('bill_has_no_installment_group');
  if (!['single', 'future', 'all_pending'].includes(a.p_scope)) throw new RpcError('invalid_installment_scope');
  const baixas = store.rows('bill_payments');
  const comBaixa = (b) => b.status !== 'pending' || num(b.paid_amount) !== 0 || baixas.some((p) => p.bill_id === b.id);
  const doGrupo = store.rows('financial_bills').filter((b) => b.company_id === ancora.company_id && b.installment_group_id === ancora.installment_group_id
    && ((a.p_scope === 'single' && b.id === ancora.id) || (a.p_scope === 'future' && b.installment_number >= ancora.installment_number) || a.p_scope === 'all_pending'));
  const skipped = doGrupo.filter(comBaixa).sort((x, y) => x.installment_number - y.installment_number)
    .map((b) => ({ id: b.id, description: b.description, due_date: b.due_date }));
  const apagar = doGrupo.filter((b) => !comBaixa(b));
  for (const b of apagar) db.remove('financial_bills', (r) => r === b);
  return { deleted: apagar.length, skipped, installment_group_id: ancora.installment_group_id };
};
