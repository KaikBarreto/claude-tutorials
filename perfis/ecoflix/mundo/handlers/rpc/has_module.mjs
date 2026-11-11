// O plano da empresa tem o módulo? (company_modules sem removed_at, ou com effective_until no futuro), como a função SQL. T9.
import { agoraMs } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a._company_id || companyId;
  const agora = new Date(agoraMs()).toISOString();
  return store.rows('company_modules').some((m) => m.company_id === cid && m.module_code === a._module_code && (!m.removed_at || (m.effective_until && m.effective_until > agora)));
};
