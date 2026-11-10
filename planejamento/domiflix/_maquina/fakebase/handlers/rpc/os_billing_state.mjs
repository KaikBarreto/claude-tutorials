// RPC os_billing_state(_service_order_id) · usada por "Faturar OS" e pelos selos "Faturada"/"Cobrança enviada".
// Lê receita lançada e cobrança ligadas à OS; no mundo do T5 nenhuma OS foi faturada, então devolve sempre "sem receita, sem cobrança".
export default async function osBillingState({ _service_order_id }, { db }) {
  const tx = db.find('financial_transactions', (r) => r.service_order_id === _service_order_id && r.transaction_type === 'entrada');
  const charge = db.find('tenant_charges', (r) => r.source_type === 'service_order' && r.source_id === _service_order_id)[0] || null;
  return {
    service_order_id: _service_order_id,
    has_revenue: tx.length > 0,
    revenue_total: tx.reduce((s, r) => s + Number(r.amount || 0), 0),
    revenue_count: tx.length,
    has_charge: !!charge,
    charge_id: charge?.id ?? null,
    charge_status: charge?.status ?? null,
    charge_value: charge?.amount ?? null,
    charge_due_date: charge?.due_date ?? null,
  };
}
