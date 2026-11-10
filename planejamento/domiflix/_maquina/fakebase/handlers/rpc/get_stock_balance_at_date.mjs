// RPC get_stock_balance_at_date(p_at, p_stock_ids) → TABLE · 20261013150000_customer_paid_expenses_and_customer_stock.sql
// "Posição de Estoque": o saldo de cada (local, material) numa data = SOMA do Kardex até p_at (inclusive), só locais que o
// usuário acessa, descartando saldo zero. O valor usa o custo/preço CADASTRADO HOJE (não o do dia escolhido).
// Ordem do banco: nome do local, SKU (numérico antes de texto; sem SKU por último), nome do material.
import { RpcError } from '../../http/rest.mjs';
import { podeAcessarLocal } from '../../lib/estoque.mjs';

export default async function getStockBalanceAtDate(a, { userId, db }) {
  if (!a.p_at) throw new RpcError('p_at é obrigatório', 'P0001');
  const ate = Date.parse(a.p_at);
  const filtro = Array.isArray(a.p_stock_ids) && a.p_stock_ids.length ? new Set(a.p_stock_ids) : null;
  const locais = new Map(db.rows('stocks').map((s) => [s.id, s]));
  const materiais = new Map(db.rows('inventory').map((i) => [i.id, i]));
  const soma = new Map();
  for (const m of db.rows('inventory_movements')) {
    if (m.customer_id) continue;
    const s = locais.get(m.stock_id);
    const i = materiais.get(m.inventory_id);
    if (!s || !i || s.customer_id || i.customer_id || i.archived_at) continue;
    if (Date.parse(m.created_at) > ate) continue;
    if (filtro && !filtro.has(m.stock_id)) continue;
    if (!podeAcessarLocal(userId, s.id)) continue;
    const k = `${m.stock_id}|${m.inventory_id}`;
    soma.set(k, (soma.get(k) || 0) + Number(m.quantity || 0));
  }
  const rows = [];
  for (const [k, saldo] of soma) {
    const r = Math.round(saldo * 1e6) / 1e6;
    if (!r) continue;
    const [sid, iid] = k.split('|');
    const s = locais.get(sid);
    const i = materiais.get(iid);
    const custo = Number(i.cost_price || 0);
    const venda = Number(i.sale_price || 0);
    rows.push({
      stock_id: sid, stock_name: s.name, inventory_id: iid, sku: i.sku ?? null, name: i.name, unit: i.unit, saldo: r,
      cost_price: custo, sale_price: venda, valor: Math.round(r * custo * 1e6) / 1e6, projecao: Math.round(r * venda * 1e6) / 1e6,
    });
  }
  const numerico = (v) => (/^[0-9]+$/.test(v || '') ? Number(v) : null);
  rows.sort((x, y) => {
    const porLocal = String(x.stock_name).localeCompare(String(y.stock_name), 'pt-BR');
    if (porLocal) return porLocal;
    const nx = numerico(x.sku);
    const ny = numerico(y.sku);
    if (nx !== null || ny !== null) { // NULLS LAST na chave numérica
      if (nx === null) return 1;
      if (ny === null) return -1;
      if (nx !== ny) return nx - ny;
    }
    if (x.sku !== y.sku) { // texto: NULL por último
      if (x.sku === null) return 1;
      if (y.sku === null) return -1;
      return String(x.sku).localeCompare(String(y.sku), 'pt-BR');
    }
    return String(x.name).localeCompare(String(y.name), 'pt-BR');
  });
  return rows;
}
