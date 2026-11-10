// Ajudantes de estoque (T7; o T8 reaproveita): a escrita atômica do saldo por local que o banco real faz em
// `register_inventory_movement` (20261013150000_customer_paid_expenses_and_customer_stock.sql:635-810) e a ACL por local
// (`can_access_stock`, 20260814225028_stock_access_acl.sql).
//  - `p_quantity` é o DELTA ASSINADO: entrada positiva; consumo e saída negativos; estorno positivo.
//  - cria a linha de `inventory_stock_levels` do par (material, local) se faltar e marca `is_present`;
//  - `inventory.quantity` reflete a SOMA dos locais (gatilho `trg_sync_inventory_quantity`);
//  - a linha de `inventory_movements` guarda `stock_before`/`stock_after` e o autor (`created_by`).
import { db } from '../core/db.mjs';
import { RpcError } from '../http/rest.mjs';

export const TIPOS_MOVIMENTO = new Set(['entrada', 'saida', 'ajuste', 'transferencia', 'estorno', 'consumo']);

export const arredonda = (n) => Math.round(Number(n) * 1e6) / 1e6;

/** admin ou gestor (is_admin_or_gestor): no mundo falso a tabela user_roles só tem 'admin' e 'tecnico'. */
export function ehGestor(userId) {
  return db.find('user_roles', { user_id: userId }).some((r) => ['admin', 'gestor', 'super_admin'].includes(r.role));
}

/** can_access_stock: gestor vê tudo; local sem nenhuma linha em stock_access é aberto; senão só quem está na lista. */
export function podeAcessarLocal(userId, stockId) {
  if (ehGestor(userId)) return true;
  const regras = db.find('stock_access', { stock_id: stockId });
  return regras.length === 0 || regras.some((r) => r.user_id === userId);
}

/** Local padrão do material: o `is_default` da empresa (estoque geral) ou o local do cliente dono do material. */
function localPadraoDoMaterial(inv) {
  return db.rows('stocks').find((s) => s.company_id === inv.company_id && (inv.customer_id ? s.customer_id === inv.customer_id : !s.customer_id && s.is_default)) || null;
}

/**
 * Registra um movimento e ajusta o saldo. Devolve a linha de `inventory_movements`.
 * `a` usa os nomes dos parâmetros da RPC (sem o prefixo p_): inventory_id, movement_type, quantity, supplier_id, unit_cost,
 * notes, service_order_id, related_movement_id, stock_id.
 */
export function registrarMovimento(a, userId) {
  if (!TIPOS_MOVIMENTO.has(a.movement_type)) throw new RpcError(`Tipo de movimento inválido: ${a.movement_type}`, '23514');
  const delta = Number(a.quantity);
  if (!delta) throw new RpcError('A quantidade do movimento deve ser diferente de zero.', '22023');
  const inv = db.first('inventory', { id: a.inventory_id });
  if (!inv) throw new RpcError(`Item de estoque não encontrado: ${a.inventory_id}`, 'P0002', 404);
  if (inv.archived_at) throw new RpcError('Material arquivado não pode ser movimentado.', '23514');

  let stock = a.stock_id ? db.first('stocks', { id: a.stock_id }) : localPadraoDoMaterial(inv);
  if (!stock) throw new RpcError('Não existe local de estoque compatível com o material.', 'P0002', 404);
  if (stock.company_id !== inv.company_id || (stock.customer_id || null) !== (inv.customer_id || null)) {
    throw new RpcError('Material e local de estoque não pertencem ao mesmo tenant/cliente.', '42501', 403);
  }
  if (!podeAcessarLocal(userId, stock.id)) throw new RpcError('Sem acesso a este local de estoque.', '42501', 403);

  if (a.service_order_id) {
    const os = db.first('service_orders', { id: a.service_order_id });
    if (!os || os.company_id !== inv.company_id) throw new RpcError('Ordem de serviço não pertence à empresa do movimento.', '42501', 403);
    if (inv.customer_id && inv.customer_id !== os.customer_id) {
      throw new RpcError('Estoque de cliente só pode ser consumido em OS do mesmo cliente.', '42501', 403);
    }
    if (!(ehGestor(userId) || os.technician_id === userId || os.created_by === userId)) {
      throw new RpcError('Sem permissão para movimentar materiais desta OS.', '42501', 403);
    }
  }

  let nivel = db.first('inventory_stock_levels', (r) => r.inventory_id === inv.id && r.stock_id === stock.id);
  if (!nivel) {
    nivel = db.insert('inventory_stock_levels', { company_id: inv.company_id, inventory_id: inv.id, stock_id: stock.id, quantity: 0, min_quantity: null, is_present: true });
  } else if (!nivel.is_present) {
    db.update('inventory_stock_levels', (r) => r === nivel, { is_present: true });
  }
  const antes = arredonda(nivel.quantity || 0);
  const depois = arredonda(antes + delta);
  db.update('inventory_stock_levels', (r) => r === nivel, { quantity: depois });
  const soma = db.find('inventory_stock_levels', { inventory_id: inv.id }).reduce((s, r) => s + Number(r.quantity || 0), 0);
  db.update('inventory', { id: inv.id }, { quantity: arredonda(soma) });

  return db.insert('inventory_movements', {
    inventory_id: inv.id, company_id: inv.company_id, customer_id: inv.customer_id || null, stock_id: stock.id,
    movement_type: a.movement_type, quantity: delta, stock_before: antes, stock_after: depois,
    supplier_id: a.supplier_id || null, unit_cost: a.unit_cost ?? null, notes: a.notes ?? null,
    service_order_id: a.service_order_id || null, related_movement_id: a.related_movement_id || null, created_by: userId,
  });
}
