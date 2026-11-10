// save_user_permissions(p_user_id, p_permissions, p_preset) ("Atualizar" do Editar em Usuários e Permissões), como a função
// SQL do EcoSistema 1.59.154 (migração 20260917235917_guard_ultimo_gestor_de_usuarios.sql): confere quem chama (master da
// plataforma, ou da mesma empresa sendo company_admin ou com "Gerenciar Usuários"), apaga as permissões do usuário, grava as
// novas (nenhuma com full_access), põe o preset no perfil e recusa o que deixaria a empresa sem ninguém que gerencie usuários.
import { agoraMs } from '../../lib/eco.mjs';

const PRESETS = ['full_access', 'standard_operator', 'view_only'];

export default (a, ctx) => {
  const { store, db, userId, RpcError } = ctx;
  if (!a.p_user_id) throw new RpcError('Informe o usuário cujas permissões serão salvas.');
  const preset = a.p_preset ?? null;
  if (preset !== null && !PRESETS.includes(preset)) throw new RpcError(`Conjunto de permissões desconhecido: ${preset}.`);
  const alvo = store.rows('profiles').find((p) => p.id === a.p_user_id);
  if (!alvo) throw new RpcError('Usuário não encontrado.');
  const papeis = (id) => store.rows('user_roles').filter((r) => r.user_id === id).map((r) => r.role);
  const temAcao = (id, perm) => store.rows('profiles').find((p) => p.id === id)?.permission_preset === 'full_access'
    || store.rows('user_permissions').some((p) => p.user_id === id && p.permission === perm);
  const quem = store.rows('profiles').find((p) => p.id === userId);
  const pode = papeis(userId).includes('admin')
    || (alvo.company_id && quem?.company_id === alvo.company_id && (papeis(userId).includes('company_admin') || temAcao(userId, 'action_manage_users')));
  if (!pode) throw new RpcError('Você não tem permissão para alterar as permissões deste usuário.');

  const antes = store.rows('user_permissions').filter((p) => p.user_id === a.p_user_id).map((p) => ({ ...p }));
  const presetAntes = alvo.permission_preset ?? null;
  db.remove('user_permissions', (p) => p.user_id === a.p_user_id);
  const agora = new Date(agoraMs()).toISOString();
  if (preset !== 'full_access' && Array.isArray(a.p_permissions)) {
    db.insert('user_permissions', [...new Set(a.p_permissions.filter(Boolean))].map((permission) => ({ user_id: a.p_user_id, permission, created_at: agora })));
  }
  db.update('profiles', { id: a.p_user_id }, { permission_preset: preset, updated_at: agora });

  // _assert_company_has_user_manager: com algum usuário ativo, alguém ativo tem de poder gerenciar usuários
  const cid = alvo.company_id;
  const ativos = store.rows('profiles').filter((p) => p.company_id === cid && p.is_active !== false);
  const gestor = ativos.some((p) => papeis(p.id).some((r) => r === 'admin' || r === 'company_admin')
    || (temAcao(p.id, 'screen_configuracoes') && temAcao(p.id, 'action_manage_users')));
  if (cid && ativos.length && !gestor) {
    db.remove('user_permissions', (p) => p.user_id === a.p_user_id);
    if (antes.length) store.table('user_permissions').rows.push(...antes);
    db.update('profiles', { id: a.p_user_id }, { permission_preset: presetAntes });
    throw new RpcError('A empresa ficaria sem ninguém capaz de gerenciar usuários. Mantenha o acesso a Configurações e Gerenciar Usuários para pelo menos um usuário ativo.');
  }
  return undefined;   // returns void
};
