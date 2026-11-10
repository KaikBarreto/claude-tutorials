// Contas que a empresa pode usar para pagar/receber (as próprias; sem matriz/filial no mundo base).
import { contas, saldoConta } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const comp = store.rows('companies').find((c) => c.id === companyId);
  return contas(store, companyId).filter((b) => b.kind !== 'card').map((b) => ({
    id: b.id, name: b.name, institution_name: b.institution_name, kind: b.kind, is_default: !!b.is_default, is_archived: !!b.is_archived,
    balance: saldoConta(store, companyId, b), is_own: true, owner_company_id: companyId, owner_company_name: comp?.name || null,
  }));
};
