// Ranking de materiais comprados/vendidos no período (por valor ou peso), como no card do Dashboard.
import { janela, pedidos, itensDe, liquido, num, r2, r3 } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const tipo = a.p_kind === 'venda' ? 'sale' : 'purchase';
  const lista = pedidos(store, cid, tipo, janela(a.p_start_date, a.p_end_date));
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const acc = new Map();
  for (const its of itensDe(store, tipo, lista).values()) for (const it of its) {
    const e = acc.get(it.material_id) || { material_id: it.material_id, material: mats.get(it.material_id)?.name || it.material_name, unidade: (mats.get(it.material_id)?.unit || 'kg').toLowerCase(), peso: 0, valor: 0 };
    e.peso += liquido(it);
    e.valor += num(it.total_price);
    acc.set(it.material_id, e);
  }
  const chave = a.p_metric === 'peso' ? 'peso' : 'valor';
  const todos = [...acc.values()].sort((x, y) => y[chave] - x[chave]);
  const total = todos.reduce((s, e) => s + e[chave], 0);
  const lim = num(a.p_limit) || 5;
  const top = todos.slice(0, lim);
  const outros = todos.slice(lim).reduce((s, e) => s + e[chave], 0);
  return {
    resultados: top.map((e) => ({ ...e, peso: r3(e.peso), valor: r2(e.valor), percentual: total ? r2((e[chave] / total) * 100) : 0 })),
    total_geral: chave === 'peso' ? r3(total) : r2(total), outros: chave === 'peso' ? r3(outros) : r2(outros),
    outros_percentual: total ? r2((outros / total) * 100) : 0, moeda_escopo: 'BRL', moedas_misturadas: false,
  };
};
