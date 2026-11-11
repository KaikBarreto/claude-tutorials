// RPC accept_ai_terms(p_version) (T21, "Entendi e autorizo"): a empresa autoriza o Cato. Só o administrador (guard do banco,
// mtr_is_company_admin: role admin/company_admin ou preset full_access, como useCatoAiConsent.tsx); grava companies.ai_consent_at,
// ai_consent_version (o TERMS_VERSION do app, '2.0') e ai_consent_by.
import { agoraMs } from '../../lib/eco.mjs';

export default (a, { store, db, userId, companyId, RpcError }) => {
  const prof = store.rows('profiles').find((p) => p.id === userId);
  const cid = prof?.company_id || companyId;
  const papel = store.rows('user_roles').filter((r) => r.user_id === userId).map((r) => r.role);
  const admin = papel.includes('admin') || papel.includes('company_admin') || prof?.permission_preset === 'full_access';
  if (!admin) throw new RpcError('Apenas o administrador da empresa pode autorizar o Cato.', '42501', 403);
  db.update('companies', { id: cid }, { ai_consent_at: new Date(agoraMs()).toISOString(), ai_consent_version: String(a?.p_version || '2.0'), ai_consent_by: userId });
  return undefined;
};
