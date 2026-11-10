// Histórico de um caixa (tela Caixa e Histórico de Caixa): pedidos do caixa (com o que entrou em dinheiro, banco e saldo)
// e os lançamentos manuais (abertura, despesa, abastecimento, transferência), do mais novo para o mais antigo.
import { num } from '../../lib/eco.mjs';
const FORMA = (pm) => (pm === 'cash' ? 'Dinheiro' : pm === 'boleto' ? 'Boleto' : pm === 'check' ? 'Cheque' : pm === 'card' ? 'Cartão de crédito' : 'Pix/Transferência');
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const rid = a.p_cash_register_id;
  const ct = store.rows('cash_transactions'), bt = store.rows('bank_transactions'), bm = store.rows('balance_movements');
  const pedidosDoCaixa = new Set([...ct.filter((c) => c.cash_register_id === rid && c.order_id), ...bt.filter((b) => b.cash_register_id === rid && b.order_id), ...bm.filter((b) => b.cash_register_id === rid && b.order_id)].map((x) => x.order_id));
  const perfis = new Map(store.rows('profiles').map((p) => [p.id, p]));
  const contas = new Map(store.rows('bank_accounts').map((b) => [b.id, b]));
  const cofre = store.rows('bank_accounts').find((b) => b.company_id === cid && b.kind === 'cash');
  const linhas = [];
  for (const [tab, tipo, ptab, pcol, sem] of [['purchases', 'Compra', 'suppliers', 'supplier_id', 'Sem fornecedor'], ['sales', 'Venda', 'customers', 'customer_id', 'Sem cliente']]) {
    const parceiros = new Map(store.rows(ptab).map((p) => [p.id, p]));
    for (const p of store.rows(tab)) {
      if (p.company_id !== cid || !pedidosDoCaixa.has(p.id)) continue;
      const cash = ct.filter((c) => c.order_id === p.id).reduce((s, c) => s + num(c.amount), 0);
      const banks = bt.filter((b) => b.order_id === p.id).sort((x, y) => String(x.created_at).localeCompare(String(y.created_at)));
      const bank = Math.abs(banks.reduce((s, b) => s + num(b.amount), 0));
      const bal = bm.filter((b) => b.order_id === p.id && b.movement_type === 'order').reduce((s, b) => s + Math.abs(num(b.amount)), 0);
      const disp = [cash > 0 && 'Dinheiro', bank > 0 && 'Pix/Transferência', bal > 0 && 'Saldo'].filter(Boolean).join(' + ') || FORMA(p.payment_method);
      const conta = banks[0] ? contas.get(banks[0].bank_account_id) : null;
      const par = parceiros.get(p[pcol]);
      linhas.push({
        id: p.id, source_table: tab, order_number: p.order_number, order_ref: p.order_ref, type: tipo, amount: p.paid_amount ?? p.total_amount, payment_method: p.payment_method,
        entity: par?.name || sem, description: null, date: p.transaction_at || p.created_at, status: p.status, created_by: p.created_by, group_id: null,
        excluded_from_dre: false, bank_account_id: banks[0]?.bank_account_id || null, bank_account_name: conta?.name || null, bank_account_color: conta?.color || null,
        bank_balance_after: banks[0]?.balance_after ?? null, cash_total: cash, bank_total: bank, balance_total: bal, payment_method_display: disp, notes: p.notes,
        partner_pix_key: par?.pix_key || null, total_amount: p.total_amount, paid_amount: p.paid_amount, _created: p.created_at,
      });
    }
  }
  for (const c of ct) {
    if (c.company_id !== cid || c.cash_register_id !== rid || !['withdrawal', 'deposit', 'saida', 'entrada', 'opening', 'transfer', 'expense'].includes(c.type)) continue;
    const tipo = c.type === 'transfer' ? 'Transferência' : ['withdrawal', 'saida', 'expense'].includes(c.type) ? 'Despesa' : c.type === 'opening' ? 'Abertura' : 'Abastecimento';
    linhas.push({ id: c.id, source_table: 'cash_transactions', order_number: null, order_ref: null, type: tipo, amount: c.amount, payment_method: 'cash', entity: c.description || '-', description: c.description || '', date: c.transaction_at || c.created_at, status: 'completed', created_by: c.created_by, group_id: c.group_id || null, excluded_from_dre: !!c.excluded_from_dre, bank_account_id: null, bank_account_name: null, bank_account_color: null, bank_balance_after: null, cash_total: 0, bank_total: 0, balance_total: 0, payment_method_display: 'Dinheiro', notes: null, partner_pix_key: null, total_amount: null, paid_amount: null, _created: c.created_at });
  }
  for (const b of bt) {
    if (b.company_id !== cid || b.cash_register_id !== rid || !['deposit', 'withdrawal', 'transfer', 'expense'].includes(b.type)) continue;
    if (/^(Compra|Venda)\s+#\d+/.test(b.description || '') || (cofre && b.bank_account_id === cofre.id && b.type === 'transfer')) continue;
    const tipo = /^Ajuste de saldo/i.test(b.description || '') ? 'Ajuste' : b.type === 'transfer' ? 'Transferência' : ['withdrawal', 'expense'].includes(b.type) ? 'Despesa' : 'Abastecimento';
    const conta = contas.get(b.bank_account_id);
    linhas.push({ id: b.id, source_table: 'bank_transactions', order_number: null, order_ref: null, type: tipo, amount: Math.abs(num(b.amount)), payment_method: b.payment_method || 'transfer', entity: b.description || '-', description: b.description || '', date: b.transaction_at || b.created_at, status: 'completed', created_by: b.created_by, group_id: b.group_id || null, excluded_from_dre: !!b.excluded_from_dre, bank_account_id: b.bank_account_id, bank_account_name: conta?.name || null, bank_account_color: conta?.color || null, bank_balance_after: b.balance_after ?? null, cash_total: 0, bank_total: 0, balance_total: 0, payment_method_display: FORMA(b.payment_method || 'transfer'), notes: null, partner_pix_key: null, total_amount: null, paid_amount: null, _created: b.created_at });
  }
  // grupos (lançamentos com o mesmo group_id)
  const grupos = new Map();
  for (const l of linhas) if (l.group_id) (grupos.get(l.group_id) || grupos.set(l.group_id, []).get(l.group_id)).push(l);
  const ord = (x, y) => String(y.date).localeCompare(String(x.date)) || String(y._created).localeCompare(String(x._created)) || String(y.id).localeCompare(String(x.id));
  for (const l of linhas) {
    const g = l.group_id ? grupos.get(l.group_id).slice().sort(ord) : null;
    const n = g ? g.length : 0;
    l.is_grouped = n > 1; l.group_size = n > 1 ? n : 0; l.is_first_in_group = n > 1 && g[0].id === l.id; l.is_last_in_group = n > 1 && g[n - 1].id === l.id;
    const pf = perfis.get(l.created_by);
    l.created_by_name = pf?.full_name || null; l.created_by_avatar = pf?.avatar_url || null;
  }
  const busca = String(a.p_search || '').trim().toLowerCase();
  const tf = a.p_type_filter || 'all', pf = a.p_payment_filter || 'all';
  const ok = (l) => (!busca || [l.entity, l.description, l.type, l.order_number != null ? String(l.order_number) : ''].some((x) => String(x || '').toLowerCase().includes(busca)))
    && (tf === 'all' || ({ compra: 'Compra', venda: 'Venda', despesa: 'Despesa', abastecimento: 'Abastecimento' })[tf] === l.type)
    && (pf === 'all' || (pf === 'cash' && l.payment_method_display.includes('Dinheiro')) || (pf === 'transfer' && l.payment_method_display.includes('Pix/Transferência')) || (['boleto', 'check', 'card'].includes(pf) && l.payment_method === pf) || (pf === 'mixed' && l.payment_method_display.includes('+')));
  const fil = linhas.filter(ok).sort(ord);
  const off = Number(a.p_offset) || 0;
  return fil.slice(off, off + (Number(a.p_limit) || 10)).map(({ _created, ...l }) => ({ ...l, total_count: fil.length }));
};
