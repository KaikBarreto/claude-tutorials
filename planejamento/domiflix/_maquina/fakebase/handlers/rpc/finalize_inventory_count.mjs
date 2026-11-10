// RPC finalize_inventory_count(p_count_id, p_notes) → jsonb { count_id, already_finalized, items_adjusted, diff_value }
// 20260721170000_inventario_e_posicao_de_estoque.sql. "Finalizar inventário": para cada item CONTADO com diferença grava um
// movimento 'ajuste' (nota "Inventário #N") levando o saldo ATUAL do local ao valor contado (a base é o saldo de agora, não o
// "esperado" congelado na criação), e marca o inventário como 'finalizado'. Idempotente: se já está finalizado, não reaplica.
import { RpcError } from '../../http/rest.mjs';
import { registrarMovimento } from '../../lib/estoque.mjs';
import { nivelDe } from '../../lib/estoque_locais.mjs';
import { nowIso } from '../../core/util.mjs';

export default async function finalizeInventoryCount(a, { userId, db }) {
  const contagem = db.first('inventory_counts', { id: a.p_count_id });
  if (!contagem) throw new RpcError(`Inventário não encontrado: ${a.p_count_id}`, 'P0002', 404);
  if (contagem.status === 'finalizado') {
    return { count_id: contagem.id, already_finalized: true, items_adjusted: 0, diff_value: 0 };
  }
  if (contagem.status !== 'aberto') throw new RpcError(`Inventário não está aberto (status=${contagem.status})`, '23514');
  if (a.p_notes !== null && a.p_notes !== undefined) db.update('inventory_counts', { id: contagem.id }, { notes: a.p_notes });

  const itens = db.find('inventory_count_items', (i) => i.count_id === contagem.id && i.counted_qty !== null && i.counted_qty !== undefined)
    .sort((x, y) => String(x.inventory_id).localeCompare(String(y.inventory_id)) || String(x.stock_id).localeCompare(String(y.stock_id)));
  let ajustados = 0;
  let valor = 0;
  for (const it of itens) {
    let nivel = nivelDe(it.inventory_id, it.stock_id);
    if (!nivel) nivel = db.insert('inventory_stock_levels', { company_id: contagem.company_id, inventory_id: it.inventory_id, stock_id: it.stock_id, quantity: 0, min_quantity: null, is_present: true });
    const delta = Math.round((Number(it.counted_qty) - Number(nivel.quantity || 0)) * 1e6) / 1e6;
    if (!delta) continue;
    registrarMovimento({
      inventory_id: it.inventory_id, movement_type: 'ajuste', quantity: delta, unit_cost: it.unit_cost,
      notes: `Inventário #${contagem.numero ?? '?'}`, stock_id: it.stock_id,
    }, userId);
    ajustados += 1;
    valor += delta * Number(it.unit_cost || 0);
  }
  db.update('inventory_counts', { id: contagem.id }, { status: 'finalizado', finalized_at: nowIso() });
  return { count_id: contagem.id, already_finalized: false, items_adjusted: ajustados, diff_value: Math.round(valor * 100) / 100 };
}
