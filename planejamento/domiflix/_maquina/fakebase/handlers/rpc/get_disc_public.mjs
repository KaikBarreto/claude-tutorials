// RPC get_disc_public(p_code) · 20260727090000_disc_public_white_label_flag.sql
// Payload público do teste DISC (/avaliacao/<nome>-<código>, sem login): marca da empresa, primeiro nome e nome completo, status e se o resultado
// aparece. scores/perfil só com o teste respondido E liberado. Visibilidade = COALESCE(avaliação, empresa, false). Código inexistente -> null.
export default async function getDiscPublic({ p_code }, { db }) {
  const code = String(p_code ?? '').trim();
  if (!code) return null;
  const a = db.first('disc_assessments', { public_short_code: code });
  if (!a) return null;
  const emp = db.first('employees', { id: a.employee_id });
  const nome = emp?.name ?? null;
  const cs = db.first('company_settings', { company_id: a.company_id });
  const wl = !!cs?.white_label_enabled;
  const logo = wl && String(cs?.white_label_logo_url ?? '').trim() ? cs.white_label_logo_url : (cs?.logo_url ?? null);
  const cor = (wl && String(cs?.white_label_primary_color ?? '').trim()) || '#00C597';
  const mostra = a.show_result_to_employee ?? cs?.disc_show_result_to_employee ?? false;
  const out = {
    company_name: cs?.name ?? null,
    logo_url: logo,
    primary_color: cor,
    company_locale: String(cs?.language ?? '').trim() || 'pt-br',
    white_label_enabled: wl,
    employee_first_name: nome ? nome.split(' ')[0] : null,
    employee_name: nome,
    status: a.status,
    show_result_to_employee: mostra,
  };
  if (a.status === 'completed' && mostra === true) {
    Object.assign(out, { scores: a.scores, profile_code: a.profile_code, primary_type: a.primary_type, secondary_type: a.secondary_type,
      completed_at: a.completed_at, locale: a.locale });
  }
  return out;
}
