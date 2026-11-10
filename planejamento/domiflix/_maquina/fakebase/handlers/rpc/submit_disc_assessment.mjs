// RPC submit_disc_assessment(p_code, p_answers, p_scores, p_profile, p_locale) · 20260725100000_disc_show_result_per_assessment.sql:128-211
// Grava o que o navegador calculou (respostas, pontuação e perfil) e devolve o resultado. Já respondido: não regrava (already: true).
import { nowIso } from '../../core/util.mjs';

export default async function submitDiscAssessment({ p_code, p_answers, p_scores, p_profile, p_locale }, { db }) {
  const code = String(p_code ?? '').trim();
  if (!code) return { error: 'not_found' };
  const a = db.first('disc_assessments', { public_short_code: code });
  if (!a) return { error: 'not_found' };
  const cs = db.first('company_settings', { company_id: a.company_id });
  const mostra = a.show_result_to_employee ?? cs?.disc_show_result_to_employee ?? false;
  if (a.status === 'completed') {
    return { already: true, show_result_to_employee: mostra, scores: a.scores, profile_code: a.profile_code, primary_type: a.primary_type, secondary_type: a.secondary_type };
  }
  const nz = (v) => (String(v ?? '').trim() || null);
  const primary = nz(p_profile?.primary), secondary = nz(p_profile?.secondary), perfil = nz(p_profile?.profile_code);
  db.update('disc_assessments', { id: a.id }, {
    answers: p_answers, scores: p_scores, primary_type: primary, secondary_type: secondary, profile_code: perfil,
    locale: nz(p_locale), status: 'completed', completed_at: nowIso(),
  });
  return { show_result_to_employee: mostra, scores: p_scores, profile_code: perfil, primary_type: primary, secondary_type: secondary };
}
