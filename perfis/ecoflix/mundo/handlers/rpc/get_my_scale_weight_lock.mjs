// Trava "Peso somente pela balança" por usuário (app 1.60: migration 20261117124500_scale_weight_lock_per_user).
// Padrão da empresa (companies.scale_weight_lock_enabled) com exceção por usuário (user_scale_weight_policies.requires_scale).
export default (a, { store, companyId, userId }) => {
  const c = store.rows('companies').find((x) => x.id === companyId) || {};
  const padrao = !!c.scale_weight_lock_enabled;
  let pol = null;
  try { pol = store.rows('user_scale_weight_policies').find((p) => p.user_id === userId && p.company_id === companyId) || null; } catch (e) { pol = null; }
  const override = pol && pol.requires_scale != null ? !!pol.requires_scale : null;
  return { company_default: padrao, override, enabled: override ?? padrao };
};
