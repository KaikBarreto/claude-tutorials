// update_installment_bill_group (app 1.60.18: supabase/migrations/20261117234500_financial_installment_groups.sql): edição em grupo das parcelas de um
// parcelamento feito na tela ("Esta e as próximas", "Todas as parcelas pendentes", "Só esta conta"). Escopos: single (só a âncora), future
// (pendentes sem baixa com número >= o da âncora), all_pending (todas as pendentes sem baixa). A descrição vira "<base> (parcela i/N)"; o vencimento
// desloca cada parcela do escopo pelo mesmo número de dias entre a data nova e a da âncora; valor, categoria, parceiro, observação, centro de custo,
// forma e conta previstas valem para todas as do escopo. Devolve { updated, installment_group_id }. T13 cap10.
import { r2, num } from '../../lib/eco.mjs';

const dias = (a, b) => Math.round((Date.parse(`${b}T00:00:00Z`) - Date.parse(`${a}T00:00:00Z`)) / 86400000);
const mais = (d, n) => new Date(Date.parse(`${d}T00:00:00Z`) + n * 86400000).toISOString().slice(0, 10);

export default (a, { store, db, RpcError }) => {
  const ancora = store.rows('financial_bills').find((b) => b.id === a.p_bill_id);
  if (!ancora) throw new RpcError('bill_not_found');
  if (!ancora.installment_group_id) throw new RpcError('bill_has_no_installment_group');
  if (!['single', 'future', 'all_pending'].includes(a.p_scope)) throw new RpcError('invalid_installment_scope');
  if (a.p_amount != null && !(num(a.p_amount) > 0)) throw new RpcError('invalid_installment_amount');
  const base = String(a.p_description ?? ancora.description).trim().replace(/\s*\(parcela\s+\d+\/\d+\)\s*$/i, '');
  const delta = a.p_due_date && ancora.due_date ? dias(ancora.due_date, a.p_due_date) : 0;
  const semBaixa = (b) => b.status === 'pending' && num(b.paid_amount) === 0;
  let n = 0;
  for (const b of store.rows('financial_bills')) {
    if (b.company_id !== ancora.company_id || b.installment_group_id !== ancora.installment_group_id) continue;
    const noEscopo = (a.p_scope === 'single' && b.id === ancora.id)
      || (a.p_scope === 'future' && semBaixa(b) && b.installment_number >= ancora.installment_number)
      || (a.p_scope === 'all_pending' && semBaixa(b));
    if (!noEscopo) continue;
    db.update('financial_bills', (r) => r === b, {
      direction: a.p_direction ?? b.direction, description: `${base} (parcela ${b.installment_number}/${b.installment_total})`,
      amount: semBaixa(b) && a.p_amount != null ? r2(a.p_amount) : b.amount,
      due_date: semBaixa(b) && a.p_due_date ? (b.due_date ? mais(b.due_date, delta) : a.p_due_date) : b.due_date,
      category_id: a.p_category_id ?? null, partner_type: a.p_partner_type ?? null, partner_id: a.p_partner_id ?? null,
      notes: a.p_notes ? String(a.p_notes).trim() || null : null, cost_center_id: a.p_cost_center_id ?? null,
      expected_payment_method: a.p_expected_payment_method ?? null, expected_bank_account_id: a.p_expected_bank_account_id ?? null,
    });
    n++;
  }
  return { updated: n, installment_group_id: ancora.installment_group_id };
};
