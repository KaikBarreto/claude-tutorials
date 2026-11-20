// Conversão rápida (T11, aba "Conversão"): como a função SQL register_production_atomic (20260829120200): cria a OP já
// "completed" com um lançamento só, posta o estoque pelo mesmo motor das ordens (baixa o insumo, dá entrada no produto) e devolve
// custo total e custo por unidade. Idempotente por client_request_id. Sem coluna do quadro (a conversão não passa pelo Kanban).
import { agoraMs, hojeBR, num } from '../../lib/eco.mjs';
import { postarProducao, recalculaTotais } from '../../lib/producao.mjs';

export default (a, ctx) => {
  const { store, db, RpcError, userId } = ctx;
  if (!a.p_output_material_id) throw new RpcError('p_output_material_id é obrigatório');
  const produzido = num(a.p_produced_qty);
  if (!(produzido > 0)) throw new RpcError('p_produced_qty deve ser > 0');
  const saida = store.rows('materials').find((m) => m.id === a.p_output_material_id);
  if (!saida) throw new RpcError('Produto de saída não encontrado');
  const cid = saida.company_id;
  const cri = String(a.p_client_request_id ?? '').trim() || null;
  if (cri) {
    const ja = store.rows('production_orders').find((o) => o.company_id === cid && o.client_request_id === cri);
    if (ja) return { order_id: ja.id, order_number: ja.order_number, total_material_cost: ja.total_material_cost, cost_per_unit: ja.cost_per_unit, produced_qty: ja.produced_qty, idempotent_skip: true };
  }
  const agora = new Date(agoraMs()).toISOString();
  const numero = store.rows('production_orders').filter((o) => o.company_id === cid).reduce((m, o) => Math.max(m, Number(o.order_number) || 0), 0) + 1;
  const dia = a.p_production_date || hojeBR();
  const ordem = db.insert('production_orders', {
    company_id: cid, order_number: numero, recipe_id: a.p_recipe_id || null, output_material_id: a.p_output_material_id, planned_qty: num(a.p_planned_qty) || produzido,
    produced_qty: produzido, status: 'draft', production_date: dia, responsible: String(a.p_responsible ?? '').trim() || null, client_request_id: cri,
    notes: null, kanban_column_id: null, machine_id: null, employee_id: null, created_by: userId, created_at: agora, updated_at: agora,
  }, { companyId: cid });
  const lanc = db.insert('production_order_entries', {
    production_order_id: ordem.id, company_id: cid, entry_date: dia, produced_qty: produzido, posted: false, note: null, client_request_id: null,
    created_by: userId, created_at: agora, updated_at: agora,
  }, { companyId: cid });
  const post = postarProducao(ctx, ordem, lanc.id, a.p_consumption, a.p_outputs);
  lanc.posted = true;
  lanc.total_material_cost = post.total_material_cost;
  store.table('production_order_entries').touch();
  recalculaTotais(ctx, ordem);
  ordem.status = 'completed';
  ordem.completed_at = agora;
  ordem.cost_per_unit = Math.round((post.total_material_cost / produzido) * 10000) / 10000;
  store.table('production_orders').touch();
  return { order_id: ordem.id, order_number: numero, total_material_cost: post.total_material_cost, cost_per_unit: ordem.cost_per_unit, produced_qty: produzido, movement_ids: post.movement_ids, idempotent_skip: false };
};
