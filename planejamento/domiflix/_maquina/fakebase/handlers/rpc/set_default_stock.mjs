// RPC set_default_stock(p_stock_id) → stocks · 20261013150000_customer_paid_expenses_and_customer_stock.sql
// "Definir como principal": só um local geral (sem cliente) por empresa tem is_default = true.
import { RpcError } from '../../http/rest.mjs';

export default async function setDefaultStock(a, { db }) {
  const alvo = db.first('stocks', (s) => s.id === a.p_stock_id && !s.customer_id);
  if (!alvo) throw new RpcError(`Estoque geral não encontrado: ${a.p_stock_id}`, 'P0002', 404);
  db.update('stocks', (s) => s.company_id === alvo.company_id && !s.customer_id && s.is_default && s.id !== alvo.id, { is_default: false });
  db.update('stocks', (s) => s === alvo, { is_default: true });
  return alvo;
}
