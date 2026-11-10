// Exclui a ordem de produção (T11), como a função SQL da 1.59.154 (20260829130100): estorna cada movimento PRODUCAO original da
// OP que ainda não foi estornado (linha nova, tipo PRODUCAO com o sinal invertido, "Estorno de produção (exclusão da OP)", sem
// apagar as originais) e apaga a OP com as filhas (o ON DELETE CASCADE do banco).
import { estornaOrdem } from '../../lib/producao.mjs';

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  if (!a.p_order_id) throw new RpcError('p_order_id é obrigatório');
  const ordem = store.rows('production_orders').find((o) => o.id === a.p_order_id);
  if (!ordem) throw new RpcError('Ordem de produção não encontrada');
  const estornado = estornaOrdem(ctx, ordem);
  const id = ordem.id;
  db.remove('production_order_consumption', (c) => c.production_order_id === id);
  db.remove('production_order_outputs', (o) => o.production_order_id === id);
  db.remove('production_order_workers', (w) => w.order_id === id);
  db.remove('production_order_entries', (e) => e.production_order_id === id);
  db.remove('production_orders', (o) => o.id === id);
  return { order_id: id, status_anterior: ordem.status, estornado };
};
