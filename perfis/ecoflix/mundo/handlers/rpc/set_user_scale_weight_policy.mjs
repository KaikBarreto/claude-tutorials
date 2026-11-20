// set_user_scale_weight_policy(p_user_id, p_requires_scale) (app 1.60: migration 20261117124500_scale_weight_lock_per_user): a tela
// chama em toda criação e em todo "Atualizar" do Editar Usuário. null = herdar o padrão da empresa (apaga a exceção); true/false =
// grava a exceção em user_scale_weight_policies e, por compatibilidade, profiles.balanca_exclusiva. Só T02 usa.
import { agoraMs } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, db, userId, RpcError } = ctx;
  const quem = store.rows('profiles').find((p) => p.id === userId);
  if (!quem) throw new RpcError('Usuário não autenticado');
  const alvo = store.rows('profiles').find((p) => p.id === a.p_user_id);
  if (!alvo || !quem.company_id || alvo.company_id !== quem.company_id) throw new RpcError('Usuário não pertence à empresa');
  const papeis = store.rows('user_roles').filter((r) => r.user_id === userId).map((r) => r.role);
  const pode = papeis.includes('admin') || papeis.includes('company_admin') || quem.permission_preset === 'full_access'
    || store.rows('user_permissions').some((p) => p.user_id === userId && p.permission === 'action_manage_users');
  if (!pode) throw new RpcError('Sem permissão para gerenciar usuários');
  const empresa = store.rows('companies').find((c) => c.id === quem.company_id) || {};
  const padrao = !!empresa.scale_weight_lock_enabled;
  const req = a.p_requires_scale ?? null;
  const agora = new Date(agoraMs()).toISOString();
  db.remove('user_scale_weight_policies', (p) => p.user_id === a.p_user_id);
  if (req !== null) {
    db.insert('user_scale_weight_policies', { user_id: a.p_user_id, company_id: quem.company_id, requires_scale: !!req, created_at: agora, updated_at: agora, updated_by: userId });
  }
  db.update('profiles', { id: a.p_user_id }, { balanca_exclusiva: req ?? padrao });
  return { user_id: a.p_user_id, override: req, enabled: req ?? padrao };
};
