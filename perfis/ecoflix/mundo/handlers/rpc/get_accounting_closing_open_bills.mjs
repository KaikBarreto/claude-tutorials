// get_accounting_closing_open_bills(p_company_id, p_end_date, p_limit, p_offset): contas em aberto na data de corte (pacote "Fechamento completo (Excel)", T15 cap15).
import { num, r2 } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  const cats = new Map(store.rows('financial_categories').map((c) => [c.id, c.name]));
  const todas = store.rows('financial_bills').filter((b) => b.company_id === ctx.companyId && ['pending', 'partial'].includes(b.status) && String(b.created_at || b.due_date || '').slice(0, 10) <= a.p_end_date);
  const pag = todas.slice(num(a.p_offset), num(a.p_offset) + (num(a.p_limit) || 1000));
  return pag.map((b) => ({
    bill_id: b.id, direction: b.direction, description: b.description, recognition_date: String(b.created_at || b.due_date).slice(0, 10), due_date: b.due_date,
    amount: num(b.amount), paid_at_cutoff: num(b.paid_amount), remaining_at_cutoff: r2(num(b.amount) - num(b.paid_amount)), status_at_cutoff: b.status,
    last_payment_date: null, payment_methods: null, installment_number: b.installment_number ?? null, installment_total: b.installment_total ?? null,
    partner_name: null, partner_document: null, category_name: cats.get(b.category_id) || null, cost_center_name: null, order_reference: null, invoices: [],
    total_count: todas.length,
  }));
};
