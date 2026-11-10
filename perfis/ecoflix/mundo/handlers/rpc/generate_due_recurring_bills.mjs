// Gera as contas das recorrências vencidas (até hoje): cria o título do vencimento e avança next_due_date. Devolve
// quantas criou. No mundo base as recorrências já estão em dia (próximo vencimento em dezembro).
import { hojeBR, addDias } from '../../lib/eco.mjs';
const avanca = (d, freq, n = 1) => {
  if (freq === 'weekly') return addDias(d, 7 * n);
  if (freq === 'daily') return addDias(d, n);
  const [y, m, dd] = d.split('-').map(Number);
  const meses = freq === 'yearly' ? 12 * n : freq === 'quarterly' ? 3 * n : n;
  const t = new Date(Date.UTC(y, m - 1 + meses, dd));
  return t.toISOString().slice(0, 10);
};
export default (a, { store, db, companyId }) => {
  const hoje = hojeBR();
  let n = 0;
  for (const t of store.rows('recurring_bill_templates')) {
    if (t.company_id !== companyId || !t.is_active) continue;
    while (t.next_due_date && t.next_due_date <= hoje && (!t.end_date || t.next_due_date <= t.end_date)) {
      db.insert('financial_bills', {
        company_id: t.company_id, direction: t.direction, description: t.description, amount: t.amount, currency: 'BRL', due_date: t.next_due_date,
        status: 'pending', paid_amount: 0, category_id: t.category_id, partner_id: t.partner_id, partner_type: t.partner_type,
        expected_bank_account_id: t.expected_bank_account_id, expected_payment_method: t.expected_payment_method, recurring_template_id: t.id, source_type: 'recurring',
      }, { companyId });
      t.next_due_date = avanca(t.next_due_date, t.frequency, t.interval || 1);
      n++;
    }
  }
  return n;
};
