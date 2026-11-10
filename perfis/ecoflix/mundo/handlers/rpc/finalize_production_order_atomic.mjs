// Finaliza a ordem de produção (T11), como a função SQL da 1.59.154 (20260829120100): idempotente pelo client_request_id, exige
// ao menos um lançamento, posta o que ficou sem postar ("só ao finalizar"), recalcula os totais e marca "completed".
// O cliente move o cartão para a coluna de conclusão depois (FinalizeProductionDialog).
import { agoraMs } from '../../lib/eco.mjs';
import { postarProducao, recalculaTotais } from '../../lib/producao.mjs';

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  if (!a.p_order_id) throw new RpcError('p_order_id é obrigatório');
  const cri = String(a.p_client_request_id ?? '').trim() || null;
  const ordem = store.rows('production_orders').find((o) => o.id === a.p_order_id);
  if (!ordem) throw new RpcError('Ordem de produção não encontrada');
  if (cri && ordem.client_request_id === cri && ordem.status === 'completed') return { order_id: ordem.id, idempotent_skip: true };
  if (!['draft', 'in_progress'].includes(ordem.status)) throw new RpcError(`Ordem já finalizada ou cancelada (status=${ordem.status})`);
  const lanc = store.rows('production_order_entries').filter((e) => e.production_order_id === ordem.id);
  if (!lanc.length) throw new RpcError('Não é possível finalizar uma OP sem nenhum lançamento de produção');
  for (const e of lanc.filter((x) => !x.posted).sort((x, y) => String(x.entry_date).localeCompare(String(y.entry_date)) || String(x.created_at).localeCompare(String(y.created_at)))) {
    const cons = store.rows('production_order_consumption').filter((c) => c.entry_id === e.id)
      .map((c) => ({ material_id: c.material_id, theoretical_qty: c.theoretical_qty, actual_qty: c.actual_qty, loss_reason: c.loss_reason }));
    const outs = store.rows('production_order_outputs').filter((o) => o.entry_id === e.id).map((o) => ({ material_id: o.material_id, qty: o.qty, is_primary: o.is_primary }));
    db.remove('production_order_consumption', (c) => c.entry_id === e.id);
    db.remove('production_order_outputs', (o) => o.entry_id === e.id);
    e.total_material_cost = postarProducao(ctx, ordem, e.id, cons, outs).total_material_cost;
    e.posted = true;
    store.table('production_order_entries').touch();
  }
  recalculaTotais(ctx, ordem);
  const agora = new Date(agoraMs()).toISOString();
  ordem.status = 'completed';
  ordem.completed_at = agora;
  ordem.client_request_id = cri || ordem.client_request_id || null;
  ordem.updated_at = agora;
  store.table('production_orders').touch();
  return { order_id: ordem.id, produced_qty: ordem.produced_qty, entry_count: lanc.length, idempotent_skip: false };
};
