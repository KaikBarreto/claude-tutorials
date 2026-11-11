// "Como emitir" do Novo MDF-e (T17 cap04): a contingência fica disponível (certificado presente), como o banco responde
// para uma empresa com certificado configurado (migration 20261028193000). Sem isto a tela mostraria "Contingência indisponível".
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const cfg = store.rows('company_fiscal_config').find((c) => c.company_id === cid && c.is_default) || store.rows('company_fiscal_config').find((c) => c.company_id === cid);
  const cert = !!(cfg && cfg.plugnotas_certificate_uploaded);
  return { available: cert, reason: cert ? null : 'Certificado digital não configurado', certificate_present: cert };
};
