// RPC register_inventory_movement(p_inventory_id, p_movement_type, p_quantity, p_supplier_id, p_unit_cost, p_notes,
// p_service_order_id, p_related_movement_id, p_stock_id) · 20261013150000_customer_paid_expenses_and_customer_stock.sql:635-810
// "Caminho atômico único de escrita de estoque": move o saldo do par (material, local) e grava o movimento (Kardex).
// Sem esta RPC a tela diz que registrou e nada muda. Lógica em lib/estoque.mjs (T7; T8 estende).
import { registrarMovimento } from '../../lib/estoque.mjs';

export default async function registerInventoryMovement(a, { userId }) {
  return registrarMovimento({
    inventory_id: a.p_inventory_id, movement_type: a.p_movement_type, quantity: a.p_quantity, supplier_id: a.p_supplier_id,
    unit_cost: a.p_unit_cost, notes: a.p_notes, service_order_id: a.p_service_order_id,
    related_movement_id: a.p_related_movement_id, stock_id: a.p_stock_id,
  }, userId);
}
