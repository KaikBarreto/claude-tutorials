// Estado do emitente no motor fiscal próprio (app 1.60: migration 20261116123500_fiscal_onboarding_motor_proprio).
// Mundo base: a Recicla Vale já emite (certificado A1 válido no cofre), então a faixa vermelha "Reenvie seu certificado A1"
// não aparece. A aula que mostra o envio do certificado (T16) troca isto pela semente dela: se a configuração tiver
// `fiscal_certificate_status` diferente de 'valid', o retorno acompanha.
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const cfgs = store.rows('company_fiscal_config').filter((c) => c.company_id === cid);
  const cfg = (a.p_fiscal_config_id && cfgs.find((c) => c.id === a.p_fiscal_config_id)) || cfgs[0];
  if (!cfg) {
    return { status: 'emitente_nao_configurado', ready: false, certificate_ready: false, configuration_ready: false, route_ready: false, missing_fields: ['emitente'] };
  }
  const cert = cfg.fiscal_certificate_status || 'valid';
  const ok = cert === 'valid';
  return {
    status: ok ? 'pronto' : 'certificado_pendente', ready: ok, company_id: cid, fiscal_config_id: cfg.id,
    certificate_status: cert, certificate_ready: ok,
    certificate_validated_at: cfg.fiscal_certificate_validated_at || null, certificate_valid_until: cfg.fiscal_certificate_valid_until || null,
    certificate_error_code: cfg.fiscal_certificate_error_code || null, certificate_error_message: cfg.fiscal_certificate_error_message || null,
    certificate_info: cfg.fiscal_certificate_info || {}, vault_present: ok, vault_origin: ok ? 'config' : null, vault_updated_at: cfg.fiscal_certificate_validated_at || null,
    configuration_ready: true, missing_fields: [], route_ready: true, route_stage: null, route_pause_reason: null,
    requires_certificate: true, active_config_count: cfgs.length,
  };
};
