// RPC get_tenant_subscription_delete_capabilities() -> [{ subscription_id, charge_count, can_delete }] (T19 · aba Assinaturas, 1.38.19).
// A real usa a empresa do JWT e conta TODA cobrança da assinatura (inclusive pendente); só assinatura sem cobrança pode ser excluída.
export default async function getTenantSubscriptionDeleteCapabilities(_a, { db, companyId }) {
  return db.rows('tenant_subscriptions')
    .filter((s) => String(s.company_id) === String(companyId) && !s.deleted_at)
    .map((s) => {
      const n = db.rows('tenant_charges').filter((c) => String(c.subscription_id) === String(s.id)).length;
      return { subscription_id: s.id, charge_count: n, can_delete: n === 0 };
    });
}
