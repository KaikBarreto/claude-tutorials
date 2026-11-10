// Lista de Pedidos (compras e vendas) com pagamentos e itens, filtros e paginação (como a função SQL).
import { pagamentosDoPedido, num } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const busca = String(a.p_search || '').trim().toLowerCase();
  const tipos = Array.isArray(a.p_order_types) && a.p_order_types.length ? a.p_order_types : null;
  const mats = Array.isArray(a.p_material_ids) && a.p_material_ids.length ? new Set(a.p_material_ids) : null;
  const contasF = Array.isArray(a.p_account_ids) && a.p_account_ids.length ? new Set(a.p_account_ids) : null;
  const kinds = Array.isArray(a.p_payment_kinds) && a.p_payment_kinds.length ? a.p_payment_kinds : null;
  const perfis = new Map(store.rows('profiles').map((p) => [p.id, p.full_name]));
  const linhas = [];
  for (const tipo of ['sale', 'purchase']) {
    if (tipos && !tipos.includes(tipo)) continue;
    const parceiros = new Map(store.rows(tipo === 'sale' ? 'customers' : 'suppliers').map((p) => [p.id, p.name]));
    const itensT = store.rows(tipo === 'sale' ? 'sale_items' : 'purchase_items');
    for (const p of store.rows(tipo === 'sale' ? 'sales' : 'purchases')) {
      if (p.company_id !== cid) continue;
      if (a.p_date_from && p.transaction_date < a.p_date_from) continue;
      if (a.p_date_to && p.transaction_date > a.p_date_to) continue;
      const pid = tipo === 'sale' ? p.customer_id : p.supplier_id;
      const nome = pid ? parceiros.get(pid) : null;
      if (busca && !(String(nome || '').toLowerCase().includes(busca) || String(p.order_ref || '').toLowerCase().includes(busca) || String(p.order_number).includes(busca))) continue;
      const its = itensT.filter((i) => (tipo === 'sale' ? i.sale_id : i.purchase_id) === p.id);
      if (mats && !its.some((i) => mats.has(i.material_id))) continue;
      const pg = pagamentosDoPedido(store, p, tipo);
      if (contasF && !pg.bank.some((b) => contasF.has(b.bank_account_id))) continue;
      if (kinds) {
        const tem = { cash: pg.cash.length > 0, transfer: pg.bank.length > 0, balance: pg.bal.length > 0 };
        const ok = (kinds.includes('cash') && tem.cash) || (kinds.includes('transfer') && tem.transfer) || (kinds.includes('mixed') && tem.cash + tem.transfer + tem.balance >= 2);
        if (!ok) continue;
      }
      const contaNome = new Map(store.rows('bank_accounts').map((b) => [b.id, b.name]));
      linhas.push({
        id: p.id, company_id: p.company_id, created_at: p.created_at, order_number: p.order_number, order_ref: p.order_ref, total_amount: p.total_amount,
        notes: p.notes, status: p.status, payment_method: p.payment_method, order_type: tipo, partner_id: pid || null, partner_name: nome || null,
        created_by_name: perfis.get(p.created_by) || null,
        cash_payments: pg.cash.map((c) => ({ method: 'Dinheiro', amount: num(c.amount) })),
        bank_payments: pg.bank.map((b) => ({ method: 'Pix/Transferência', amount: num(b.amount), bank_account_id: b.bank_account_id, bank_account_name: contaNome.get(b.bank_account_id) || null })),
        balance_payments: pg.bal.map((b) => ({ method: 'Saldo', amount: Math.abs(num(b.amount)) })),
        items: its.map((i) => ({ material_name: i.material_name, quantity: i.quantity, unit_price: i.unit_price, total_price: i.total_price, impurity: i.impurity, tare_weight: i.tare_weight, impurity_kg: i.impurity_kg, impurity_pct: i.impurity_pct, first_weight: i.first_weight, second_weight: i.second_weight, weighing_mode: i.weighing_mode })),
        transaction_at: p.transaction_at, transaction_date: p.transaction_date, driver_name: p.driver_name, vehicle_plate: p.vehicle_plate, paid_amount: p.paid_amount,
        hide_financial_details: !!p.hide_financial_details, reverted_at: p.reverted_at || null, reverted_compensation_register_id: p.reverted_compensation_register_id || null, currency: p.currency || 'BRL',
      });
    }
  }
  linhas.sort((x, y) => (y.transaction_at || '').localeCompare(x.transaction_at || '') || (y.created_at || '').localeCompare(x.created_at || '') || y.id.localeCompare(x.id));
  const off = Number(a.p_offset) || 0;
  return linhas.slice(off, off + (Number(a.p_limit) || 50));
};
