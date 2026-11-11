// RPC get_group_subscription_summary (20261016150000), a tela "Assinaturas do grupo" e o checkout do grupo: uma linha por empresa (matriz
// primeiro, depois por nome) com plano, ciclo, situação, vencimento, valor efetivo e o que a fatura única cobra (group_expected_payment).
import { exigeDono, empresasDoGrupo } from '../../lib/grupo.mjs';
import { esperado } from './group_expected_payment.mjs';
import { num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  const g = exigeDono(ctx, a._group_id);
  const exp = esperado(store, g.id);
  return empresasDoGrupo(store, g.id).map((id) => store.rows('companies').find((c) => c.id === id)).filter(Boolean).map((c) => {
    const m = exp.members.find((x) => x.company_id === c.id) || {};
    const promo = num(c.custom_price) > 0 && num(c.custom_price_months) > 0 && num(c.custom_price_payments_made) < num(c.custom_price_months);
    return { company_id: c.id, company_name: c.name, is_matriz: c.id === g.owner_company_id, subscription_plan: c.subscription_plan, billing_cycle: c.billing_cycle,
      subscription_status: c.subscription_status, subscription_expires_at: c.subscription_expires_at, subscription_value: c.subscription_value,
      custom_price: c.custom_price ?? null, effective_value: promo ? c.custom_price : c.subscription_value, max_users: c.max_users, extra_users: c.extra_users ?? 0,
      expected_value: m.expected ?? null, expected_basis: m.basis ?? null, installment_label: m.installment ?? null, new_expires_at: m.new_expires_at ?? null,
      group_expected_total: exp.total, group_mixed_cycle: exp.mixed_cycle };
  }).sort((x, y) => Number(y.is_matriz) - Number(x.is_matriz) || String(x.company_name).localeCompare(String(y.company_name)));
};
