// RPC certificate_vault_status (useCertificateVaultState): o par .pfx + senha está no cofre do emitente? Booleano e data, nada de segredo.
import { configFiscal } from '../../lib/nfe.mjs';

export default (a, { store, companyId }) => {
  const cfg = configFiscal(store, a.p_company_id || companyId, a.p_fiscal_config_id);
  const presente = !!cfg?.plugnotas_certificate_uploaded;
  return { presente, fiscal_config_id: cfg?.id ?? null, atualizado_em: presente ? (cfg.plugnotas_certificate_info?.uploaded_at ?? null) : null,
    rollout_selected: false };
};
