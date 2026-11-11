// Ranking de fornecedores (compra) ou clientes (venda) no período, por valor ou peso. Compra de balcão (sem cadastro)
// entra como "Sem cadastro" (como a função SQL: COALESCE(nome, 'Sem cadastro'); T25).
import { janela, pedidos, itensDe, liquido, num, r2, r3 } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const tipo = a.p_kind === 'venda' ? 'sale' : 'purchase';
  const lista = pedidos(store, cid, tipo, janela(a.p_start_date, a.p_end_date));
  const itens = itensDe(store, tipo, lista);
  const nomes = new Map(store.rows(tipo === 'sale' ? 'customers' : 'suppliers').map((p) => [p.id, p.name]));
  const acc = new Map();
  for (const p of lista) {
    const pid = (tipo === 'sale' ? p.customer_id : p.supplier_id) || null;
    const e = acc.get(pid) || { parceiro_id: pid, parceiro: pid ? nomes.get(pid) : 'Sem cadastro', peso: 0, valor: 0 };
    e.valor += num(p.total_amount);
    for (const it of itens.get(p.id) || []) e.peso += liquido(it);
    acc.set(pid, e);
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
