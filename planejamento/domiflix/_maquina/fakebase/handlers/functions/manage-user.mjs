// Edge function manage-user falsa (T2: Usuários, cargos e permissões). Espelha supabase/functions/manage-user/index.ts (1.38.9).
// Contrato: { action, user_id, email? } com action em
//   get_email        -> { email }                     (a janela "Editar Usuário" pede o e-mail do login)
//   update_email     -> { success: true }             (e-mail inválido: 400 "Invalid email"; repetido: 400)
//   deactivate_user  -> { success: true }             (marca o perfil inativo e encerra as sessões; recusa o próprio usuário)
//   reactivate_user  -> { success: true }             (só com vaga livre: ativos < vagas do plano + extras; senão 400)
//   delete_user      -> { success: true }             (apaga permissões, papéis, vínculo com funcionário, perfil e sessões; recusa o próprio usuário)
// Erros: 400 { error }, 403 (quem chama não gere usuários ou o alvo é de outra empresa).
// Vagas (espelha useCompanyModules.ts:236-243 e a própria edge): plano 'personalizado' usa companies.max_users como total; os demais somam
// subscription_plans.max_users + companies.extra_users. Só perfis ATIVOS ocupam vaga.
import { FunctionError } from '../../http/functions.mjs';

function podeGerirUsuarios(db, userId) {
  if (db.find('user_roles', { user_id: userId }).some((r) => r.role === 'admin' || r.role === 'super_admin')) return true;
  const perm = db.first('user_permissions', { user_id: userId });
  return !!perm && Array.isArray(perm.permissions) && (perm.permissions.includes('*') || perm.permissions.includes('fn:manage_users'));
}

export default async function manageUser(body, { db, store, userId }) {
  if (!podeGerirUsuarios(db, userId)) throw new FunctionError('Forbidden: insufficient permissions', 403);
  const { action, user_id, email } = body || {};
  if (!user_id) throw new FunctionError('Missing user_id', 400);

  const alvo = db.first('profiles', { user_id });
  const chamador = db.first('profiles', { user_id: userId });
  const mesmaEmpresa = () => !!alvo?.company_id && alvo.company_id === chamador?.company_id;
  const encerraSessoes = () => {
    if (store.peek('active_sessions')) db.remove('active_sessions', { user_id });
  };

  if (action === 'get_email') return { email: alvo?.email || '' };

  if (action === 'update_email') {
    if (!email || typeof email !== 'string' || !email.includes('@')) throw new FunctionError('Invalid email', 400);
    const outro = db.rows('profiles').find((p) => p.user_id !== user_id && String(p.email || '').toLowerCase() === email.toLowerCase());
    if (outro) throw new FunctionError('A user with this email address has already been registered', 400);
    db.update('profiles', { user_id }, { email: email.toLowerCase() });
    return { success: true };
  }

  if (action === 'deactivate_user') {
    if (user_id === userId) throw new FunctionError('Você não pode desativar a si mesmo.', 400);
    if (!mesmaEmpresa()) throw new FunctionError('Forbidden: usuário de outra empresa', 403);
    db.update('profiles', { user_id }, { is_active: false });
    encerraSessoes();
    return { success: true };
  }

  if (action === 'reactivate_user') {
    if (!mesmaEmpresa()) throw new FunctionError('Forbidden: usuário de outra empresa', 403);
    const empresa = db.first('companies', { id: alvo.company_id });
    const plano = empresa?.subscription_plan || 'start';
    const extras = empresa?.extra_users || 0;
    let vagas;
    if (plano === 'personalizado') vagas = empresa?.max_users || 0;
    else vagas = (db.first('subscription_plans', { code: plano })?.max_users ?? empresa?.max_users ?? 0) + extras;
    const ativos = db.find('profiles', (p) => p.company_id === alvo.company_id && p.is_active === true).length;
    if (ativos >= vagas) throw new FunctionError('Limite de usuários atingido; faça upgrade ou desative outro.', 400);
    db.update('profiles', { user_id }, { is_active: true });
    return { success: true };
  }

  if (action === 'delete_user') {
    if (user_id === userId) throw new FunctionError('Você não pode excluir a si mesmo.', 400);
    if (!mesmaEmpresa()) throw new FunctionError('Forbidden: usuário de outra empresa', 403);
    db.remove('user_permissions', { user_id });
    db.remove('user_roles', { user_id });
    db.update('employees', { user_id }, { user_id: null });
    db.remove('profiles', { user_id });
    encerraSessoes();
    return { success: true };
  }

  throw new FunctionError('Invalid action', 400);
}
