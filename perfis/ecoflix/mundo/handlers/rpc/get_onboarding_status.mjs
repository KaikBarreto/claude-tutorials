// Guia de implantação: a Recicla Vale Metais é cliente desde março e concluiu o onboarding (o card não aparece).
export default (a, { store, companyId, userId }) => {
  const c = store.rows('companies').find((x) => x.id === (a.p_company_id || companyId));
  return {
    is_owner: c?.onboarding_owner_user_id ? c.onboarding_owner_user_id === userId : true,
    completed_at: c?.onboarding_completed_at || null, dismissed_at: c?.onboarding_dismissed_at || null,
    current_step: null, steps: [], progress: { essencial_done: 0, essencial_total: 0, pct: 100 },
  };
};
