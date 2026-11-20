// Edge create-company-user ("Criar Usuário" em Configurações > Usuários e Permissões), como a função real
// (supabase/functions/create-company-user/index.ts do EcoSistema 1.59.154): quem chama tem de ser o master (company_admin/admin)
// ou ter "Gerenciar Usuários"; e-mail que já existe devolve 409 com a mensagem da função (mesma empresa ou outra); cria o
// usuário (no banco falso o perfil é o usuário: profiles com id, email e full_name, como o gatilho handle_new_user, mais o
// company_id de quem chamou), o papel "operator" e as permissões pedidas, SEM permission_preset (a função não grava o perfil
// rápido: logo depois de criar, o detalhe diz "Personalizado"). Resposta igual à real: { success, user: { id, email, full_name } }
// (a tela lê result.userId, que não existe: foto e tela inicial da criação nunca gravam, achado 1 do T2).
// 1.60.18 (create-company-user/index.ts do EcoSistema): o corpo leva `preset` (obrigatório: full_access, standard_operator, view_only
// ou custom; custom grava permission_preset nulo) e `bank_account_ids` (a restrição de contas pede ao menos uma); a resposta traz
// `userId`, e é por ele que a tela grava a tela inicial, a política de peso e a foto da criação.
import { agoraMs } from '../../lib/eco.mjs';

const normaliza = (e) => String(e || '').trim().toLowerCase();

export default (body, ctx) => {
  const { store, db, user, FunctionError } = ctx;
  if (!user) throw new FunctionError('Unauthorized', 401);
  const quem = store.rows('profiles').find((p) => p.id === user.id);
  if (!quem?.company_id) throw new FunctionError('User profile not found or no company associated', 403);
  const papeis = store.rows('user_roles').filter((r) => r.user_id === user.id).map((r) => r.role);
  const pode = papeis.includes('company_admin') || papeis.includes('admin') || quem.permission_preset === 'full_access'
    || store.rows('user_permissions').some((p) => p.user_id === user.id && p.permission === 'action_manage_users');
  if (!pode) throw new FunctionError('Insufficient permissions', 403);
  const { email, password, full_name: nome, permissions, preset, bank_account_ids: contas } = body || {};
  if (!email || !password || !nome) throw new FunctionError('Missing required fields: email, password, full_name', 400);
  if (!['full_access', 'standard_operator', 'view_only', 'custom'].includes(preset)) throw new FunctionError('Escolha um perfil de acesso antes de criar o usuário.', 400);
  const idsContas = Array.isArray(contas) ? contas.filter(Boolean) : [];
  if (Array.isArray(permissions) && permissions.includes('restriction_bank_accounts_selected_only') && !idsContas.length) {
    throw new FunctionError('Selecione pelo menos uma conta bancária para este usuário.', 400);
  }
  const em = normaliza(email);
  const ja = store.rows('profiles').find((p) => normaliza(p.email) === em);
  if (ja) {
    if (ja.company_id === quem.company_id) throw new FunctionError('Esse email já é usuário desta empresa.', 409);
    throw new FunctionError('Esse email já está em uso em outra empresa. Cada email só pode pertencer a uma empresa por vez.', 409);
  }
  const agora = new Date(agoraMs()).toISOString();
  const novo = db.insert('profiles', { email: em, full_name: nome, company_id: quem.company_id, permission_preset: preset === 'custom' ? null : preset, created_at: agora, updated_at: agora }, { companyId: quem.company_id });
  db.insert('user_roles', { user_id: novo.id, role: 'operator', created_at: agora });
  const lista = Array.isArray(permissions) ? permissions.filter(Boolean) : [];
  if (lista.length) db.insert('user_permissions', lista.map((permission) => ({ user_id: novo.id, permission, created_at: agora })));
  if (idsContas.length && lista.includes('restriction_bank_accounts_selected_only') && preset !== 'full_access') {
    db.insert('user_bank_account_access', [...new Set(idsContas)].map((bank_account_id) => ({ user_id: novo.id, bank_account_id, created_by: user.id, created_at: agora })));
  }
  return { success: true, userId: novo.id, user: { id: novo.id, email: em, full_name: nome } };
};
