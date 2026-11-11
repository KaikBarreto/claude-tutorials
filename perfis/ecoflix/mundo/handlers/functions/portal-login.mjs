// Edge portal-login (o "Entrar" do "Acesso restrito" do portal público): confere usuário e senha do parceiro (a linha do token ou a do lado
// vinculado) e devolve a sessão de 30 dias que a página guarda em localStorage (portal_session_<token>). Sem senha no portal: session null.
import { parteDoPortal, temModulo } from '../../lib/coletas.mjs';
import { hashSenha, novaSessao } from '../../lib/portal.mjs';

export default async (body, { store, FunctionError }) => {
  const { token, username, password } = body || {};
  if (!token) throw new FunctionError('token', 400, { ok: false, error: 'token' });
  const p = parteDoPortal(store, token);
  if (!p) throw new FunctionError('not_found', 404, { ok: false, error: 'not_found' });
  if (!temModulo(store, p.companyId, 'portal_cliente')) throw new FunctionError('Portal indisponível', 403, { reason: 'portal_module_inactive' });
  if (!p.senha) return { ok: true, session: null };
  await new Promise((r) => setTimeout(r, 400)); // o atraso fixo da função de verdade
  const linhas = [{ row: p.row, tipo: p.tipo }, ...(p.outro ? [{ row: p.outro, tipo: p.tipo === 'customer' ? 'supplier' : 'customer' }] : [])]
    .filter((l) => l.row.portal_password_enabled && l.row.portal_password_hash);
  const ok = linhas.find((l) => typeof username === 'string' && username === l.row.portal_username && hashSenha(l.row.id, password) === l.row.portal_password_hash);
  if (!ok) throw new FunctionError('invalid', 401, { ok: false, error: 'invalid' });
  return { ok: true, session: novaSessao(ok.row.id, ok.tipo) };
};
