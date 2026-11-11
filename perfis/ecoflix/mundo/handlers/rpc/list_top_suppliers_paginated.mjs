// list_top_suppliers_paginated(p_company_id, p_period_start, p_period_end, p_sort_by, p_limit, p_offset): o pódio "Fornecedores por
// compra" da Visão geral de Clientes e Fornecedores (EntitiesSummaryTab.tsx; T4 cap01). Pedidos concluídos do período (datas
// AAAA-MM-DD, inclusive), por parceiro cadastrado: valor, peso líquido, nº de pedidos e o total de parceiros (total_count).
// Ordem: p_sort_by 'value' ou 'quantity', decrescente.
import { pedidos, itensDe, liquido, num, r2, r3 } from '../../lib/eco.mjs';

export function ranking(a, { store, companyId }, tipo) {
  const cid = a.p_company_id || companyId;
  const dia = (v, def) => (v ? String(v).slice(0, 10) : def);
  const j = { d1: dia(a.p_period_start, '0000-01-01'), d2: dia(a.p_period_end, '9999-12-31') };
  const lista = pedidos(store, cid, tipo, j);
  const itens = itensDe(store, tipo, lista);
  const campo = tipo === 'sale' ? 'customer_id' : 'supplier_id';
  const nomes = new Map(store.rows(tipo === 'sale' ? 'customers' : 'suppliers').map((p) => [p.id, p.name]));
  const acc = new Map();
  for (const p of lista) {
    const id = p[campo];
    if (!id) continue;
    const e = acc.get(id) || { id, name: nomes.get(id) || null, value: 0, quantity: 0, n: 0 };
    e.value += num(p.total_amount);
    e.n += 1;
    for (const it of itens.get(p.id) || []) e.quantity += liquido(it);
    acc.set(id, e);
  }
  const chave = a.p_sort_by === 'quantity' ? 'quantity' : 'value';
  const todos = [...acc.values()].sort((x, y) => y[chave] - x[chave] || String(x.name).localeCompare(String(y.name)));
  const ini = num(a.p_offset);
  const fim = ini + (num(a.p_limit) || 5);
  return todos.slice(ini, fim).map((e) => ({
    id: e.id, name: e.name, value: r2(e.value), quantity: r3(e.quantity), [tipo === 'sale' ? 'sales_count' : 'purchases_count']: e.n,
    total_count: todos.length,
  }));
}

export default (a, ctx) => ranking(a, ctx, 'purchase');
