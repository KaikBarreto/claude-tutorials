// Edge function face-enrollment falsa (T15, cap. 9: página "Cadastro facial", /ativar-ponto/<token>, sem login).
// Espelha supabase/functions/face-enrollment/index.ts (1.38.21). Só a ação `context` (a aula toca "Continuar sem biometria"; o cadastro
// facial em si, `complete`, não é demonstrado). O token é o do RPC `create_employee_face_enrollment_link` (hash do nome do funcionário).
//   context → { employee_first_name, company_name, language, white_label_*, logo_url, model_version, embedding_dimension, required_captures,
//               expires_at, point_path }   (point_path = /ponto/<slug do funcionário>, para onde "Continuar sem biometria" leva)
// Token desconhecido, ponto desligado ou funcionário inativo: 404 { error: 'invalid_or_expired_link' } (indistinguíveis, como no banco).
import { FunctionError } from '../../http/functions.mjs';
import { now } from '../../core/util.mjs';
import { tokenDoNome } from '../rpc/create_employee_face_enrollment_link.mjs';

export default async function faceEnrollment(body, { db }) {
  const token = body?.token;
  if (typeof token !== 'string' || !/^[0-9a-f]{64}$/.test(token)) throw new FunctionError('invalid_request', 400);
  if (body.action !== 'context') throw new FunctionError('invalid_request', 400);
  const emp = db.first('employees', (e) => e.ponto_enabled === true && e.is_active !== false && tokenDoNome(e.name) === token);
  if (!emp || !emp.ponto_slug) throw new FunctionError('invalid_or_expired_link', 404);
  const cs = db.first('company_settings', { company_id: emp.company_id }) || {};
  const co = db.first('companies', { id: emp.company_id }) || {};
  return {
    employee_first_name: String(emp.name).trim().split(' ')[0],
    company_name: (cs.name || co.name || 'Empresa').trim(),
    language: ['pt-br', 'en', 'es', 'fr'].includes(String(cs.language || '').trim()) ? String(cs.language).trim() : 'pt-br',
    white_label_enabled: cs.white_label_enabled ?? false, white_label_primary_color: cs.white_label_primary_color ?? null,
    white_label_logo_url: cs.white_label_logo_url ?? null, logo_url: cs.logo_url ?? null,
    model_version: 'face-api@1.7.15/dlib-128d-v1', embedding_dimension: 128, required_captures: 3,
    expires_at: new Date(now().getTime() + 24 * 3600 * 1000).toISOString(), point_path: `/ponto/${emp.ponto_slug}`,
  };
}
