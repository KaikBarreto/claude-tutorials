// Edge order-photos-public (a página pública /fotos/<empresa>-compra-<nº>-<código>, aberta pelo QR "Escaneie para ver fotos" do comprovante;
// T20 cap10): o token de order_photo_shares leva ao pedido; devolve cabeçalho (empresa, nº), as fotos com URL "assinada" do storage falso, e os
// dados do pedido (parceiro, itens, total, pago, forma de pagamento). Pedido "sem valor": preços e totais saem nulos. Sem senha do portal.
import { temModulo } from '../../lib/coletas.mjs';
import { anexos } from '../../lib/portal.mjs';

export default (body, { store, url, FunctionError }) => {
  const token = url.searchParams.get('token') || body?.token;
  if (!token) throw new FunctionError('Token é obrigatório', 400);
  const share = store.rows('order_photo_shares').find((s) => s.token === token);
  if (!share) throw new FunctionError('Link inválido ou expirado', 404);
  if (!temModulo(store, share.company_id, 'portal_cliente')) throw new FunctionError('Portal indisponível', 403, { reason: 'portal_module_inactive' });
  const co = store.rows('companies').find((c) => c.id === share.company_id) || {};
  const venda = share.order_kind === 'sale';
  const pedido = store.rows(venda ? 'sales' : 'purchases').find((o) => o.id === share.order_id) || {};
  const oculto = !!pedido.hide_financial_details;
  const parceiro = pedido[venda ? 'customer_id' : 'supplier_id']
    ? (store.rows(venda ? 'customers' : 'suppliers').find((x) => x.id === pedido[venda ? 'customer_id' : 'supplier_id']) || {}).name ?? null : null;
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const itens = store.rows(venda ? 'sale_items' : 'purchase_items').filter((i) => i[venda ? 'sale_id' : 'purchase_id'] === share.order_id)
    .map((i) => ({ materialName: i.material_name ?? (mats.get(i.material_id) || {}).name ?? '-', unit: (mats.get(i.material_id) || {}).unit ?? 'Kg',
      quantity: i.quantity, unitPrice: oculto ? null : i.unit_price, totalPrice: oculto ? null : i.total_price }));
  return {
    orderNumber: pedido.order_number ?? null, orderKind: share.order_kind, companyName: co.name ?? null, companyLogo: co.logo_url ?? null,
    invertCustomerSupplierTerms: co.invert_customer_supplier_terms === true,
    photos: anexos(store, share.order_id, share.order_kind),
    order: { partnerName: parceiro, createdAt: pedido.transaction_at ?? pedido.created_at ?? null, notes: pedido.notes ?? null,
      driverName: pedido.driver_name ?? null, vehiclePlate: pedido.vehicle_plate ?? null, paymentMethod: oculto ? null : pedido.payment_method ?? null,
      totalAmount: oculto ? null : pedido.total_amount ?? null, paidAmount: oculto ? null : pedido.paid_amount ?? null, hideFinancials: oculto, items: itens },
  };
};
