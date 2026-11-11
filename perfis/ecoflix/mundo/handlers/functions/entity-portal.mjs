// Edge entity-portal (a página pública /portal/<token> do parceiro): resolve o dono pelo portal_token (fornecedor ou cliente, com o lado
// vinculado), confere o módulo portal_cliente e devolve empresa, parceiro, saldo e movimentos de 90 dias, pedidos (compras/vendas com os
// itens), notas, e a aba Coletas (has_coletas, as ordens do parceiro e as janelas das Configurações). Molde do index.ts da 1.59.154; sem
// senha de portal, sem anexos de pedido, sem tabela de preços, sem campos personalizados nem etiquetas (o mundo não usa).
import { parteDoPortal, temModulo } from '../../lib/coletas.mjs';
import { agoraMs } from '../../lib/eco.mjs';
import { anexos, sessaoValida } from '../../lib/portal.mjs';

const desc = (k) => (a, b) => String(b[k] ?? '').localeCompare(String(a[k] ?? ''));
export default (body, { store, url, FunctionError }) => {
  const token = url.searchParams.get('token') || body?.token;
  if (!token) throw new FunctionError('Token é obrigatório', 400);
  const p = parteDoPortal(store, token);
  if (!p) throw new FunctionError('Token inválido ou expirado', 404);
  if (!temModulo(store, p.companyId, 'portal_cliente')) throw new FunctionError('Portal indisponível', 403, { reason: 'portal_module_inactive' });
  if (p.senha && !sessaoValida(url.searchParams.get('session'), p.ids)) return { requiresLogin: true };
  const co = store.rows('companies').find((c) => c.id === p.companyId) || {};
  const ent = p.row;
  const cfg = p.cfg;

  // saldo (lado legado: entity_type do dono do token) e movimentos dos últimos 90 dias
  const bal = store.rows('balances').find((b) => b.company_id === p.companyId && b.entity_type === p.tipo && b.entity_id === ent.id) || null;
  const desde = new Date(agoraMs() - 90 * 86400000).toISOString();
  let movements = bal
    ? store.rows('balance_movements').filter((m) => m.balance_id === bal.id && String(m.created_at) >= desde).sort(desc('created_at')).slice(0, 100)
      .map((m) => ({ id: m.id, amount: m.amount, movement_type: m.movement_type, description: m.description, created_at: m.created_at,
        payment_method: m.payment_method, order_id: m.order_id }))
    : [];

  // pedidos com os itens (compras do fornecedor, vendas do cliente)
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const item = (i) => ({ name: (mats.get(i.material_id) || {}).name || 'Material', unit: (mats.get(i.material_id) || {}).unit || 'UN', quantity: i.quantity,
    unit_price: i.unit_price, total_price: i.total_price, impurity: i.impurity ?? null, tare_weight: i.tare_weight ?? null, impurity_kg: i.impurity_kg ?? null,
    impurity_pct: i.impurity_pct ?? null, first_weight: i.first_weight ?? null, second_weight: i.second_weight ?? null, weighing_mode: i.weighing_mode ?? null,
    item_discount: i.item_discount ?? null });
  const pedido = (r, tipo, itens) => ({ id: r.id, order_number: r.order_number, order_ref: r.order_ref, total_amount: r.total_amount, currency: r.currency,
    status: r.status, created_at: r.created_at, payment_method: r.payment_method, hide_financial_details: r.hide_financial_details, order_type: tipo,
    items: itens.map(item), attachments: cfg.fotos ? anexos(store, r.id, tipo) : [] });
  let orders = [];
  if (cfg.historico) {
    if (p.customerId) {
      const its = store.rows('sale_items');
      orders.push(...store.rows('sales').filter((s) => s.customer_id === p.customerId && s.company_id === p.companyId).sort(desc('created_at')).slice(0, 100)
        .map((s) => pedido(s, 'sale', its.filter((i) => i.sale_id === s.id))));
    }
    if (p.supplierId) {
      const its = store.rows('purchase_items');
      orders.push(...store.rows('purchases').filter((s) => s.supplier_id === p.supplierId && s.company_id === p.companyId).sort(desc('created_at')).slice(0, 100)
        .map((s) => pedido(s, 'purchase', its.filter((i) => i.purchase_id === s.id))));
    }
    orders = orders.sort(desc('created_at')).slice(0, 100);
  }
  const hidden = new Set();
  orders = orders.map((o) => {
    if (cfg.valores && o.hide_financial_details !== true) return { ...o, hide_financial_details: false };
    hidden.add(o.id);
    return { ...o, hide_financial_details: true, total_amount: 0, items: o.items.map((i) => ({ ...i, unit_price: 0, total_price: 0, item_discount: 0 })) };
  });
  let saldo = bal ? Number(bal.balance) : 0;
  movements = movements.map((m) => {
    if (m.order_id && hidden.has(m.order_id)) {
      saldo -= Number(m.amount) || 0;
      return { ...m, amount: 0, hide_financial_details: true };
    }
    return { ...m, hide_financial_details: false };
  });

  // notas emitidas/canceladas do parceiro
  const invoices = cfg.notas
    ? store.rows('invoices').filter((i) => i.company_id === p.companyId && !i.archived_at && ['emitida', 'cancelada'].includes(i.status)
      && ((p.customerId && i.customer_id === p.customerId) || (p.supplierId && i.supplier_id === p.supplierId))).sort(desc('issue_date')).slice(0, 200)
      .map((i) => ({ id: i.id, invoice_number: i.invoice_number, serie: i.serie, invoice_type: i.invoice_type, issue_date: i.issue_date,
        total_amount: i.total_amount, status: i.status, nfe_key: i.nfe_key, plugnotas_id: i.plugnotas_id }))
    : [];

  // aba Coletas
  const hasColetas = temModulo(store, p.companyId, 'coletas');
  let collections = [];
  let timeWindows = null;
  if (hasColetas) {
    const st = store.rows('collection_settings').find((s) => s.company_id === p.companyId);
    if (st && Array.isArray(st.time_windows) && st.time_windows.length) timeWindows = st.time_windows;
    const evs = store.rows('collection_order_events');
    collections = store.rows('collection_orders').filter((c) => c.company_id === p.companyId && p.ids.includes(c.partner_id)).sort(desc('created_at')).slice(0, 100)
      .map((c) => ({ id: c.id, numero: c.numero, status: c.status, scheduled_date: c.scheduled_date, scheduled_window: c.scheduled_window,
        material_estimado: c.material_estimado, observacoes: c.observacoes, created_at: c.created_at, completed_at: c.completed_at,
        cancel_reason: c.status === 'cancelada'
          ? ((evs.filter((e) => e.order_id === c.id && e.to_status === 'cancelada').sort(desc('created_at'))[0] || {}).nota ?? null) : null }));
  }

  return {
    entity: { name: ent.name, type: p.tipo, is_dual: p.isDual, custom_fields: [], labels: [],
      address: { logradouro: ent.logradouro ?? '', numero: ent.numero ?? '', bairro: ent.bairro ?? '', cidade: ent.cidade ?? '', uf: ent.uf ?? '', cep: ent.cep ?? '' } },
    portal_config: cfg, locked_sections: cfg.locked, requires_login: false, free_sections: [], portal_receipt_format: ent.portal_receipt_format ?? 'auto',
    company: { name: co.name || 'Empresa', logo_url: co.logo_url || null, cnpj: co.cnpj || null, phone: co.phone || null, email: co.email || null,
      address: co.address || null, white_label_enabled: co.white_label_enabled || false, white_label_primary_color: co.white_label_primary_color || null,
      invert_customer_supplier_terms: co.invert_customer_supplier_terms === true, material_prefixes: {},
      show_name_in_documents: co.show_name_in_documents ?? true, show_cnpj_in_documents: co.show_cnpj_in_documents ?? true,
      show_address_in_documents: co.show_address_in_documents ?? true, show_phone_in_documents: co.show_phone_in_documents ?? true,
      show_email_in_documents: co.show_email_in_documents ?? true, address_visibility_settings: co.address_visibility_settings ?? null,
      address_2: co.address_2 ?? null, show_address_2_in_documents: co.show_address_2_in_documents ?? false, base_currency: co.base_currency ?? null },
    balance: saldo, balance_currency: bal ? bal.currency ?? null : null, balance_convention: 'legacy', movements, orders,
    sides: { has_purchases: orders.some((o) => o.order_type === 'purchase'), has_sales: orders.some((o) => o.order_type === 'sale') },
    invoices, has_coletas: hasColetas, collections, time_windows: timeWindows,
  };
};
