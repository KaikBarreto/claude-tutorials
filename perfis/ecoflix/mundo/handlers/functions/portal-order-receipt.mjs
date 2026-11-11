// Edge portal-order-receipt (a impressora "Gerar comprovante" do Histórico do portal; T20 cap09): confere o token do portal (e a sessão, quando o
// portal tem senha) e que o pedido é do parceiro, e devolve os dados que o app transforma no PDF (A4 ou térmico): empresa, pedido, parceiro,
// itens, formas de pagamento (dinheiro, Pix/Transferência, Saldo), quem lançou e o QR "Escaneie para ver fotos" quando o pedido tem fotos
// (cria o link em order_photo_shares se ainda não existir). Molde do index.ts da 1.59.154.
import { parteDoPortal, temModulo } from '../../lib/coletas.mjs';
import { caminhoFotos, sessaoValida } from '../../lib/portal.mjs';

export default (body, { store, db, url, FunctionError }) => {
  const token = url.searchParams.get('token') || body?.token;
  const orderId = url.searchParams.get('order_id') || body?.order_id;
  if (!token || !orderId) throw new FunctionError('Token e order_id são obrigatórios', 400);
  const p = parteDoPortal(store, token);
  if (!p) throw new FunctionError('Token inválido', 404);
  if (!temModulo(store, p.companyId, 'portal_cliente')) throw new FunctionError('Portal indisponível', 403, { reason: 'portal_module_inactive' });
  if (p.senha && !sessaoValida(url.searchParams.get('session'), p.ids)) throw new FunctionError('login', 401, { requiresLogin: true });
  const co = store.rows('companies').find((c) => c.id === p.companyId) || {};
  let tipo = 'sale';
  let pedido = store.rows('sales').find((s) => s.id === orderId && s.company_id === p.companyId);
  let itens;
  if (pedido) {
    if (!p.customerId || pedido.customer_id !== p.customerId) throw new FunctionError('Pedido não pertence a esta entidade', 403);
    itens = store.rows('sale_items').filter((i) => i.sale_id === pedido.id);
  } else {
    pedido = store.rows('purchases').find((s) => s.id === orderId && s.company_id === p.companyId);
    tipo = 'purchase';
    if (pedido) {
      if (!p.supplierId || pedido.supplier_id !== p.supplierId) throw new FunctionError('Pedido não pertence a esta entidade', 403);
      itens = store.rows('purchase_items').filter((i) => i.purchase_id === pedido.id);
    }
  }
  if (!pedido) throw new FunctionError('Pedido não encontrado', 404);
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const linhas = itens.map((i) => {
    const m = mats.get(i.material_id) || {};
    return { code: m.code || '', code_prefix: m.code_prefix || null, name: m.name || i.material_name || '', unit: m.unit || 'UN', quantity: i.quantity,
      impurity: i.impurity ?? 0, unit_price: i.unit_price, total_price: i.total_price, tare_weight: i.tare_weight ?? null, impurity_kg: i.impurity_kg ?? null,
      impurity_pct: i.impurity_pct ?? null, first_weight: i.first_weight ?? null, second_weight: i.second_weight ?? null, weighing_mode: i.weighing_mode ?? null };
  });
  const soma = (xs) => xs.reduce((s, x) => s + Number(x.amount), 0);
  const pagamentos = [];
  const din = soma(store.rows('cash_transactions').filter((t) => t.order_id === orderId && t.type === tipo));
  if (din > 0) pagamentos.push({ method: 'Dinheiro', amount: din });
  const banco = Math.abs(soma(store.rows('bank_transactions').filter((t) => t.order_id === orderId)));
  if (banco > 0) pagamentos.push({ method: 'Pix/Transferência', amount: banco });
  const saldo = Math.abs(soma(store.rows('balance_movements').filter((m) => m.order_id === orderId && m.movement_type === 'order')));
  if (saldo > 0) pagamentos.push({ method: 'Saldo', amount: saldo });
  const total = pagamentos.reduce((s, x) => s + x.amount, 0) || (pedido.total_amount ?? 0);
  const criador = pedido.created_by ? (store.rows('profiles').find((u) => u.id === pedido.created_by) || {}).full_name || '' : '';
  let photoQr = null;
  const fotos = store.rows('order_attachments').filter((a) => a.order_id === pedido.id && a.order_kind === tipo).length;
  if (co.show_photo_qr_on_receipt !== false && fotos > 0) {
    let share = store.rows('order_photo_shares').find((s) => s.order_id === pedido.id && s.order_kind === tipo);
    if (!share) share = db.insert('order_photo_shares', { order_id: pedido.id, order_kind: tipo, company_id: p.companyId }, { companyId: p.companyId });
    photoQr = { path: caminhoFotos(share.token, { empresa: co.name, tipo, ref: pedido.order_ref ?? pedido.order_number }), caption: 'Escaneie para ver fotos', photoCount: fotos };
  }
  const e = p.row;
  return {
    company: { name: co.name || 'Empresa', logo_url: co.logo_url || null, cnpj: co.cnpj || null, phone: co.phone || null, address: co.address || null,
      email: co.email || null, show_name_in_documents: co.show_name_in_documents ?? true, show_cnpj_in_documents: co.show_cnpj_in_documents ?? true,
      show_address_in_documents: co.show_address_in_documents ?? true, show_phone_in_documents: co.show_phone_in_documents ?? true,
      show_email_in_documents: co.show_email_in_documents ?? true, address_visibility_settings: co.address_visibility_settings || null,
      receipt_phrase: co.receipt_phrase || null, show_receipt_phrase: co.show_receipt_phrase ?? false, white_label_enabled: co.white_label_enabled ?? false,
      invert_customer_supplier_terms: co.invert_customer_supplier_terms === true, show_net_weight_only: co.show_net_weight_only ?? false,
      address_2: co.address_2 ?? null, show_address_2_in_documents: co.show_address_2_in_documents ?? false,
      show_signatures_on_receipt: co.show_signatures_on_receipt ?? false, receipt_format: co.receipt_format ?? 'thermal_80mm',
      receipt_item_layout: String(co.receipt_item_layout || '').trim().toLowerCase() === 'b' ? 'b' : 'a', material_prefixes: {},
      show_photo_qr_on_receipt: co.show_photo_qr_on_receipt !== false },
    order: { id: pedido.id, order_number: pedido.order_number, order_type: tipo, total, total_amount: pedido.total_amount ?? null,
      paid_amount: pedido.paid_amount ?? null, freight: pedido.freight || 0, discount: pedido.discount || 0, created_at: pedido.created_at,
      notes: pedido.notes || null, payment_method: pedido.payment_method || null, driver_name: pedido.driver_name || null,
      vehicle_plate: pedido.vehicle_plate || null, hide_financial_details: pedido.hide_financial_details ?? false },
    partner: { name: e.name, type: p.tipo, cpf_cnpj: e.cpf_cnpj ?? null, address: e.address ?? null, phone: e.phone ?? null, pix_key: e.pix_key ?? null,
      logradouro: e.logradouro ?? null, numero: e.numero ?? null, complemento: e.complemento ?? null, bairro: e.bairro ?? null, cidade: e.cidade ?? null,
      uf: e.uf ?? null, cep: e.cep ?? null, bank_name: e.bank_name ?? null, bank_agency: e.bank_agency ?? null, bank_account: e.bank_account ?? null,
      bank_account_type: e.bank_account_type ?? null, show_phone_in_docs: e.show_phone_in_docs ?? true, show_address_in_docs: e.show_address_in_docs ?? true,
      show_cpf_cnpj_in_docs: e.show_cpf_cnpj_in_docs ?? true, show_bank_in_docs: e.show_bank_in_docs ?? true, show_pix_in_docs: e.show_pix_in_docs ?? true },
    items: linhas, paymentMethods: pagamentos, employeeName: criador, photoQr,
  };
};
