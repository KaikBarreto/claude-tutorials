// Desfazer um pedido (T9): a prévia da exclusão (preview_order_deletion), a exclusão (delete_purchase_atomic / delete_sale_atomic) e a
// reversão da edição (revert_consolidated_order_atomic), como as funções SQL da 1.59.154:
//  - caixa de origem ABERTO (ou sem caixa): hard delete. Some o pedido inteiro: itens, movimentos de estoque (o saldo do material
//    volta), dinheiro e banco do pedido, saldo do parceiro e faturas.
//  - caixa de origem FECHADO: modo compensado. O pedido fica (reverted_at, reverted_compensation_register_id), o estoque volta por um
//    movimento de estorno e o dinheiro volta por um lançamento espelhado no caixa aberto de hoje (p_compensation_register_id).
import { num, r2, agoraMs, inserir, remover, atualizar, atualizaSaldo } from './eco.mjs';

const TAB = { purchase: 'purchases', sale: 'sales' };
const ITENS = { purchase: ['purchase_items', 'purchase_id'], sale: ['sale_items', 'sale_id'] };

export function achaPedido(ctx, tipo, id) {
  const t = TAB[tipo];
  if (!t) throw new ctx.RpcError('invalid_order_type');
  return ctx.store.rows(t).find((p) => p.id === id) || null;
}

/** caixas de origem do pedido (os dos lançamentos em dinheiro) e se algum está fechado */
export function origem(ctx, p) {
  const ids = [...new Set(ctx.store.rows('cash_transactions').filter((c) => c.order_id === p.id && c.cash_register_id).map((c) => c.cash_register_id))];
  const caixas = ids.map((id) => ctx.store.rows('cash_register').find((c) => c.id === id)).filter(Boolean);
  return { caixas, fechado: caixas.some((c) => c.status === 'closed') };
}

export function previa(ctx, tipo, id) {
  const { store } = ctx;
  const p = achaPedido(ctx, tipo, id);
  if (!p || p.company_id !== ctx.companyId) return { exists: false };
  const dir = tipo === 'purchase' ? 'payable' : 'receivable';
  if (p.reverted_at) {
    return { exists: true, already_reverted: true, order_type: tipo, order_number: p.order_number, stock: [], bill: { exists: false, amount: 0, direction: dir }, payments: [], mode_summary: 'compensated', warnings: [] };
  }
  const [tabI, fk] = ITENS[tipo];
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const stock = store.rows(tabI).filter((i) => i[fk] === p.id).map((i) => ({ material_name: mats.get(i.material_id)?.name || i.material_name, qty: r2(num(i.quantity) - num(i.impurity)), unit: mats.get(i.material_id)?.unit || 'Kg' }));
  const { fechado } = origem(ctx, p);
  const modo = fechado ? 'compensated' : 'hard_delete';
  const caixas = new Map(store.rows('cash_register').map((c) => [c.id, c]));
  const contas = new Map(store.rows('bank_accounts').map((b) => [b.id, b]));
  const ord = (x, y) => String(x.transaction_at).localeCompare(String(y.transaction_at)) || String(x.id).localeCompare(String(y.id));
  const pays = [];
  for (const c of store.rows('cash_transactions').filter((c) => c.order_id === p.id && Math.abs(num(c.amount)) >= 0.005).sort(ord)) {
    const cx = caixas.get(c.cash_register_id);
    pays.push({ amount: Math.abs(num(c.amount)), method: 'cash', register_status: cx?.status || 'n/a', reconciled: false, mode: modo, source: 'cash_transaction',
      account_name: cx ? `Caixa #${cx.register_number}` : 'Caixa', shared_account: false, owner_company_name: null, signed_amount: num(c.amount), will_be: fechado ? 'compensated' : 'deleted' });
  }
  for (const b of store.rows('bank_transactions').filter((b) => b.order_id === p.id && Math.abs(num(b.amount)) >= 0.005).sort(ord)) {
    pays.push({ amount: Math.abs(num(b.amount)), method: 'bank', register_status: 'n/a', reconciled: false, mode: 'hard_delete', source: 'bank_transaction',
      account_name: contas.get(b.bank_account_id)?.name || 'Conta bancária', shared_account: false, owner_company_name: null, signed_amount: num(b.amount), will_be: 'deleted' });
  }
  const faturas = store.rows('financial_bills').filter((f) => f.order_id === p.id && f.order_type === tipo);
  return {
    exists: true, already_reverted: false, order_type: tipo, order_number: p.order_number, stock,
    bill: { exists: faturas.length > 0, amount: r2(faturas.reduce((s, f) => s + num(f.amount), 0)), direction: dir },
    payments: pays, mode_summary: modo,
    warnings: fechado ? ['Parte do pedido saiu de um caixa já fechado → em vez de apagar, será lançado um estorno espelhado no caixa aberto de hoje (o histórico do caixa fechado é preservado).'] : [],
  };
}

/** desfaz o pedido; devolve { modo, pedido } */
export function desfaz(ctx, tipo, id, compensacao) {
  const { store, RpcError } = ctx;
  const p = achaPedido(ctx, tipo, id);
  if (!p) return { modo: 'ausente', pedido: null };
  if (p.reverted_at) return { modo: 'ja_revertido', pedido: p };
  const cid = p.company_id;
  const { fechado } = origem(ctx, p);
  const agora = new Date(agoraMs()).toISOString();
  const mats = (mid) => store.rows('materials').find((m) => m.id === mid);
  const movs = store.rows('stock_movements').filter((m) => m.order_id === p.id);
  if (fechado) {
    if (!compensacao) throw new RpcError('COMPENSATION_REGISTER_REQUIRED: abra o caixa de hoje para estornar um pedido de caixa fechado');
    const cx = store.rows('cash_register').find((c) => c.id === compensacao);
    if (!cx || cx.status !== 'open') throw new RpcError('ABRA_CAIXA_HOJE: caixa de compensação inexistente ou fechado');
    for (const m of movs) {
      const mat = mats(m.material_id);
      const antes = num(mat?.current_stock);
      const depois = Math.round((antes - num(m.quantity)) * 1000) / 1000;
      inserir(ctx, 'stock_movements', { company_id: cid, material_id: m.material_id, order_id: p.id, order_type: tipo, type: m.type, quantity: -num(m.quantity),
        stock_before: antes, stock_after: depois, description: `Estorno ${tipo === 'purchase' ? 'da Compra' : 'da Venda'} #${p.order_number}`, created_by: ctx.userId, transaction_at: agora });
      if (mat) { mat.current_stock = depois; store.table('materials').touch(); }
    }
    const dinheiro = store.rows('cash_transactions').filter((c) => c.order_id === p.id).reduce((s, c) => s + num(c.amount), 0);
    if (Math.abs(dinheiro) >= 0.005) {
      inserir(ctx, 'cash_transactions', { company_id: cid, cash_register_id: compensacao, type: tipo === 'purchase' ? 'sale' : 'purchase', amount: r2(dinheiro),
        description: `Estorno ${tipo === 'purchase' ? 'da Compra' : 'da Venda'} #${p.order_number}`, reversal_for_order_id: p.id, created_by: ctx.userId, transaction_at: agora });
    }
    remover(ctx, 'bank_transactions', (b) => b.order_id === p.id);
    atualizar(ctx, TAB[tipo], { id: p.id }, { reverted_at: agora, reverted_compensation_register_id: compensacao });
    return { modo: 'compensated', pedido: p };
  }
  for (const m of movs) {
    const mat = mats(m.material_id);
    if (mat) { mat.current_stock = Math.round((num(mat.current_stock) - num(m.quantity)) * 1000) / 1000; store.table('materials').touch(); }
  }
  remover(ctx, 'stock_movements', (m) => m.order_id === p.id);
  for (const bm of store.rows('balance_movements').filter((b) => b.order_id === p.id)) atualizaSaldo(ctx, cid, bm.entity_type, bm.entity_id, -num(bm.amount));
  remover(ctx, 'balance_movements', (b) => b.order_id === p.id);
  remover(ctx, 'cash_transactions', (c) => c.order_id === p.id);
  remover(ctx, 'bank_transactions', (b) => b.order_id === p.id);
  remover(ctx, 'financial_bills', (f) => f.order_id === p.id && f.order_type === tipo);
  const [tabI, fk] = ITENS[tipo];
  remover(ctx, tabI, (i) => i[fk] === p.id);
  remover(ctx, TAB[tipo], (x) => x.id === p.id);
  return { modo: 'hard_delete', pedido: p };
}

/** linha do Histórico de Exclusões (destructive_actions_audit), rótulo = nome do parceiro */
export function auditoria(ctx, tipo, p, modo) {
  const { store } = ctx;
  const parceiro = tipo === 'purchase' ? store.rows('suppliers').find((s) => s.id === p.supplier_id) : store.rows('customers').find((c) => c.id === p.customer_id);
  const perfil = store.rows('profiles').find((x) => x.id === ctx.userId) || {};
  const papel = store.rows('user_roles').find((r) => r.user_id === ctx.userId)?.role || null;
  const emp = store.rows('companies').find((c) => c.id === p.company_id) || {};
  return ctx.db.insert('destructive_actions_audit', {
    company_id: p.company_id, action_type: 'delete_entity', entity_type: tipo, entity_id: p.id, entity_label: parceiro?.name || `#${p.order_number}`,
    performed_by: ctx.userId, performed_by_email: perfil.email || null, performed_by_role: papel, company_name_snapshot: emp.name || null,
    entity_snapshot: { order_number: p.order_number, total_amount: num(p.total_amount) }, payload: { mode: modo, order_type: tipo },
    created_at: new Date(agoraMs()).toISOString(),
  }, { companyId: p.company_id });
}
