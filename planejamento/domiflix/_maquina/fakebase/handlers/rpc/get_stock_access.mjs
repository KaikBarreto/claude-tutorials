// RPC get_stock_access(p_stock_id) → jsonb { restricted, user_ids } · 20260814225028_stock_access_acl.sql
// Aba "Acesso" de "Configurar <local>". "Restrito" é DERIVADO de haver linhas em `stock_access` (zero linhas = local aberto).
// Só admin/gestor consulta.
import { RpcError } from '../../http/rest.mjs';
import { ehGestor } from '../../lib/estoque.mjs';

export default async function getStockAccess(a, { userId, db }) {
  const stock = db.first('stocks', { id: a.p_stock_id });
  if (!stock) throw new RpcError(`Estoque nao encontrado: ${a.p_stock_id}`, 'P0002', 404);
  if (!ehGestor(userId)) throw new RpcError('sem permissao para gerenciar acesso deste local', '42501', 403);
  const ids = db.find('stock_access', { stock_id: stock.id })
    .sort((x, y) => String(x.created_at).localeCompare(String(y.created_at)))
    .map((r) => r.user_id);
  return { restricted: ids.length > 0, user_ids: ids };
}
