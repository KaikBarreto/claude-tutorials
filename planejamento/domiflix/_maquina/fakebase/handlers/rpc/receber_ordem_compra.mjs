// RPC receber_ordem_compra(p_ordem_id, p_itens) → jsonb · 20260930110000_compras_ordem_de_compra.sql
// "Registrar recebimento" da ordem de compra: p_itens = [{ item_id, quantity }] (só o que chegou AGORA). Para cada linha:
//  - teto: recebido + agora não pode passar do pedido ("receipt_exceeds_ordered: <material>");
//  - entrada no local da requisição (compras.stock_id; sem local, o principal) pelo caminho único `registrarMovimento`,
//    com o fornecedor da ordem, o preço da linha e a nota "Recebimento da O.C. #N";
//  - soma em `quantity_received`.
// Depois recalcula o status pelo estado real dos itens: tudo recebido = 'recebida' (carimba received_at); senão 'recebida_parcial'.
// Não cria despesa (a compra direta é que amarra o Financeiro).
import { RpcError } from '../../http/rest.mjs';
import { registrarMovimento } from '../../lib/estoque.mjs';
import { nowIso } from '../../core/util.mjs';

export default async function receberOrdemCompra(a, { userId, db }) {
  if (!a.p_ordem_id) throw new RpcError('payload_invalido: p_ordem_id obrigatorio', '22023');
  if (!Array.isArray(a.p_itens)) throw new RpcError('payload_invalido: p_itens deve ser um array de objetos com item_id e quantity', '22023');
  const ordem = db.first('compra_ordens', { id: a.p_ordem_id });
  if (!ordem) throw new RpcError(`Ordem de compra nao encontrada: ${a.p_ordem_id}`, 'P0002', 404);
  if (ordem.status === 'cancelada') throw new RpcError(`ordem_cancelada: a O.C. #${ordem.numero} foi cancelada e nao aceita recebimento`, '23514');
  const compra = db.first('compras', { id: ordem.compra_id });
  const stockId = compra?.stock_id || null;

  let tocados = 0;
  let qtdTotal = 0;
  for (const e of a.p_itens) {
    const itemId = e?.item_id || null;
    const qtd = Number(e?.quantity ?? 0);
    if (!itemId || !(qtd > 0)) continue;
    const item = db.first('compra_ordem_itens', (r) => r.id === itemId && r.ordem_id === ordem.id);
    if (!item) throw new RpcError(`payload_invalido: item ${itemId} nao pertence a O.C. #${ordem.numero}`, '22023');
    if (Number(item.quantity_received || 0) + qtd > Number(item.quantity_ordered)) {
      throw new RpcError(`receipt_exceeds_ordered: ${String(item.material_name || '').trim() || 'Material'}`, '23514');
    }

    let inventoryId = item.inventory_id;
    if (!inventoryId) { // material manual: nasce no estoque da empresa antes da entrada
      const novo = db.insert('inventory', {
        company_id: ordem.company_id, name: String(item.material_name || '').trim() || 'Material',
        unit: String(item.unit || '').trim() || 'un', cost_price: item.unit_price ?? 0, quantity: 0,
      });
      inventoryId = novo.id;
      db.update('compra_ordem_itens', { id: item.id }, { inventory_id: inventoryId });
      if (item.compra_material_id) db.update('compra_materiais', (m) => m.id === item.compra_material_id && !m.inventory_id, { inventory_id: inventoryId });
    }

    registrarMovimento({
      inventory_id: inventoryId, movement_type: 'entrada', quantity: qtd, supplier_id: ordem.supplier_id,
      unit_cost: item.unit_price, notes: `Recebimento da O.C. #${ordem.numero}`, stock_id: stockId,
    }, userId);
    db.update('compra_ordem_itens', { id: item.id }, { quantity_received: Number(item.quantity_received || 0) + qtd });
    tocados += 1;
    qtdTotal += qtd;
  }

  const itens = db.find('compra_ordem_itens', { ordem_id: ordem.id });
  const pendentes = itens.filter((i) => Number(i.quantity_received || 0) < Number(i.quantity_ordered)).length;
  let status = ordem.status;
  if (itens.length > 0 && pendentes === 0) {
    db.update('compra_ordens', { id: ordem.id }, { status: 'recebida', received_at: ordem.received_at || nowIso() });
    status = 'recebida';
  } else if (tocados > 0) {
    db.update('compra_ordens', { id: ordem.id }, { status: 'recebida_parcial' });
    status = 'recebida_parcial';
  }
  return {
    ordem_id: ordem.id, numero: ordem.numero, status, itens_recebidos: tocados, quantidade_total: qtdTotal,
    itens_pendentes: pendentes, stock_id: stockId,
  };
}
