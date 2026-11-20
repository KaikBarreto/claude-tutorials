// save_user_permissions_and_bank_accounts(p_user_id, p_permissions, p_preset, p_bank_account_ids, p_scale_weight_override) ("Atualizar"
// do Editar Usuário no app 1.60: migrations 20261112224000 e 20261117124500). Chama save_user_permissions (mesmas regras e mesmos
// avisos), depois grava as contas liberadas (só com a restrição "restriction_bank_accounts_selected_only" e perfil que não é
// full_access; senão apaga) e a exceção de peso. Só T02 usa.
import salvar from './save_user_permissions.mjs';
import politica from './set_user_scale_weight_policy.mjs';

export default (a, ctx) => {
  const { store, db, userId, RpcError } = ctx;
  salvar({ p_user_id: a.p_user_id, p_permissions: a.p_permissions, p_preset: a.p_preset ?? null }, ctx);
  const alvo = store.rows('profiles').find((p) => p.id === a.p_user_id);
  if (!alvo?.company_id) throw new RpcError('Usuário sem empresa vinculada.');
  const restrito = (a.p_preset ?? null) !== 'full_access' && (a.p_permissions || []).includes('restriction_bank_accounts_selected_only');
  if (!restrito) {
    db.remove('user_bank_account_access', (r) => r.user_id === a.p_user_id);
  } else {
    const ids = [...new Set((a.p_bank_account_ids || []).filter(Boolean))];
    if (!ids.length) throw new RpcError('Selecione pelo menos uma conta bancária para este usuário.');
    const validas = store.rows('bank_accounts').filter((b) => ids.includes(b.id) && b.company_id === alvo.company_id && b.is_archived === false && (b.kind || 'bank') === 'bank');
    if (validas.length !== ids.length) throw new RpcError('Uma ou mais contas selecionadas não pertencem à empresa, estão arquivadas ou não são contas bancárias.');
    db.remove('user_bank_account_access', (r) => r.user_id === a.p_user_id && !ids.includes(r.bank_account_id));
    const ja = store.rows('user_bank_account_access').filter((r) => r.user_id === a.p_user_id).map((r) => r.bank_account_id);
    const novas = ids.filter((id) => !ja.includes(id));
    if (novas.length) db.insert('user_bank_account_access', novas.map((bank_account_id) => ({ user_id: a.p_user_id, bank_account_id, created_by: userId, created_at: new Date().toISOString() })));
  }
  politica({ p_user_id: a.p_user_id, p_requires_scale: a.p_scale_weight_override ?? null }, ctx);
  return undefined;
};
