// Edge function create-user falsa (T2: Usuários, cargos e permissões). Espelha supabase/functions/create-user/index.ts (1.38.9).
// Contrato: { email, password, full_name, phone?, permissions?, preset_id?, role?, avatar_url?, employee_id? }
//   -> { user: { id, email } }  |  { error } com 400 (faltam campos / e-mail repetido) ou 403 (quem chama não pode gerir usuários).
// O que o servidor real faz e aqui também: cria o login já confirmado (sem e-mail de convite), grava o perfil na empresa de QUEM CHAMA
// (nunca a do corpo), grava `user_permissions` só se houver ao menos uma permissão (upsert por user_id), `user_roles` só se vier papel
// (sem duplicar) e vincula o funcionário quando vem `employee_id`.
// Diferenças deliberadas:
//  - o banco real preenche `profiles.email` pelo gatilho handle_new_user (o login e a lista de usuários dependem dele); aqui o handler grava
//    o e-mail na mesma hora, em minúsculas;
//  - sem a espera de 800 ms do servidor real (o gatilho do banco);
//  - `terms_accepted_at` fica nulo, como no banco: o termo de uso aparece no primeiro login da pessoa (as sementes `t2/apos-capNN` já
//    trazem os termos aceitos para o capítulo em que o Rafael entra).
// Quem pode gerir usuários: papel admin (o fake só tem a Camila nesse papel) ou a permissão fn:manage_users / curinga '*'.
import { FunctionError } from '../../http/functions.mjs';
import { uuid } from '../../core/util.mjs';

function podeGerirUsuarios(db, userId) {
  if (db.find('user_roles', { user_id: userId }).some((r) => r.role === 'admin' || r.role === 'super_admin')) return true;
  const perm = db.first('user_permissions', { user_id: userId });
  return !!perm && Array.isArray(perm.permissions) && (perm.permissions.includes('*') || perm.permissions.includes('fn:manage_users'));
}

export default async function createUser(body, { db, userId, companyId }) {
  if (!podeGerirUsuarios(db, userId)) throw new FunctionError('Forbidden: requires admin, gestor role or manage_users permission', 403);
  const { email, password, full_name, phone, permissions, preset_id, role, avatar_url, employee_id } = body || {};
  if (!email || !password || !full_name) throw new FunctionError('Missing required fields: email, password, full_name', 400);

  const mail = String(email).trim();
  if (db.rows('profiles').some((p) => String(p.email || '').toLowerCase() === mail.toLowerCase())) {
    throw new FunctionError('Este e-mail já está cadastrado no sistema.', 400);
  }

  const novoId = uuid();
  const caller = db.first('profiles', { user_id: userId });
  db.insert('profiles', {
    user_id: novoId,
    company_id: caller?.company_id || companyId,
    full_name,
    email: mail.toLowerCase(),
    phone: phone || null,
    avatar_url: avatar_url || null,
    is_active: true,
    navigation_style: 'sidebar',
    terms_accepted_at: null,
  });

  if (Array.isArray(permissions) && permissions.length > 0) {
    db.upsert('user_permissions', ['user_id'], { user_id: novoId, permissions, preset_id: preset_id || null, is_active: true });
  }
  if (role && !db.first('user_roles', { user_id: novoId, role })) db.insert('user_roles', { user_id: novoId, role });
  if (employee_id) db.update('employees', { id: employee_id }, { user_id: novoId });

  return { user: { id: novoId, email: mail } };
}
