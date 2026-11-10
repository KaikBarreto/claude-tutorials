// Edge manage-company-users (Usuários e Permissões: "Atualizar" do Editar e "Excluir Usuário"), como a função real
// (supabase/functions/manage-company-users/index.ts do EcoSistema 1.59.154). Ações: update_email (o "Atualizar" manda sempre,
// com o e-mail que já vem preenchido: o mesmo e-mail devolve 200), update_password (mínimo 6 caracteres) e delete_user (só quem
// gerencia usuários; nunca a si mesmo nem o master). Mensagens e códigos HTTP iguais aos da função.
import { remover } from '../../lib/eco.mjs';

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default (body, ctx) => {
  const { store, db, user, FunctionError } = ctx;
  if (!user) throw new FunctionError('Não autorizado', 401);
  const quem = store.rows('profiles').find((p) => p.id === user.id);
  const papeis = (id) => store.rows('user_roles').filter((r) => r.user_id === id).map((r) => r.role);
  const ehMaster = (id) => papeis(id).some((r) => r === 'admin' || r === 'company_admin');
  const pode = ehMaster(user.id) || quem?.permission_preset === 'full_access'
    || store.rows('user_permissions').some((p) => p.user_id === user.id && p.permission === 'action_manage_users');
  const { action, userId, password, email } = body || {};
  const alvo = store.rows('profiles').find((p) => p.id === userId);
  if (!alvo) throw new FunctionError('Usuário não encontrado', 404);
  if (quem?.company_id !== alvo.company_id) throw new FunctionError('Acesso negado: usuário de outra empresa', 403);
  const mesmo = user.id === userId;
  if (!pode && !mesmo) throw new FunctionError('Sem permissão para gerenciar outros usuários', 403);

  if (action === 'update_password') {
    if (!password || String(password).length < 6) throw new FunctionError('Senha deve ter pelo menos 6 caracteres', 400);
    return { success: true, message: 'Senha atualizada com sucesso' };   // a senha não fica guardada no banco falso
  }
  if (action === 'update_email') {
    const novo = email ? String(email).trim().toLowerCase() : null;
    if (!novo || !EMAIL.test(novo)) throw new FunctionError('Email inválido', 400);
    if (store.rows('profiles').some((p) => p.id !== userId && String(p.email || '').toLowerCase() === novo)) {
      throw new FunctionError('Este email já está em uso por outro usuário.', 400);
    }
    if (alvo.email !== novo) db.update('profiles', { id: userId }, { email: novo });
    return { success: true, message: 'Email atualizado com sucesso' };
  }
  if (action === 'delete_user') {
    if (!pode) throw new FunctionError('Sem permissão para excluir usuários', 403);
    if (mesmo) throw new FunctionError('Você não pode excluir seu próprio usuário', 400);
    if (ehMaster(userId)) throw new FunctionError('Não é possível excluir o usuário master da empresa. Transfira o título de master antes de excluí-lo.', 403);
    for (const t of ['user_permissions', 'user_roles', 'active_sessions']) remover(ctx, t, (r) => r.user_id === userId);
    remover(ctx, 'profiles', (r) => r.id === userId);
    return { success: true, message: 'Usuário excluído com sucesso' };
  }
  throw new FunctionError('Ação inválida', 400);
};
