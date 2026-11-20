// Edge entity-portal (a página pública /portal/<token> do parceiro): resolve o dono pelo portal_token (fornecedor ou cliente, com o lado
// vinculado), confere o módulo portal_cliente e devolve empresa, parceiro, saldo e movimentos de 90 dias, pedidos (compras/vendas com os
// itens), notas, aba Preços (price_list), senha por seção (requires_login/free_sections) e a aba Coletas (has_coletas, as ordens do parceiro e as janelas das Configurações). Molde do index.ts da 1.59.154; sem
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
  const co = store.rows('companies').find((c) => c.id === p.companyId) || {};
  const ent = p.row;
  const cfg = p.cfg;
  // senha por seção (1.60.x): sem sessão, só as seções visíveis e livres (locked === false) saem; nenhuma livre = { requiresLogin: true }
  const hasColetasMod = temModulo(store, p.companyId, 'coletas');
  let partial = false;
  let freeSections = [];
  if (p.senha && !sessaoValida(url.searchParams.get('session'), p.ids)) {
    const visivel = { historico: cfg.historico, saldo: cfg.saldo, notas: cfg.notas, relatorio: cfg.relatorio, coletas: cfg.coletas && hasColetasMod,
      precos: cfg.precos === true && !!p.supplierId };
    freeSections = Object.keys(visivel).filter((k) => visivel[k] && cfg.locked[k] === false);
    if (!freeSections.length) return { requiresLogin: true };
    partial = true;
  }
  const serve = (s) => !partial || freeSections.includes(s);

  // saldo e movimentos dos últimos 90 dias. Parceiro dual: a linha 'party' (convenção cliente) e o link de fornecedor inverte o sinal
  const isDualSupplier = p.isDual && p.tipo === 'supplier';
  const bal0 = !serve('saldo') ? null : (p.isDual
    ? store.rows('balances').find((b) => b.company_id === p.companyId && b.entity_type === 'party' && b.entity_id === p.customerId)
    : store.rows('balances').find((b) => b.company_id === p.companyId && b.entity_type === p.tipo && b.entity_id === ent.id)) || null;
  const bal = bal0 ? { ...bal0, balance: isDualSupplier ? -Number(bal0.balance) : Number(bal0.balance) } : null;
  const desde = new Date(agoraMs() - 90 * 86400000).toISOString();
  let movements = bal
    ? store.rows('balance_movements').filter((m) => m.balance_id === bal0.id && String(m.created_at) >= desde).sort(desc('created_at')).slice(0, 100)
      .map((m) => ({ id: m.id, amount: isDualSupplier ? -Number(m.amount) : m.amount, movement_type: m.movement_type, description: m.description,
        created_at: m.created_at, payment_method: m.payment_method, order_id: m.order_id }))
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
  if (cfg.historico && serve('historico')) {
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
  // "sem valor": o pedido marcado no cadastro OU o portal com "Valores financeiros" desligado esconde o valor (servidor, não só a tela)
  const hidden = new Set();
  const flagged = new Set();
  orders = orders.map((o) => {
    const marcado = o.hide_financial_details === true;
    if (marcado) flagged.add(o.id);
    if (cfg.valores && !marcado) return { ...o, hide_financial_details: false };
    hidden.add(o.id);
    return { ...o, hide_financial_details: true, total_amount: 0, items: o.items.map((i) => ({ ...i, unit_price: 0, total_price: 0, item_discount: 0 })) };
  });

  // notas emitidas/canceladas do parceiro
  let invoices = cfg.notas && serve('notas')
    ? store.rows('invoices').filter((i) => i.company_id === p.companyId && !i.archived_at && ['emitida', 'cancelada'].includes(i.status)
      && ((p.customerId && i.customer_id === p.customerId) || (p.supplierId && i.supplier_id === p.supplierId))).sort(desc('issue_date')).slice(0, 200)
      .map((i) => ({ id: i.id, order_id: i.order_id ?? null, invoice_number: i.invoice_number, serie: i.serie, invoice_type: i.invoice_type, issue_date: i.issue_date,
        total_amount: i.total_amount, status: i.status, nfe_key: i.nfe_key, plugnotas_id: i.plugnotas_id }))
    : [];

  // pedido "sem valor" FORA do feed (movimento ou nota de um pedido que não está na lista): confere no cadastro do pedido
  const noFeed = new Set(orders.map((o) => o.id));
  const fora = new Set([...movements.map((m) => m.order_id), ...invoices.map((i) => i.order_id)].filter((id) => id && !noFeed.has(id)));
  for (const r of [...store.rows('sales'), ...store.rows('purchases')]) {
    if (fora.has(r.id) && r.hide_financial_details === true) { flagged.add(r.id); hidden.add(r.id); }
  }
  invoices = invoices.map(({ order_id, ...rest }) => (order_id && flagged.has(order_id)
    ? { ...rest, total_amount: 0, nfe_key: null, plugnotas_id: null, hide_financial_details: true } : { ...rest, hide_financial_details: false }));

  // o SALDO sai igual ao da tela de Saldo do sistema (19/11/2026): sem descontar o movimento escondido; o movimento sai zerado
  const saldo = bal ? Number(bal.balance) : 0;
  movements = movements.map((m) => (m.order_id && (!cfg.valores || hidden.has(m.order_id))
    ? { ...m, amount: 0, hide_financial_details: true } : { ...m, hide_financial_details: false }));

  // aba Preços do fornecedor (RPC get_entity_portal_price_list): preço próprio > tabela do fornecedor > preço de compra do material; a chave só
  // existe no payload quando "Aba Preços" está ligada (sem ela, nem a RPC roda). Dual: vale o lado fornecedor do par.
  let priceList = null;
  if (cfg.precos === true && p.supplierId && serve('precos')) {
    const sup = store.rows('suppliers').find((x) => x.id === p.supplierId) || {};
    const custom = new Map(store.rows('entity_custom_prices').filter((c) => c.entity_type === 'supplier' && c.entity_id === p.supplierId).map((c) => [c.material_id, Number(c.custom_price)]));
    const tabela = new Map(store.rows('price_table_items').filter((t) => sup.default_price_table_id && t.price_table_id === sup.default_price_table_id).map((t) => [t.material_id, Number(t.purchase_price)]));
    const proprios = new Map();
    for (const c of store.rows('purchases').filter((x) => x.supplier_id === p.supplierId && x.company_id === p.companyId && !x.cancelled_at && !x.reverted_at)) {
      for (const i of store.rows('purchase_items').filter((it) => it.purchase_id === c.id)) {
        const o = proprios.get(i.material_id) || { last: '', qty: 0 };
        if (String(c.transaction_at || c.created_at) > o.last) o.last = String(c.transaction_at || c.created_at);
        if (String(c.transaction_at || c.created_at) >= new Date(agoraMs() - 365 * 86400000).toISOString()) o.qty += Number(i.quantity || 0);
        proprios.set(i.material_id, o);
      }
    }
    priceList = store.rows('materials').filter((m) => m.company_id === p.companyId && !m.is_archived).map((m) => {
      const preco = custom.has(m.id) ? custom.get(m.id) : tabela.has(m.id) ? tabela.get(m.id) : Number(m.purchase_price || 0);
      const o = proprios.get(m.id);
      return { material_id: m.id, code: m.code ?? null, code_prefix: m.code_prefix ?? null, name: m.name, unit: m.unit ?? null, price: preco, is_own: !!o,
        own_qty: o ? o.qty : 0, last_purchase_at: o ? o.last : null };
    }).filter((r) => r.price > 0).sort((a, b) => (b.is_own - a.is_own) || (b.own_qty - a.own_qty) || String(a.name).localeCompare(String(b.name)));
  }

  // aba Coletas
  const hasColetas = temModulo(store, p.companyId, 'coletas');
  let collections = [];
  let timeWindows = null;
  if (hasColetas && serve('coletas')) {
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
      ...(partial ? {} : { address: { logradouro: ent.logradouro ?? '', numero: ent.numero ?? '', bairro: ent.bairro ?? '', cidade: ent.cidade ?? '', uf: ent.uf ?? '', cep: ent.cep ?? '' } }) },
    portal_config: cfg, locked_sections: cfg.locked, requires_login: partial, free_sections: freeSections, portal_receipt_format: ent.portal_receipt_format ?? 'auto',
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
    ...(priceList ? { price_list: priceList, price_list_generated_at: new Date(agoraMs()).toISOString() } : {}),
  };
};
