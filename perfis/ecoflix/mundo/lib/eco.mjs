// Contas do mundo da EcoFlix usadas pelos handlers (o que as funções SQL do EcoSistema fazem, em memória).
// Fuso: America/Sao_Paulo (-03:00, sem horário de verão). Datas lógicas dos pedidos: transaction_date/transaction_at.
export const r2 = (n) => Math.round((Number(n) || 0) * 100) / 100;
export const r3 = (n) => Math.round((Number(n) || 0) * 1000) / 1000;
export const num = (v) => Number(v) || 0;

/** "Agora" do mundo em ms: o relógio do Supabase falso (FAKE_NOW, correndo desde o último reset). */
export function agoraMs() {
  if (globalThis.__fakebaseAgora) return globalThis.__fakebaseAgora();
  const d = process.env.FAKE_NOW ? new Date(process.env.FAKE_NOW) : null;
  return d && !Number.isNaN(d.getTime()) ? d.getTime() : Date.now();
}
const pad = (n) => String(n).padStart(2, '0');
/** Dia (AAAA-MM-DD) de um instante em Brasília. */
export function diaBR(iso) {
  const t = new Date(typeof iso === 'number' ? iso : iso || agoraMs());
  if (Number.isNaN(t.getTime())) return null;
  const b = new Date(t.getTime() - 3 * 3600000);
  return `${b.getUTCFullYear()}-${pad(b.getUTCMonth() + 1)}-${pad(b.getUTCDate())}`;
}
export const hojeBR = () => diaBR(agoraMs());
/** Hora (0-23) e dia da semana (0 domingo) de um instante em Brasília. */
export function horaBR(iso) {
  const b = new Date(new Date(iso).getTime() - 3 * 3600000);
  return { hora: b.getUTCHours(), dow: b.getUTCDay() };
}
export const addDias = (d, n) => {
  const t = new Date(`${d}T12:00:00Z`);
  t.setUTCDate(t.getUTCDate() + n);
  return t.toISOString().slice(0, 10);
};
/** Data lógica de uma linha (transaction_date ou o dia BRT de transaction_at/created_at). */
export const diaDe = (r) => r.transaction_date || diaBR(r.transaction_at || r.created_at);
/** Janela de dias [ini, fim] (inclusive) a partir de dois instantes (como as RPCs: dia BRT de cada ponta). */
export function janela(ini, fim) {
  return { d1: ini ? diaBR(ini) : '0000-01-01', d2: fim ? diaBR(fim) : '9999-12-31' };
}
export const naJanela = (r, j) => {
  const d = diaDe(r);
  return d >= j.d1 && d <= j.d2;
};

/** Pedidos concluídos (compra ou venda) da empresa na janela. */
export function pedidos(store, cid, tipo, j) {
  const t = tipo === 'purchase' || tipo === 'compra' ? 'purchases' : 'sales';
  return store.rows(t).filter((p) => p.company_id === cid && p.status === 'completed' && (!j || naJanela(p, j)));
}
/** Itens de uma lista de pedidos: Map pedidoId -> [itens]. */
export function itensDe(store, tipo, lista) {
  const isC = tipo === 'purchase' || tipo === 'compra';
  const ids = new Set(lista.map((p) => p.id));
  const m = new Map();
  for (const it of store.rows(isC ? 'purchase_items' : 'sale_items')) {
    const oid = isC ? it.purchase_id : it.sale_id;
    if (!ids.has(oid)) continue;
    if (!m.has(oid)) m.set(oid, []);
    m.get(oid).push(it);
  }
  return m;
}
export const liquido = (it) => num(it.quantity) - num(it.impurity);

export function materiais(store, cid) {
  return store.rows('materials').filter((m) => m.company_id === cid);
}
export function nomeParceiro(store, tipo, id) {
  if (!id) return null;
  const t = tipo === 'purchase' || tipo === 'supplier' ? 'suppliers' : 'customers';
  return store.rows(t).find((x) => x.id === id)?.name || null;
}

/** Custo médio ponderado de compra por material (até um dia, inclusive). */
export function custoMedio(store, cid, ateDia = '9999-12-31') {
  const acc = new Map();
  const compras = pedidos(store, cid, 'purchase').filter((p) => diaDe(p) <= ateDia);
  const itens = itensDe(store, 'purchase', compras);
  for (const lst of itens.values()) {
    for (const it of lst) {
      const a = acc.get(it.material_id) || { q: 0, v: 0 };
      a.q += liquido(it);
      a.v += num(it.total_price);
      acc.set(it.material_id, a);
    }
  }
  const out = new Map();
  for (const m of materiais(store, cid)) {
    const a = acc.get(m.id);
    out.set(m.id, a && a.q > 0 ? a.v / a.q : num(m.purchase_price));
  }
  return out;
}
/** Valor do estoque atual (saldo x custo médio). */
export function valorEstoque(store, cid) {
  const cm = custoMedio(store, cid);
  return r2(materiais(store, cid).filter((m) => !m.is_archived).reduce((s, m) => s + Math.max(0, num(m.current_stock)) * (cm.get(m.id) || 0), 0));
}

// ---------------------------------------------------------------- dinheiro
export const SINAL_CAIXA = { sale: 1, purchase: -1, deposit: 1, withdrawal: -1, expense: -1, adjustment: 1 };
export const sinalCaixa = (t) => SINAL_CAIXA[t.type] !== undefined ? SINAL_CAIXA[t.type] * num(t.amount) * (t.type === 'adjustment' ? 1 : 1) : 0;
/** Saldo de uma conta: cofre (kind cash) = gaveta (cash_transactions sem opening/closing/transfer) + perna banco. */
export function saldoConta(store, cid, conta) {
  const banco = store.rows('bank_transactions').filter((b) => b.bank_account_id === conta.id).reduce((s, b) => s + num(b.amount), 0);
  if (conta.kind !== 'cash') return r2(banco);
  const gaveta = store.rows('cash_transactions')
    .filter((c) => c.company_id === cid && !['opening', 'closing', 'transfer'].includes(c.type))
    .reduce((s, c) => s + (SINAL_CAIXA[c.type] || 0) * num(c.amount), 0);
  return r2(gaveta + banco);
}
export const contas = (store, cid) => store.rows('bank_accounts').filter((b) => b.company_id === cid && !b.is_archived);
export const cofre = (store, cid) => contas(store, cid).find((b) => b.kind === 'cash') || null;
/** Saldo da gaveta de um caixa: abertura + entradas - saídas (sem fechamento). */
export function saldoCaixa(store, caixa) {
  let s = 0;
  for (const t of store.rows('cash_transactions')) {
    if (t.cash_register_id !== caixa.id || t.type === 'closing') continue;
    s += t.type === 'opening' ? num(t.amount) : (SINAL_CAIXA[t.type] || 0) * num(t.amount);
  }
  return r2(s);
}

// ---------------------------------------------------------------- DRE
/** Lançamentos de resultado (fora pedidos, transferências, ajustes e o que foi tirado da DRE) na janela. */
export function lancamentosResultado(store, cid, j) {
  const out = [];
  for (const c of store.rows('cash_transactions')) {
    if (c.company_id !== cid || c.excluded_from_dre || c.order_id || c.partner_id || !naJanela(c, j)) continue;
    if (c.type === 'expense' || c.type === 'withdrawal') out.push({ ...c, valor: num(c.amount), natureza: 'expense' });
    else if (c.type === 'deposit') out.push({ ...c, valor: num(c.amount), natureza: 'income' });
  }
  for (const b of store.rows('bank_transactions')) {
    if (b.company_id !== cid || b.excluded_from_dre || b.order_id || b.partner_id || b.group_id || b.type === 'transfer' || !naJanela(b, j)) continue;
    if (b.type === 'expense' || b.type === 'withdrawal') out.push({ ...b, valor: Math.abs(num(b.amount)), natureza: 'expense' });
    else if (b.type === 'deposit') out.push({ ...b, valor: Math.abs(num(b.amount)), natureza: 'income' });
  }
  return out;
}
/** Categorias da DRE: [{ name, value, color, costCenters }] por natureza (expense | income). */
export function categoriasDRE(store, cid, j) {
  const cats = new Map(store.rows('financial_categories').filter((c) => c.company_id === cid).map((c) => [c.id, c]));
  const ccs = new Map(store.rows('cost_centers').filter((c) => c.company_id === cid).map((c) => [c.id, c]));
  const grupos = { expense: new Map(), income: new Map(), tax: new Map() };
  for (const l of lancamentosResultado(store, cid, j)) {
    const cat = cats.get(l.category_id);
    const nat = cat?.dre_group === 'impostos' ? 'tax' : l.natureza;
    const nome = cat?.name || 'Sem categoria';
    const g = grupos[nat];
    if (!g.has(nome)) g.set(nome, { name: nome, value: 0, color: cat?.color || '#9CA3AF', cc: new Map() });
    const e = g.get(nome);
    e.value += l.valor;
    const cc = ccs.get(l.cost_center_id);
    const k = cc?.id || null;
    if (!e.cc.has(k)) e.cc.set(k, { id: k, name: cc?.name || 'Sem centro de custo', color: cc?.color || '#9CA3AF', value: 0 });
    e.cc.get(k).value += l.valor;
  }
  const lista = (g) => [...g.values()].map((e) => ({ name: e.name, value: r2(e.value), color: e.color, costCenters: [...e.cc.values()].map((c) => ({ ...c, value: r2(c.value) })).sort((a, b) => b.value - a.value) })).sort((a, b) => b.value - a.value);
  return { despesas: lista(grupos.expense), receitas: lista(grupos.income), impostos: lista(grupos.tax) };
}
/** Resumo da DRE (get_financial_dre_summary) na janela. */
export function resumoDRE(store, cid, j, regime = 'caixa') {
  const compras = pedidos(store, cid, 'purchase', j);
  const vendas = pedidos(store, cid, 'sale', j);
  const totalPurchases = r2(compras.reduce((s, p) => s + num(p.total_amount), 0));
  const totalSales = r2(vendas.reduce((s, p) => s + num(p.total_amount), 0));
  let cmv = 0;
  if (regime === 'competencia') {
    const cm = custoMedio(store, cid, j.d2);
    for (const lst of itensDe(store, 'sale', vendas).values()) for (const it of lst) cmv += liquido(it) * (cm.get(it.material_id) || 0);
  }
  const { despesas, receitas, impostos } = categoriasDRE(store, cid, j);
  const otherRevenues = r2(receitas.reduce((s, c) => s + c.value, 0));
  // rankings e tickets médios (Relatório Financeiro > Indicadores operacionais)
  const topParceiros = (tipo, lista) => {
    const nomes = new Map(store.rows(tipo === 'sale' ? 'customers' : 'suppliers').map((p) => [p.id, p.name]));
    const its = itensDe(store, tipo, lista);
    const acc = new Map();
    for (const p of lista) {
      const pid = (tipo === 'sale' ? p.customer_id : p.supplier_id) || null;
      const e = acc.get(pid) || { id: pid, name: pid ? nomes.get(pid) : tipo === 'sale' ? 'Sem cliente' : 'Sem fornecedor', value: 0, count: 0, quantity: 0 };
      e.value += num(p.total_amount); e.count += 1;
      for (const it of its.get(p.id) || []) e.quantity += liquido(it);
      acc.set(pid, e);
    }
    return [...acc.values()].sort((x, y) => y.value - x.value).slice(0, 10).map((e) => ({ ...e, value: r2(e.value), quantity: r3(e.quantity) }));
  };
  const topMateriais = (tipo, lista) => {
    const mats = new Map(store.rows('materials').map((m) => [m.id, m.name]));
    const acc = new Map();
    for (const lst of itensDe(store, tipo, lista).values()) for (const it of lst) {
      const e = acc.get(it.material_id) || { name: mats.get(it.material_id) || it.material_name, value: 0, quantity: 0 };
      e.value += num(it.total_price); e.quantity += liquido(it);
      acc.set(it.material_id, e);
    }
    return [...acc.values()].sort((x, y) => y.value - x.value).slice(0, 10).map((e) => ({ ...e, value: r2(e.value), quantity: r3(e.quantity) }));
  };
  return {
    totalSales, totalPurchases, cmv: r2(cmv), costBasis: regime === 'competencia' ? 'competencia' : 'caixa',
    avgTicketPurchase: compras.length ? r2(totalPurchases / compras.length) : 0, avgTicketSale: vendas.length ? r2(totalSales / vendas.length) : 0,
    topSuppliers: topParceiros('purchase', compras), topClients: topParceiros('sale', vendas),
    topPurchaseMaterials: topMateriais('purchase', compras), topSaleMaterials: topMateriais('sale', vendas), stockCostReliable: true,
    otherRevenues, purchaseCount: compras.length, saleCount: vendas.length, stockValue: valorEstoque(store, cid),
    operatingExpenses: despesas, taxExpenses: impostos, revenueCategories: receitas,
    dreMixedCurrency: false, dreScopeCurrency: 'BRL', expensesByCurrency: [], revenuesByCurrency: [],
    orderCurrencies: compras.length || vendas.length ? ['BRL'] : [],
    salesByCurrency: vendas.length ? [{ currency: 'BRL', total: totalSales, count: vendas.length }] : [],
    purchasesByCurrency: compras.length ? [{ currency: 'BRL', total: totalPurchases, count: compras.length }] : [],
  };
}

/** Pagamentos de um pedido: dinheiro, banco e saldo (como get_orders_with_payments). */
export function pagamentosDoPedido(store, p, tipo) {
  const ct = tipo === 'sale' ? 'sale' : 'purchase';
  const cash = store.rows('cash_transactions').filter((c) => c.order_id === p.id && c.type === ct && num(c.amount) > 0);
  const bank = store.rows('bank_transactions').filter((b) => b.order_id === p.id);
  const bal = store.rows('balance_movements').filter((b) => b.order_id === p.id && b.movement_type === 'order');
  return { cash, bank, bal };
}

/** Próximo número de pedido (compartilhado entre compra e venda, como get_next_order_number). */
export function proximoNumero(store, cid) {
  let mx = 0;
  for (const t of ['purchases', 'sales']) for (const p of store.rows(t)) if (p.company_id === cid && num(p.order_number) > mx) mx = num(p.order_number);
  return mx + 1;
}

/** Linhas da DRE (get_dre_expense_lines / get_dre_revenue_lines): um lançamento por linha, com totais repetidos. */
export function linhasDRE(a, { store, companyId }, natureza) {
  const ids = Array.isArray(a.p_company_ids) && a.p_company_ids.length ? a.p_company_ids : [companyId];
  const j = janela(a.p_start_date, a.p_end_date);
  const cats = new Map(store.rows('financial_categories').map((c) => [c.id, c]));
  const ccs = new Map(store.rows('cost_centers').map((c) => [c.id, c]));
  const comps = new Map(store.rows('companies').map((c) => [c.id, c.name]));
  const linhas = [];
  for (const cid of ids) {
    for (const l of lancamentosResultado(store, cid, j)) {
      const cat = cats.get(l.category_id);
      const nat = cat?.dre_group === 'impostos' ? 'tax' : l.natureza;
      if ((natureza === 'income') !== (nat === 'income')) continue;
      const cc = ccs.get(l.cost_center_id);
      const src = l.bank_account_id ? 'bank' : 'cash';
      linhas.push({
        line_id: l.id, line_source: src, company_id: cid, company_name: comps.get(cid) || null, tx_type: l.type, amount: num(l.amount), abs_amount: l.valor,
        description: l.description, transaction_date: diaDe(l), transaction_at: l.transaction_at, occurred_at: l.transaction_at, dre_date: diaDe(l),
        category_id: l.category_id || null, category_name: cat?.name || null, category_color: cat?.color || null,
        cost_center_id: l.cost_center_id || null, cost_center_name: cc?.name || null, cost_center_color: cc?.color || null,
        partner_id: l.partner_id || null, partner_type: l.partner_type || null, partner_name: null, credit_card_bill_date: null,
        nature: nat === 'tax' ? 'tax' : nat === 'income' ? 'revenue' : 'opex', is_credit_card: false, currency: 'BRL',
      });
    }
  }
  linhas.sort((x, y) => String(y.transaction_at).localeCompare(String(x.transaction_at)));
  const total = r2(linhas.reduce((s, l) => s + l.abs_amount, 0));
  const off = Number(a.p_offset) || 0;
  const pag = a.p_limit ? linhas.slice(off, off + Number(a.p_limit)) : linhas.slice(off);
  return pag.map((l) => ({ ...l, total_count: linhas.length, total_amount: total, total_amount_by_currency: total ? { BRL: total } : {} }));
}

// ---------------------------------------------------------------- "triggers" (hooks do Supabase falso)
/** transaction_date = dia BRT de transaction_at (trigger sync_transaction_date). */
export function sincronizaData(row, nowIso) {
  if (!row.transaction_at) row.transaction_at = row.created_at || nowIso();
  row.transaction_date = diaBR(row.transaction_at);
}
/** Recalcula o saldo gravado de uma conta (cofre: fórmula única; demais: soma dos lançamentos). */
export function recalculaConta(store, conta) {
  if (!conta) return;
  conta.balance = saldoConta(store, conta.company_id, conta);
  store.table('bank_accounts').touch();
}
/** Recalcula o saldo derivado da gaveta de um caixa (opening_balance = abertura + entradas - saídas). */
export function recalculaCaixa(store, caixaId) {
  const c = store.rows('cash_register').find((x) => x.id === caixaId);
  if (!c) return;
  c.opening_balance = saldoCaixa(store, c);
  store.table('cash_register').touch();
}
/** Sinal canônico de bank_transactions (canonical_bank_transaction_amount). */
export function sinalBanco(type, amount) {
  const v = Math.abs(num(amount));
  if (type === 'withdrawal' || type === 'expense') return -v;
  if (type === 'deposit') return v;
  return num(amount);
}

/** Os "triggers" de cada tabela (os hooks/<tabela>.mjs exportam estes; handlers usam via inserir/atualizar). */
const _conta = (store, id) => store.rows('bank_accounts').find((b) => b.id === id);
const _depoisCaixa = (row, { store }) => {
  if (row.cash_register_id) recalculaCaixa(store, row.cash_register_id);
  recalculaConta(store, cofre(store, row.company_id));
};
const _soData = { beforeInsert(row, { nowIso }) { sincronizaData(row, nowIso); } };
export const GATILHOS = {
  cash_transactions: {
    beforeInsert(row, { nowIso }) { sincronizaData(row, nowIso); },
    beforeUpdate(row, patch) { if (patch.transaction_at) patch.transaction_date = diaBR(patch.transaction_at); },
    afterInsert: _depoisCaixa, afterUpdate: _depoisCaixa, afterDelete: _depoisCaixa,
  },
  bank_transactions: {
    beforeInsert(row, { store, nowIso }) {
      row.amount = sinalBanco(row.type, row.amount);
      sincronizaData(row, nowIso);
      const ant = store.rows('bank_transactions').filter((b) => b.bank_account_id === row.bank_account_id && String(b.created_at) < String(row.created_at)).sort((x, y) => String(y.created_at).localeCompare(String(x.created_at)))[0];
      row.balance_after = r2(num(ant?.balance_after) + num(row.amount));
    },
    beforeUpdate(row, patch) {
      if (patch.amount !== undefined || patch.type) patch.amount = sinalBanco(patch.type || row.type, patch.amount ?? row.amount);
      if (patch.transaction_at) patch.transaction_date = diaBR(patch.transaction_at);
    },
    afterInsert(row, { store }) { recalculaConta(store, _conta(store, row.bank_account_id)); },
    afterUpdate(row, { store }) { recalculaConta(store, _conta(store, row.bank_account_id)); },
    afterDelete(row, { store }) { recalculaConta(store, _conta(store, row.bank_account_id)); },
  },
  balance_movements: _soData, stock_movements: _soData, purchases: _soData, sales: _soData,
  cash_register: {
    beforeInsert(row, { store }) {
      if (!num(row.register_number)) row.register_number = Math.max(0, ...store.rows('cash_register').filter((c) => c.company_id === row.company_id).map((c) => num(c.register_number))) + 1;
      if (!row.currency) row.currency = store.rows('companies').find((c) => c.id === row.company_id)?.base_currency || 'BRL';
      if (!row.opened_at) row.opened_at = row.created_at;
      if (row.initial_opening_balance == null) row.initial_opening_balance = num(row.opening_balance);
    },
  },
};
/** Insere pelo db (defaults do banco) e roda os "triggers" da tabela, como um INSERT de verdade. */
export function inserir(ctx, tabela, linha) {
  const g = GATILHOS[tabela] || {};
  const hc = { store: ctx.store, companyId: ctx.companyId, userId: ctx.userId, nowIso: () => new Date(agoraMs()).toISOString() };
  const lista = Array.isArray(linha) ? linha : [linha];
  const out = lista.map((l) => {
    const row = { ...l };
    if (!row.created_at) row.created_at = hc.nowIso();
    g.beforeInsert?.(row, hc);
    const r = ctx.db.insert(tabela, row, { companyId: ctx.companyId });
    g.afterInsert?.(r, hc);
    return r;
  });
  return Array.isArray(linha) ? out : out[0];
}
export function atualizar(ctx, tabela, filtro, patch) {
  const g = GATILHOS[tabela] || {};
  const hc = { store: ctx.store, companyId: ctx.companyId, userId: ctx.userId, nowIso: () => new Date(agoraMs()).toISOString() };
  const alvo = ctx.store.rows(tabela).filter((r) => Object.entries(filtro).every(([k, v]) => String(r[k]) === String(v)));
  for (const r of alvo) {
    const p = { ...patch };
    g.beforeUpdate?.(r, p, hc);
    Object.assign(r, p);
    g.afterUpdate?.(r, hc);
  }
  if (alvo.length) ctx.store.table(tabela).touch();
  return alvo;
}
export function remover(ctx, tabela, fn) {
  const g = GATILHOS[tabela] || {};
  const hc = { store: ctx.store, companyId: ctx.companyId, userId: ctx.userId, nowIso: () => new Date(agoraMs()).toISOString() };
  const gone = ctx.db.remove(tabela, fn);
  for (const r of gone) g.afterDelete?.(r, hc);
  return gone;
}
