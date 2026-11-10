// Lança a produção de UM dia (T11), como a função SQL da 1.59.154 (20260829120100 + 20260829130000): idempotente pelo
// client_request_id, rascunho vira "em andamento", equipe do dia por lançamento, postagem no estoque no dia (padrão) e totais da OP.
import { agoraMs, hojeBR, num } from '../../lib/eco.mjs';
import { empresaDe, postarProducao, sincronizaEquipeDoDia, recalculaTotais } from '../../lib/producao.mjs';

export default (a, ctx) => {
  const { store, db, RpcError, userId } = ctx;
  if (!a.p_order_id) throw new RpcError('p_order_id é obrigatório');
  const ordem = store.rows('production_orders').find((o) => o.id === a.p_order_id);
  if (!ordem) throw new RpcError('Ordem de produção não encontrada');
  const comp = empresaDe(store, ordem.company_id);
  const postaNoDia = comp.production_post_stock_on_entry == null ? true : !!comp.production_post_stock_on_entry;
  const cri = String(a.p_client_request_id ?? '').trim() || null;
  if (cri) {
    const ja = store.rows('production_order_entries').find((e) => e.production_order_id === ordem.id && e.client_request_id === cri);
    if (ja) return { entry_id: ja.id, order_id: ordem.id, idempotent_skip: true };
  }
  if (!['draft', 'in_progress'].includes(ordem.status)) {
    throw new RpcError(`Só é possível lançar produção em OP em rascunho ou em andamento (status=${ordem.status})`);
  }
  const agora = new Date(agoraMs()).toISOString();
  if (ordem.status === 'draft') {
    ordem.status = 'in_progress';
    ordem.updated_at = agora;
    store.table('production_orders').touch();
  }
  const saidas = Array.isArray(a.p_outputs) ? a.p_outputs : [];
  let produzido = saidas.filter((o) => o.is_primary).reduce((s, o) => s + num(o.qty), 0);
  const lanc = db.insert('production_order_entries', {
    production_order_id: ordem.id, company_id: ordem.company_id, entry_date: a.p_entry_date || hojeBR(), produced_qty: produzido, posted: false,
    client_request_id: cri, created_by: userId, created_at: agora, updated_at: agora,
  }, { companyId: ordem.company_id });
  const daEquipe = sincronizaEquipeDoDia(ctx, ordem, lanc.id, a.p_workers, produzido);
  if (daEquipe !== produzido) {
    produzido = daEquipe;
    lanc.produced_qty = produzido;
  }
  let custo = null;
  let postado = false;
  if (postaNoDia) {
    custo = postarProducao(ctx, ordem, lanc.id, a.p_consumption, saidas).total_material_cost;
    postado = true;
  } else {
    // "só ao finalizar": guarda as linhas sem mexer no estoque (custo 0 até a finalização postar)
    for (const c of Array.isArray(a.p_consumption) ? a.p_consumption : []) {
      db.insert('production_order_consumption', {
        production_order_id: ordem.id, entry_id: lanc.id, company_id: ordem.company_id, material_id: c.material_id, theoretical_qty: num(c.theoretical_qty),
        actual_qty: num(c.actual_qty), unit_cost: 0, line_cost: 0, loss_qty: num(c.actual_qty) - num(c.theoretical_qty), loss_reason: c.loss_reason || null, created_at: agora,
      }, { companyId: ordem.company_id });
    }
    for (const o of saidas) {
      if (num(o.qty) <= 0) continue;
      db.insert('production_order_outputs', {
        production_order_id: ordem.id, entry_id: lanc.id, company_id: ordem.company_id, material_id: o.material_id, is_primary: !!o.is_primary, qty: num(o.qty), created_at: agora,
      }, { companyId: ordem.company_id });
    }
  }
  lanc.posted = postado;
  lanc.total_material_cost = custo;
  lanc.updated_at = agora;
  store.table('production_order_entries').touch();
  recalculaTotais(ctx, ordem);
  return { entry_id: lanc.id, order_id: ordem.id, produced_qty: produzido, posted: postado, total_material_cost: custo, idempotent_skip: false };
};
