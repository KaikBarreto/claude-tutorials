// RPC publica get_lead_capture_form(p_short_code) -> { form, company_settings } ou null (pagina /cadastro/<slug>-<codigo>).
// Mesmo recorte do banco: allowlist de 7 campos do formulario + 9 da identidade visual da empresa.
export default async function getLeadCaptureForm({ p_short_code }, { db }) {
  const code = String(p_short_code ?? '').trim();
  if (!code) return null;
  const f = db.first('lead_capture_forms', { short_code: code });
  if (!f) return null;
  const expired =
    (f.expires_at && new Date(f.expires_at) <= new Date()) || (f.max_submissions != null && f.submission_count >= f.max_submissions) || false;
  const cs = db.first('company_settings', { company_id: f.company_id });
  return {
    form: {
      title: f.title,
      description: f.description ?? null,
      field_config: f.field_config,
      require_consent: f.require_consent,
      consent_text: f.consent_text ?? null,
      is_active: f.is_active,
      expired,
    },
    company_settings: cs
      ? {
          name: cs.name,
          logo_url: cs.logo_url ?? null,
          white_label_enabled: cs.white_label_enabled ?? false,
          white_label_primary_color: cs.white_label_primary_color ?? null,
          white_label_logo_url: cs.white_label_logo_url ?? null,
          white_label_icon_url: cs.white_label_icon_url ?? null,
          language: cs.language || 'pt-br',
          currency: cs.currency || 'BRL',
          timezone: cs.timezone || 'America/Sao_Paulo',
        }
      : null,
  };
}
