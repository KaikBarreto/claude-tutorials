// get_financial_accounting_report(p_company_id, p_start_date, p_end_date, p_limit, p_offset): lançamentos do período para o pacote "Fechamento completo (Excel)"
// (T15 cap15). Lançamentos manuais do caixa e do banco (os de pedido não entram: o mundo falso não monta o vínculo com nota nem com a conta paga).
import { janela, lancamentosResultado, num, diaDe } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  const cats = new Map(store.rows('financial_categories').map((c) => [c.id, c.name]));
  const ccs = new Map(store.rows('cost_centers').map((c) => [c.id, c.name]));
  const contas = new Map(store.rows('bank_accounts').map((c) => [c.id, c.name]));
  const todas = lancamentosResultado(store, ctx.companyId, janela(a.p_start_date, a.p_end_date))
    .sort((x, y) => String(x.transaction_at).localeCompare(String(y.transaction_at)));
  const pag = todas.slice(num(a.p_offset), num(a.p_offset) + (num(a.p_limit) || 1000));
  return pag.map((l) => ({
    movement_id: l.id, movement_source: l.bank_account_id ? 'bank' : 'cash', movement_date: diaDe(l), movement_at: l.transaction_at, direction: l.natureza === 'income' ? 'entrada' : 'saida',
    transaction_type: l.type, description: l.description, amount: l.valor, payment_method: l.payment_method || null, account_name: contas.get(l.bank_account_id) || 'Caixa',
    partner_names: null, partner_documents: null, category_names: cats.get(l.category_id) || null, cost_center_names: ccs.get(l.cost_center_id) || null,
    bills: [], orders: [], invoices: [], is_reconciled: false, reconciled_at: null, total_count: todas.length,
  }));
};
