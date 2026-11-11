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
    // 'transfer' entra pelo SINAL do amount, como no razão do app (_cash_register_ledger_balance, migration 20260926164000): saque
    // do banco para o caixa (+) e sangria do caixa (-). T06 cap09: o #86 do Marcos vai de 17.000,00 a 20.000,00.
    s += t.type === 'opening' ? num(t.amount) : t.type === 'transfer' ? num(t.amount) : (SINAL_CAIXA[t.type] || 0) * num(t.amount);
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
      const e = acc.get(pid) || { id: pid, name: pid ? nomes.get(pid) : 'Não informado', value: 0, count: 0, quantity: 0 };
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

// ---------------------------------------------------------------- pedidos (create_purchase_atomic / create_sale_atomic)
/** update_balance: saldo do parceiro (parceiro duplo vai para a linha 'party' do lado do cliente, sinal invertido no fornecedor). */
export function atualizaSaldo(ctx, cid, tipo, entidade, valor) {
  const { store } = ctx;
  let et = tipo, eid = entidade, v = valor;
  if (tipo === 'customer') {
    const c = store.rows('customers').find((x) => x.id === entidade);
    if (c?.linked_supplier_id) et = 'party';
  } else if (tipo === 'supplier') {
    const s = store.rows('suppliers').find((x) => x.id === entidade);
    if (s?.linked_customer_id) { et = 'party'; eid = s.linked_customer_id; v = -valor; }
  }
  let b = store.rows('balances').find((x) => x.company_id === cid && x.entity_type === et && x.entity_id === eid);
  if (b) { b.balance = r2(num(b.balance) + v); b.updated_at = new Date(agoraMs()).toISOString(); store.table('balances').touch(); }
  else b = ctx.db.insert('balances', { company_id: cid, entity_type: et, entity_id: eid, balance: r2(v), currency: 'BRL' }, { companyId: cid });
  return b;
}
/** Pedido completo como as funções atômicas do banco: cabeçalho, itens, estoque, pagamentos (register_order_payments) e
 *  parcelas (generate_order_installments). Devolve o jsonb da função. */
export function criarPedido(ctx, tipo, a) {
  const { store, RpcError } = ctx;
  const isC = tipo === 'purchase';
  const cid = a.p_company_id || ctx.companyId;
  const uid = a.p_user_id || ctx.userId;
  const parceiro = isC ? a.p_supplier_id : a.p_customer_id;
  const tab = isC ? 'purchases' : 'sales';
  if (a.p_client_request_id) {
    const ja = store.rows(tab).find((p) => p.company_id === cid && p.client_request_id === a.p_client_request_id);
    if (ja) return { [isC ? 'purchase_id' : 'sale_id']: ja.id, order_number: ja.order_number, order_ref: ja.order_ref, already_existed: true, weighing_ticket_id: null, weighing_ticket_linked: null };
  }
  let caixa = null;
  if (a.p_cash_register_id) {
    caixa = store.rows('cash_register').find((c) => c.id === a.p_cash_register_id);
    if (!caixa || caixa.company_id !== cid || caixa.status !== 'open') throw new RpcError(`CASH_REGISTER_CLOSED: caixa ${a.p_cash_register_id} inexistente, de outra empresa ou fechado (status=${caixa?.status || 'NULL'})`);
  }
  const cobrado = r2(a.p_paid_amount ?? a.p_total_amount ?? 0);
  const dinheiro = num(a.p_cash_amount), banco = num(a.p_transfer_amount), saldo = num(a.p_balance_amount), excesso = num(a.p_excess_to_balance);
  const formas = r2(dinheiro + banco + saldo);
  if (Math.abs(formas - r2(cobrado + excesso)) > 0.01) throw new RpcError(`PAGAMENTO_NAO_FECHA: formas somam ${formas} e o pedido cobra ${r2(cobrado + excesso)}`);
  const txAt = a.p_transaction_at || new Date(agoraMs()).toISOString();
  const numero = a.p_order_number || proximoNumero(store, cid);
  const comp = store.rows('companies').find((c) => c.id === cid) || {};
  const ref = String(comp.order_number_template || '#{NUM}').replace('{NUM}', String(numero));
  const head = inserir(ctx, tab, {
    company_id: cid, [isC ? 'supplier_id' : 'customer_id']: parceiro || null, notes: a.p_notes || null, total_amount: r2(a.p_total_amount), paid_amount: a.p_paid_amount ?? null,
    payment_method: a.p_payment_method || null, order_number: numero, order_seq: a.p_preserve_numbering ? a.p_order_seq ?? null : numero, order_period: a.p_preserve_numbering ? a.p_order_period ?? null : null,
    order_ref: a.p_preserve_numbering ? a.p_order_ref ?? null : ref, created_by: uid, transaction_at: txAt, driver_id: a.p_driver_id || null, vehicle_id: a.p_vehicle_id || null,
    driver_name: a.p_driver_name || null, vehicle_plate: a.p_vehicle_plate || null, status: 'completed', client_request_id: a.p_client_request_id || null,
    hide_financial_details: !!a.p_hide_financial_details, currency: a.p_currency || 'BRL',
  });
  const rot = isC ? 'Compra' : 'Venda';
  const itens = Array.isArray(a.p_items) ? a.p_items : [];
  for (const it of itens) {
    ctx.db.insert(isC ? 'purchase_items' : 'sale_items', {
      [isC ? 'purchase_id' : 'sale_id']: head.id, material_id: it.material_id, material_name: it.material_name, quantity: num(it.quantity), unit_price: num(it.unit_price),
      impurity: num(it.impurity), total_price: r2(it.total_price), tare_weight: it.tare_weight ?? null, impurity_kg: it.impurity_kg ?? null, impurity_pct: it.impurity_pct ?? null,
      first_weight: it.first_weight ?? null, second_weight: it.second_weight ?? null, weighing_mode: it.weighing_mode ?? null, item_discount: num(it.item_discount),
      weight_source: it.weight_source || 'manual', captured_weight: it.captured_weight ?? null, scale_identifier: it.scale_identifier ?? null,
    });
  }
  // estoque: um movimento por item, saldo corrido por material
  for (const it of itens) {
    const m = store.rows('materials').find((x) => x.id === it.material_id && x.company_id === cid);
    if (!m) throw new RpcError(`Material não encontrado ou de outra empresa em {${it.material_id}}`);
    const imp = num(it.impurity);
    const liq = num(it.quantity) - imp;
    const antes = num(m.current_stock);
    const depois = Math.round((antes + (isC ? liq : -liq)) * 1000) / 1000;
    inserir(ctx, 'stock_movements', {
      company_id: cid, material_id: m.id, order_id: head.id, order_type: tipo, type: isC ? 'COMPRA' : 'VENDA', quantity: isC ? liq : -liq,
      stock_before: antes, stock_after: depois, description: `${rot} #${numero}${imp > 0 ? ` (${imp}kg impureza)` : ''}`, created_by: uid, transaction_at: txAt,
    });
    m.current_stock = depois;
    store.table('materials').touch();
  }
  // pagamentos (register_order_payments)
  const ctTipo = isC ? 'purchase' : 'sale';
  const partes = (dinheiro > 0) + (banco > 0) + (saldo > 0);
  const sufixo = partes > 1 ? ' (Parcial)' : '';
  if (dinheiro === 0 && banco === 0 && saldo === 0) {
    if (caixa) inserir(ctx, 'cash_transactions', { company_id: cid, type: ctTipo, amount: 0, description: `${rot} #${numero} (Doação)`, order_id: head.id, cash_register_id: caixa.id, created_by: uid, transaction_at: txAt });
  } else {
    if (dinheiro > 0) {
      if (!caixa) throw new RpcError('cash_register_id obrigatorio quando cash_amount > 0');
      inserir(ctx, 'cash_transactions', { company_id: cid, type: ctTipo, amount: dinheiro, description: `${rot} #${numero}${sufixo}`, order_id: head.id, cash_register_id: caixa.id, created_by: uid, transaction_at: txAt });
    }
    if (banco > 0) {
      const conta = a.p_bank_account_id || contas(store, cid).find((b) => b.is_default)?.id;
      if (!conta) throw new RpcError('Empresa sem bank_account default — nao pode processar transferencia');
      inserir(ctx, 'bank_transactions', { company_id: cid, type: isC ? 'withdrawal' : 'deposit', amount: isC ? -banco : banco, description: `${rot} #${numero}${sufixo}`, order_id: head.id, bank_account_id: conta, created_by: uid, transaction_at: txAt, payment_method: 'transfer', source: 'order' });
      if (dinheiro === 0 && caixa) inserir(ctx, 'cash_transactions', { company_id: cid, type: ctTipo, amount: 0, description: `${rot} #${numero} (PIX/Transferência)`, order_id: head.id, cash_register_id: caixa.id, created_by: uid, transaction_at: txAt });
    }
    if (excesso > 0 && isC && parceiro) {
      const b = atualizaSaldo(ctx, cid, 'supplier', parceiro, -excesso);
      inserir(ctx, 'balance_movements', { balance_id: b.id, company_id: cid, entity_type: 'supplier', entity_id: parceiro, movement_type: 'order', amount: -excesso, description: `Sobra do pagamento - ${rot} #${numero}`, order_id: head.id, payment_method: null, created_by: uid, transaction_at: txAt });
    }
    if (saldo > 0) {
      if (!parceiro) throw new RpcError('entity_type e entity_id obrigatorios quando balance_amount > 0');
      const et = isC ? 'supplier' : 'customer';
      const b = atualizaSaldo(ctx, cid, et, parceiro, saldo);
      inserir(ctx, 'balance_movements', { balance_id: b.id, company_id: cid, entity_type: et, entity_id: parceiro, movement_type: 'order', amount: saldo, description: `${rot} #${numero}`, order_id: head.id, payment_method: 'balance', created_by: uid, transaction_at: txAt, cash_register_id: caixa?.id || null });
      if (a.p_balance_due_date) { b.due_date = a.p_balance_due_date; }
      if (dinheiro === 0 && banco === 0 && caixa) inserir(ctx, 'cash_transactions', { company_id: cid, type: ctTipo, amount: 0, description: `${rot} #${numero} (Saldo)`, order_id: head.id, cash_register_id: caixa.id, created_by: uid, transaction_at: txAt });
      // parcelas (generate_order_installments)
      const parc = Array.isArray(a.p_installments) ? a.p_installments : [];
      const label = isC ? 'compra' : 'venda';
      const base = { company_id: cid, direction: isC ? 'payable' : 'receivable', category_id: null, paid_amount: 0, status: 'pending', partner_type: et, partner_id: parceiro, order_id: head.id, order_type: tipo, payment_condition_id: a.p_payment_condition_id || null, created_by: uid, currency: 'BRL' };
      if (parc.length) parc.forEach((p, i) => ctx.db.insert('financial_bills', { ...base, description: `Fatura ${label} #${numero} (parcela ${p.number || i + 1}/${parc.length})`, amount: num(p.amount), due_date: p.due_date || null, installment_number: p.number || i + 1, installment_total: parc.length }, { companyId: cid }));
      else if (a.p_balance_due_date) ctx.db.insert('financial_bills', { ...base, description: `Fatura ${label} #${numero}`, amount: saldo, due_date: a.p_balance_due_date, installment_number: 1, installment_total: 1 }, { companyId: cid });
    }
  }
  // T8: pedido da valorização marca o(s) ticket(s) como valorizado(s), como _link_weighing_ticket_batch_to_order (20261028140000)
  const rasc = a.p_order_draft_id ? store.rows('order_drafts').find((d) => d.id === a.p_order_draft_id) : null;
  const tks = new Set([a.p_source_weighing_ticket_id, rasc?.source_weighing_ticket_id, ...(rasc?.source_weighing_ticket_ids || [])].filter(Boolean));
  for (const t of store.rows('weighing_tickets')) if (tks.has(t.id) && t.company_id === cid && (!t.customer_supplier_id || t.customer_supplier_id === parceiro)) Object.assign(t, { status: 'valorized', valorized_order_id: head.id, updated_at: new Date(agoraMs()).toISOString() });
  if (tks.size) store.table('weighing_tickets').touch();
  if (a.p_order_draft_id) ctx.db.remove('order_drafts', { id: a.p_order_draft_id });
  return { [isC ? 'purchase_id' : 'sale_id']: head.id, order_number: numero, order_ref: head.order_ref, already_existed: false, weighing_ticket_id: a.p_source_weighing_ticket_id || null, weighing_ticket_linked: a.p_source_weighing_ticket_id ? true : null };
}

/** claim/heartbeat_draft_editing: quem chama fica com o bastão (um operador por sessão no mundo falso). */
export function bastao(ctx, a, modo) {
  const { store, userId, companyId } = ctx;
  const t = store.table('draft_editors');
  const agora = new Date(agoraMs()).toISOString();
  let r = t.rows.find((x) => x.draft_kind === a.p_draft_kind && x.draft_id === a.p_draft_id);
  if (!r) {
    if (modo === 'heartbeat') return [];
    r = { draft_kind: a.p_draft_kind, draft_id: a.p_draft_id, company_id: companyId, user_id: userId, session_id: a.p_session_id, claimed_at: agora, heartbeat_at: agora };
    t.rows.push(r);
  } else if (modo === 'claim' || r.session_id === a.p_session_id) {
    Object.assign(r, { user_id: userId, session_id: a.p_session_id, heartbeat_at: agora, ...(modo === 'claim' && r.session_id !== a.p_session_id ? { claimed_at: agora } : {}) });
  }
  t.touch();
  const nome = store.rows('profiles').find((p) => p.id === r.user_id)?.full_name || null;
  return [{ draft_kind: r.draft_kind, draft_id: r.draft_id, holder_user_id: r.user_id, holder_name: nome, holder_session_id: r.session_id, claimed_at: r.claimed_at, heartbeat_at: r.heartbeat_at, is_holder: r.session_id === a.p_session_id }];
}
