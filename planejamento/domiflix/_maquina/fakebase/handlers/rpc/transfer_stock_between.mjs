// RPC transfer_stock_between(p_inventory_id, p_from_stock, p_to_stock, p_qty, p_notes, p_client_request_id) → SETOF inventory_movements
// 20260814225028_stock_access_acl.sql. Duas pernas no Kardex: saída (−qty) na origem e entrada (+qty) no destino, uma apontando
// para a outra em `related_movement_id`; o destino nasce/vira "presente". Devolve [perna da origem, perna do destino].
import { RpcError } from '../../http/rest.mjs';
import { arredonda, podeAcessarLocal } from '../../lib/estoque.mjs';
import { espelharQuantidade, nivelDe } from '../../lib/estoque_locais.mjs';

export default async function transferStockBetween(a, { userId, db }) {
  const qty = Number(a.p_qty);
  if (!(qty > 0)) throw new RpcError('Quantidade da transferencia deve ser positiva', '23514');
  if (a.p_from_stock === a.p_to_stock) throw new RpcError('Estoque de origem e destino devem ser diferentes', '23514');
  const inv = db.first('inventory', { id: a.p_inventory_id });
  if (!inv) throw new RpcError(`Item de estoque nao encontrado: ${a.p_inventory_id}`, 'P0002', 404);
  for (const sid of [a.p_from_stock, a.p_to_stock]) {
    if (!podeAcessarLocal(userId, sid)) throw new RpcError('sem acesso a este local de estoque', '42501', 403);
  }

  // idempotência: o mesmo client_request_id devolve o par já gravado
  if (a.p_client_request_id) {
    const ja = db.find('inventory_movements', (m) => m.company_id === inv.company_id && m.client_request_id === a.p_client_request_id);
    if (ja.length) {
      const par = db.find('inventory_movements', (m) => m.id === ja[0].id || m.id === ja[0].related_movement_id);
      return par.sort((x, y) => x.quantity - y.quantity);
    }
  }
  for (const sid of [a.p_from_stock, a.p_to_stock]) {
    const s = db.first('stocks', { id: sid });
    if (!s || s.company_id !== inv.company_id) throw new RpcError(`Estoque invalido/de outra empresa: ${sid}`, '42501', 403);
  }

  // níveis: a origem fica como estava; o destino recebe saldo, então nasce presente
  let de = nivelDe(inv.id, a.p_from_stock);
  if (!de) de = db.insert('inventory_stock_levels', { company_id: inv.company_id, inventory_id: inv.id, stock_id: a.p_from_stock, quantity: 0, min_quantity: null, is_present: true });
  let para = nivelDe(inv.id, a.p_to_stock);
  if (!para) para = db.insert('inventory_stock_levels', { company_id: inv.company_id, inventory_id: inv.id, stock_id: a.p_to_stock, quantity: 0, min_quantity: null, is_present: true });

  const deAntes = arredonda(de.quantity || 0);
  const paraAntes = arredonda(para.quantity || 0);
  if (deAntes < qty) throw new RpcError(`Saldo insuficiente no estoque de origem: disponivel ${deAntes}, solicitado ${qty}`, '23514');
  const deDepois = arredonda(deAntes - qty);
  const paraDepois = arredonda(paraAntes + qty);
  db.update('inventory_stock_levels', (r) => r === de, { quantity: deDepois });
  db.update('inventory_stock_levels', (r) => r === para, { quantity: paraDepois, is_present: true });

  const movDe = db.insert('inventory_movements', {
    inventory_id: inv.id, company_id: inv.company_id, stock_id: a.p_from_stock, movement_type: 'transferencia', quantity: -qty,
    stock_before: deAntes, stock_after: deDepois, notes: a.p_notes ?? null, client_request_id: a.p_client_request_id ?? null, created_by: userId,
  });
  const movPara = db.insert('inventory_movements', {
    inventory_id: inv.id, company_id: inv.company_id, stock_id: a.p_to_stock, movement_type: 'transferencia', quantity: qty,
    stock_before: paraAntes, stock_after: paraDepois, notes: a.p_notes ?? null, related_movement_id: movDe.id, created_by: userId,
  });
  movDe.related_movement_id = movPara.id; // fecha o vínculo nos dois sentidos
  espelharQuantidade(inv.id);
  return [movDe, movPara];
}
