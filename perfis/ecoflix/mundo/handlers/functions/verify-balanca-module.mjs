// Edge verify-balanca-module (chamada pelo EcoTray no "destravar" da balança): libera a leitura de peso quando a empresa
// do usuário do token tem o módulo Integração com Balança (ou está em teste), como a função real.
export default (body, { store, user, companyId }) => {
  if (!user) return { unlocked: false, in_carencia: false, carencia_until: null, reason: 'unauthorized' };
  const prof = store.rows('profiles').find((p) => p.id === user.id);
  const cid = prof?.company_id || companyId;
  const comp = store.rows('companies').find((c) => c.id === cid);
  if (!comp) return { unlocked: false, in_carencia: false, carencia_until: null, reason: 'no_company' };
  const temModulo = store.rows('company_modules').some((m) => m.company_id === cid && m.module_code === 'balanca_integration' && !m.removed_at);
  const plano = store.rows('subscription_plans').find((p) => p.code === comp.subscription_plan);
  const doPlano = comp.subscription_status === 'active' && (plano?.modules || []).includes('balanca_integration');
  if (comp.subscription_status === 'testing' || temModulo || doPlano) return { unlocked: true, in_carencia: false, carencia_until: null, reason: null, company_id: cid };
  return { unlocked: false, in_carencia: false, carencia_until: null, reason: 'module_inactive', company_id: cid };
};
