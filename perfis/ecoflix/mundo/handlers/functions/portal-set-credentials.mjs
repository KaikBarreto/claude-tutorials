// Edge portal-set-credentials (o "Salvar acesso" / "Remover login" da aba Portal do cadastro; EntityFormDialog.tsx): liga ou desliga a
// senha do portal da linha do parceiro. Ligado com usuário e senha grava usuário e hash; ligado sem senha nova só marca; desligado limpa.
// O hash é o sha256 salgado com o id da linha (lib/portal.mjs); a senha nunca é gravada.
import { hashSenha } from '../../lib/portal.mjs';

export default (body, { store, db, FunctionError }) => {
  const { entityId, entityType, enabled, username, password } = body || {};
  if (!entityId || (entityType !== 'customer' && entityType !== 'supplier')) throw new FunctionError('params', 400, { ok: false });
  const tabela = entityType === 'customer' ? 'customers' : 'suppliers';
  if (!store.rows(tabela).some((r) => r.id === entityId)) throw new FunctionError('forbidden', 403, { ok: false });
  let patch;
  if (enabled) patch = !username || !password ? { portal_password_enabled: true }
    : { portal_password_enabled: true, portal_username: username, portal_password_hash: hashSenha(entityId, password) };
  else patch = { portal_password_enabled: false, portal_username: null, portal_password_hash: null };
  db.update(tabela, { id: entityId }, patch);
  return { ok: true };
};
