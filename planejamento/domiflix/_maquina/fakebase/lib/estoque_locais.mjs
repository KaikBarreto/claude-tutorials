// T8 · estoque por local (presença, transferência, contagem, posição, relatório de compras): o que o banco real faz nas RPCs
// `transfer_stock_between`, `set_inventory_presence`, `set_stock_materials`, `add_group_to_stock`, `receber_ordem_compra`,
// `finalize_inventory_count`, `get_stock_balance_at_date` e `get_material_purchase_report` (migrations 20260814225028,
// 20260930100000, 20260930110000, 20261013150000, 20261018005000 e 20260721170000 da 1.38.9). Estende `lib/estoque.mjs` (T7),
// que continua dono de `registrarMovimento` (escrita atômica do saldo e do Kardex).
import { db } from '../core/db.mjs';
import { arredonda } from './estoque.mjs';

/** Linha de `inventory_stock_levels` do par (material, local) ou null. */
export const nivelDe = (invId, stockId) =>
  db.rows('inventory_stock_levels').find((r) => r.inventory_id === invId && r.stock_id === stockId) || null;

/** `inventory.quantity` = soma dos saldos por local (gatilho trg_sync_inventory_quantity do banco). */
export function espelharQuantidade(invId) {
  const soma = db.find('inventory_stock_levels', { inventory_id: invId }).reduce((s, r) => s + Number(r.quantity || 0), 0);
  db.update('inventory', { id: invId }, { quantity: arredonda(soma) });
}

/**
 * `INSERT ... ON CONFLICT (inventory_id, stock_id) DO UPDATE SET is_present = <presente>`: cria o nível com saldo 0 se faltar,
 * senão só troca a presença (nunca mexe no saldo). Devolve o nível.
 */
export function marcarPresenca(empresa, invId, stockId, presente) {
  const n = nivelDe(invId, stockId);
  if (n) {
    if (n.is_present !== presente) db.update('inventory_stock_levels', (r) => r === n, { is_present: presente });
    return n;
  }
  return db.insert('inventory_stock_levels', {
    company_id: empresa, inventory_id: invId, stock_id: stockId, quantity: 0, min_quantity: null, is_present: presente,
  });
}

/** Ordem do banco para nomes na mensagem da trava `presence_has_balance` (ORDER BY name). */
export const porNome = (a, b) => String(a).localeCompare(String(b), 'pt-BR');

/** Dia (YYYY-MM-DD, UTC) de um instante ISO, como `timestamptz::date` numa sessão UTC. */
export const diaDe = (iso) => (iso ? String(iso).slice(0, 10) : null);
