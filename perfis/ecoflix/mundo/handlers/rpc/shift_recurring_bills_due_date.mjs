// shift_recurring_bills_due_date (app 1.59.154: supabase/migrations/20260630121000_shift_recurring_bills_due_date_rpc.sql): no "Esta e as
// futuras" com vencimento novo, desloca pelo mesmo número de dias as contas da recorrência com vencimento >= o da conta editada e ainda não
// pagas, e o next_due_date do molde (se >= essa data). O resto do "Esta e as futuras" (descrição, valor, categoria) o app grava direto
// por REST (hooks/useBills.ts). T13 cap08.
const dias = (a, b) => Math.round((Date.parse(`${b}T00:00:00Z`) - Date.parse(`${a}T00:00:00Z`)) / 86400000);
const mais = (d, n) => new Date(Date.parse(`${d}T00:00:00Z`) + n * 86400000).toISOString().slice(0, 10);

export default (a, { store, db, RpcError }) => {
  const delta = dias(a.p_from_due_date, a.p_new_due_date);
  if (!delta) return null;
  const t = store.rows('recurring_bill_templates').find((x) => x.id === a.p_template_id);
  if (!t) throw new RpcError(`Template de recorrência não encontrado (id ${a.p_template_id}).`);
  for (const b of store.rows('financial_bills')) {
    if (b.recurring_template_id !== t.id || !b.due_date || b.due_date < a.p_from_due_date || b.status === 'paid') continue;
    db.update('financial_bills', (r) => r === b, { due_date: mais(b.due_date, delta) });
  }
  if (t.next_due_date && t.next_due_date >= a.p_from_due_date) db.update('recurring_bill_templates', { id: t.id }, { next_due_date: mais(t.next_due_date, delta) });
  return null;
};
