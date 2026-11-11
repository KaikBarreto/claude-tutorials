// RPC get_group_financial_dre_summary (20261014084500), a DRE do Financeiro Gerencial: só a dona; empresas do grupo (ou as pedidas, que têm de
// ser do grupo); dia BRT nas duas pontas. Vendas e compras concluídas e não estornadas; despesas e receitas pela régua da DRE, juntadas pelo
// nome da categoria (imposto = nome com "imposto"); regime de competência: CMV = Σ_empresa (estoque no fim da véspera do início + compras -
// estoque no fim do último dia), com saldo e custo médio da _stock_balance_at_date_unchecked; stockCostReliable = nenhuma empresa com saldo
// positivo e custo zero no fechamento. Nada de total escrito: tudo sai da soma das unidades.
import { exigeDono, escopo, diaDoInstante, fimDoDia, vespera, valorNaData, categoriasDoGrupo } from '../../lib/grupo.mjs';
import { r2, num, diaDe } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  exigeDono(ctx, a._group_id);
  const cids = escopo(ctx, a._group_id, a._company_ids);
  if (!cids.length) return {};
  const regime = String(a._regime || 'caixa').toLowerCase();
  const d1 = diaDoInstante(a._start_date);
  const d2 = diaDoInstante(a._end_date);
  const noPeriodo = (p) => cids.includes(p.company_id) && p.status === 'completed' && !p.reverted_at && diaDe(p) >= d1 && diaDe(p) <= d2;
  const vendas = store.rows('sales').filter(noPeriodo);
  const compras = store.rows('purchases').filter(noPeriodo);
  const totalSales = r2(vendas.reduce((s, p) => s + num(p.total_amount), 0));
  const totalPurchases = r2(compras.reduce((s, p) => s + num(p.total_amount), 0));
  const stockValue = r2(store.rows('materials').filter((m) => cids.includes(m.company_id) && !m.is_archived)
    .reduce((s, m) => s + Math.max(0, num(m.current_stock)) * num(m.purchase_price), 0));
  let cmv = null;
  let confiavel = true;
  if (regime === 'competencia') {
    let abre = 0, fecha = 0;
    for (const cid of cids) {
      abre += valorNaData(store, cid, fimDoDia(vespera(d1))).valor;
      const f = valorNaData(store, cid, fimDoDia(d2));
      fecha += f.valor;
      if (!f.confiavel) confiavel = false;
    }
    cmv = r2(abre + totalPurchases - fecha);
  }
  // rankings (5 primeiros), como as CTEs da RPC
  const top = (lista, tab, campo, itens, chave) => {
    const nomes = new Map(store.rows(tab).map((x) => [x.id, x.name]));
    const qtd = new Map();
    for (const it of store.rows(itens)) if (lista.some((p) => p.id === it[chave])) qtd.set(it[chave], (qtd.get(it[chave]) || 0) + num(it.quantity));
    const acc = new Map();
    for (const p of lista) {
      const id = p[campo] || null;
      const e = acc.get(id) || { id, name: id ? nomes.get(id) || null : null, value: 0, quantity: 0, count: 0 };
      e.value += num(p.total_amount); e.quantity += qtd.get(p.id) || 0; e.count += 1;
      acc.set(id, e);
    }
    return [...acc.values()].sort((x, y) => y.value - x.value).slice(0, 5).map((e) => ({ ...e, value: r2(e.value) }));
  };
  const topMat = (lista, itens, chave) => {
    const ids = new Set(lista.map((p) => p.id));
    const mats = new Map(store.rows('materials').map((m) => [m.id, m.name]));
    const acc = new Map();
    for (const it of store.rows(itens)) {
      if (!ids.has(it[chave])) continue;
      const nome = mats.get(it.material_id) || it.material_name;
      const e = acc.get(nome) || { name: nome, quantity: 0, value: 0 };
      e.quantity += num(it.quantity); e.value += num(it.quantity) * num(it.unit_price);
      acc.set(nome, e);
    }
    return [...acc.values()].sort((x, y) => y.value - x.value).slice(0, 5).map((e) => ({ ...e, value: r2(e.value) }));
  };
  const cats = categoriasDoGrupo(store, cids, d1, d2);
  const otherRevenues = r2(cats.revenueCategories.reduce((s, c) => s + c.value, 0));
  const desp = [...cats.operatingExpenses, ...cats.taxExpenses];
  const totDesp = r2(desp.reduce((s, c) => s + c.value, 0));
  return {
    totalSales, totalPurchases, saleCount: vendas.length, purchaseCount: compras.length, otherRevenues,
    operatingExpenses: cats.operatingExpenses, taxExpenses: cats.taxExpenses, revenueCategories: cats.revenueCategories,
    topSuppliers: top(compras, 'suppliers', 'supplier_id', 'purchase_items', 'purchase_id'), topClients: top(vendas, 'customers', 'customer_id', 'sale_items', 'sale_id'),
    topPurchaseMaterials: topMat(compras, 'purchase_items', 'purchase_id'), topSaleMaterials: topMat(vendas, 'sale_items', 'sale_id'),
    stockValue, avgTicketPurchase: compras.length ? totalPurchases / compras.length : 0, avgTicketSale: vendas.length ? totalSales / vendas.length : 0,
    cmv, costBasis: regime === 'competencia' ? 'competencia' : 'caixa', stockCostReliable: regime === 'competencia' ? confiavel : true,
    dreCurrencies: desp.length || cats.revenueCategories.length ? ['BRL'] : [], dreScopeCurrency: desp.length || cats.revenueCategories.length ? 'BRL' : null,
    dreMixedCurrency: false,
    expensesByCurrency: desp.length ? [{ currency: 'BRL', total: totDesp, categories: cats.operatingExpenses, taxes: cats.taxExpenses }] : [],
    revenuesByCurrency: cats.revenueCategories.length ? [{ currency: 'BRL', total: otherRevenues, categories: cats.revenueCategories }] : [],
    orderCurrencies: vendas.length || compras.length ? ['BRL'] : [],
    salesByCurrency: vendas.length ? [{ currency: 'BRL', total: totalSales, count: vendas.length }] : [],
    purchasesByCurrency: compras.length ? [{ currency: 'BRL', total: totalPurchases, count: compras.length }] : [],
  };
};
