// RPC set_stock_access(p_stock_id, p_restricted, p_user_ids) → void · 20260814225028_stock_access_acl.sql
// "Salvar acesso": apaga a lista atual; com p_restricted = false o local volta a ser aberto; com true grava só quem pertence à
// empresa do local. Marcar "restrito" SEM marcar ninguém grava lista vazia e o local continua aberto (restrito = haver linhas).
import { RpcError } from '../../http/rest.mjs';
import { ehGestor } from '../../lib/estoque.mjs';

export default async function setStockAccess(a, { userId, db }) {
  const stock = db.first('stocks', { id: a.p_stock_id });
  if (!stock) throw new RpcError(`Estoque nao encontrado: ${a.p_stock_id}`, 'P0002', 404);
  if (!ehGestor(userId)) throw new RpcError('sem permissao para gerenciar acesso deste local', '42501', 403);
  db.remove('stock_access', { stock_id: stock.id });
  if (!a.p_restricted) return;
  const pedidos = new Set(a.p_user_ids || []);
  const validos = [...new Set(db.rows('profiles').filter((p) => p.company_id === stock.company_id && pedidos.has(p.user_id)).map((p) => p.user_id))];
  for (const uid of validos) db.insert('stock_access', { company_id: stock.company_id, stock_id: stock.id, user_id: uid });
}
