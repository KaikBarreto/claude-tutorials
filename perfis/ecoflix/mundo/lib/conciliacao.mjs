// Conciliação bancária (T14): o que as funções SQL do EcoSistema 1.59.154 fazem, em memória.
// Fontes (repositório do app, f37573ea0): get_bank_reconciliation_state (20261002210000_conciliacao_uma_linha_para_n_lancamentos.sql),
// reconcile_find_distant_exact_candidates (20261013183000), reconcile_find_in_other_accounts (20260916164739),
// reconcile_search_candidates (20260910150000), reconcile_search_transfer_candidates (20261009174500), reconcile_match_existing
// (20260807163000), reconcile_settle_bill (20260727120000 + pay_financial_bill de 20261012093000), reconcile_create_transaction
// (20260907150000), create_bank_statement_import / ignorar / finalizar / cancelar / get_statement_imports (20260922180000).
import { r2, num, agoraMs, inserir, atualizar, remover, diaBR, addDias } from './eco.mjs';

const T = (iso) => new Date(iso).getTime();
const DIA = 86400000;
const igual = (a, b) => Math.abs(num(a) - num(b)) < 0.005;
const sinal = (v) => Math.sign(num(v));
export const agoraIso = () => new Date(agoraMs()).toISOString();

export const linhasDo = (store, importId) => store.rows('bank_statement_entries').filter((e) => e.import_id === importId);
export const casamentosDa = (store, entryId) => store.rows('reconciliation_matches').filter((m) => m.entry_id === entryId);
const vinculados = (store) => new Set(store.rows('reconciliation_matches').map((m) => m.bank_transaction_id));

export function linha(ctx, id) {
  const e = ctx.store.rows('bank_statement_entries').find((x) => x.id === id);
  if (!e) throw new ctx.RpcError('Linha do extrato não encontrada.');
  return e;
}
export function extrato(ctx, id) {
  const i = ctx.store.rows('bank_statement_imports').find((x) => x.id === id);
  if (!i) throw new ctx.RpcError(`Import não encontrado (id ${id}).`);
  return i;
}
export function pendente(ctx, e) {
  if (e.status !== 'pending') throw new ctx.RpcError('Esta linha já foi conciliada ou ignorada.');
  const imp = ctx.store.rows('bank_statement_imports').find((x) => x.id === e.import_id);
  if (imp && imp.status !== 'open') throw new ctx.RpcError('Este extrato ja foi finalizado.');
}

/** pedido de origem (compra/venda) de um lançamento, como os LEFT JOIN das funções */
export function pedidoDe(store, orderId) {
  if (!orderId) return { order_kind: null, order_number: null, order_ref: null, counterparty_name: null };
  const p = store.rows('purchases').find((x) => x.id === orderId);
  if (p) return { order_kind: 'purchase', order_number: p.order_number ?? null, order_ref: p.order_ref ?? null, counterparty_name: store.rows('suppliers').find((s) => s.id === p.supplier_id)?.name ?? null };
  const s = store.rows('sales').find((x) => x.id === orderId);
  if (s) return { order_kind: 'sale', order_number: s.order_number ?? null, order_ref: s.order_ref ?? null, counterparty_name: store.rows('customers').find((c) => c.id === s.customer_id)?.name ?? null };
  return { order_kind: null, order_number: null, order_ref: null, counterparty_name: null };
}
export function candidato(store, bt, extra = {}) {
  return { id: bt.id, transaction_at: bt.transaction_at, description: bt.description ?? null, amount: num(bt.amount), type: bt.type, order_id: bt.order_id ?? null, ...pedidoDe(store, bt.order_id), ...extra };
}
/** tipos que a conciliação aceita (avulso: deposit/withdrawal/expense/transfer; pagamento de pedido: deposit/withdrawal) */
export const tipoOk = (bt) => (bt.order_id ? ['deposit', 'withdrawal'] : ['deposit', 'withdrawal', 'expense', 'transfer']).includes(bt.type);

/** pool da sugestão: mesma conta, mesmo sinal, até R$ 2,00, tipo aceito, [posted − 3 dias, posted + 3 dias), ainda livre */
function pool(store, e, livres) {
  const p = T(e.posted_at);
  return store.rows('bank_transactions').filter((bt) => bt.bank_account_id === e.bank_account_id && sinal(bt.amount) === sinal(e.amount)
    && Math.abs(num(bt.amount) - num(e.amount)) <= 2.0 + 1e-9 && tipoOk(bt) && T(bt.transaction_at) >= p - 3 * DIA && T(bt.transaction_at) < p + 3 * DIA
    && !livres.has(bt.id));
}
export function sugestao(store, e, ocupados = vinculados(store)) {
  const p = T(e.posted_at);
  const pl = pool(store, e, ocupados);
  const cand = pl.filter((bt) => igual(bt.amount, e.amount)).sort((a, b) => Math.abs(T(a.transaction_at) - p) - Math.abs(T(b.transaction_at) - p)).slice(0, 10);
  const near = cand.length ? [] : pl.filter((bt) => Math.abs(num(bt.amount) - num(e.amount)) > 0.01)
    .sort((a, b) => Math.abs(num(a.amount) - num(e.amount)) - Math.abs(num(b.amount) - num(e.amount)) || Math.abs(T(a.transaction_at) - p) - Math.abs(T(b.transaction_at) - p)).slice(0, 5);
  return {
    ambiguous: cand.length >= 2, suggested_transaction_id: cand.length === 1 ? cand[0].id : null, candidate_count: cand.length,
    candidates: cand.map((bt) => { const c = candidato(store, bt); delete c.type; delete c.order_ref; return c; }),
    near_matches: near.map((bt) => { const c = candidato(store, bt, { difference: r2(num(e.amount) - num(bt.amount)) }); delete c.type; delete c.order_ref; return c; }),
  };
}
/** valor exato, mesma conta, livre, FORA da janela de 3 dias (só para linhas pendentes; máx. 5 na amostra) */
export function distantes(store, e, ocupados = vinculados(store)) {
  const p = T(e.posted_at);
  const ex = store.rows('bank_transactions').filter((bt) => bt.bank_account_id === e.bank_account_id && igual(bt.amount, e.amount) && tipoOk(bt)
    && !(T(bt.transaction_at) >= p - 3 * DIA && T(bt.transaction_at) < p + 3 * DIA) && !ocupados.has(bt.id))
    .sort((a, b) => Math.abs(T(a.transaction_at) - p) - Math.abs(T(b.transaction_at) - p) || String(a.id).localeCompare(String(b.id)));
  return { candidate_count: ex.length, candidates: ex.slice(0, 5).map((bt) => { const c = candidato(store, bt); delete c.order_ref; return c; }) };
}

function pernas(store, e) {
  const ms = casamentosDa(store, e.id).map((m) => ({ m, bt: store.rows('bank_transactions').find((b) => b.id === m.bank_transaction_id) }));
  ms.sort((a, b) => (a.bt ? T(a.bt.transaction_at) : Infinity) - (b.bt ? T(b.bt.transaction_at) : Infinity) || String(a.m.bank_transaction_id).localeCompare(String(b.m.bank_transaction_id)) || String(a.m.id).localeCompare(String(b.m.id)));
  return ms;
}

/** get_bank_reconciliation_state: rodapé (saldo do banco = ledger; conciliado = abertura + Σ linhas não ignoradas), linhas e sugestões */
export function estado(store, imp) {
  const es = linhasDo(store, imp.id).sort((a, b) => T(a.posted_at) - T(b.posted_at) || String(a.id).localeCompare(String(b.id)));
  const statement = num(imp.ledger_balance);
  const reconciled = r2(num(imp.opening_balance) + es.filter((e) => e.status !== 'ignored').reduce((s, e) => s + num(e.amount), 0));
  const ocupados = vinculados(store);
  // diferenças casadas, agrupadas por group_id (ou pelo id do casamento)
  const grupos = new Map();
  for (const e of es.filter((x) => x.status === 'matched')) {
    for (const { m, bt } of pernas(store, e)) {
      const k = m.group_id || m.id;
      const g = grupos.get(k) || { group_id: m.group_id || null, diff: 0, linhas: new Map(), txs: new Map(), posted: e.posted_at };
      g.diff += num(m.value_difference);
      g.linhas.set(e.id, num(e.amount));
      if (bt) g.txs.set(bt.id, bt);
      if (T(e.posted_at) < T(g.posted)) g.posted = e.posted_at;
      grupos.set(k, g);
    }
  }
  const lista = [...grupos.entries()].filter(([, g]) => Math.abs(g.diff) > 0.005).sort((a, b) => T(a[1].posted) - T(b[1].posted) || String(a[0]).localeCompare(String(b[0])));
  const vd = lista.map(([, g]) => {
    const tx = [...g.txs.values()].sort((a, b) => T(a.transaction_at) - T(b.transaction_at) || String(a.id).localeCompare(String(b.id)))[0];
    return { group_id: g.group_id, line_count: [...g.linhas.keys()].length, order_number: tx ? pedidoDe(store, tx.order_id).order_number : null,
      description: tx?.description ?? null, entry_amount: r2([...g.linhas.values()].reduce((s, v) => s + v, 0)),
      tx_amount: r2([...g.txs.values()].reduce((s, b) => s + num(b.amount), 0)), diff: r2(g.diff) };
  });
  const entries = es.map((e) => {
    const ps = pernas(store, e);
    const m0 = ps[0]?.m;
    return {
      id: e.id, fitid: e.fitid ?? null, posted_at: e.posted_at, amount: num(e.amount), trn_type: e.trn_type ?? null, memo: e.memo ?? null, name: e.name ?? null, status: e.status,
      current_match: m0 ? { match_id: m0.id, bank_transaction_id: m0.bank_transaction_id, match_type: m0.match_type, bill_id: m0.bill_id ?? null, confidence: m0.confidence,
        value_difference: num(m0.value_difference), group_id: m0.group_id ?? null, employee_movement_label: null, balance_movement_id: m0.balance_movement_id ?? null, balance_partner_label: null } : null,
      match_legs: ps.map(({ m, bt }) => ({ match_id: m.id, bank_transaction_id: m.bank_transaction_id, match_type: m.match_type, confidence: m.confidence, value_difference: num(m.value_difference),
        group_id: m.group_id ?? null, transaction_at: bt?.transaction_at ?? null, description: bt?.description ?? null, amount: bt ? num(bt.amount) : null, type: bt?.type ?? null,
        order_id: bt?.order_id ?? null, ...(() => { const o = pedidoDe(store, bt?.order_id); return { order_kind: o.order_kind, order_number: o.order_number, counterparty_name: o.counterparty_name }; })() })),
      suggested: sugestao(store, e, ocupados),
      already_reconciled: [],
    };
  });
  return {
    import: { id: imp.id, bank_account_id: imp.bank_account_id, file_name: imp.file_name ?? null, status: imp.status, period_start: imp.period_start ?? null, period_end: imp.period_end ?? null,
      ledger_balance: imp.ledger_balance ?? null, opening_balance: num(imp.opening_balance), entry_count: num(imp.entry_count) },
    statement_balance: statement, reconciled_balance: reconciled, difference: r2(statement - reconciled),
    pending_count: es.filter((e) => e.status === 'pending').length,
    matched_value_difference_total: r2(lista.reduce((s, [, g]) => s + g.diff, 0)), matched_value_difference_count: lista.length,
    matched_value_differences: vd, entries,
  };
}

/** resumo de um import para a lista da aba (get_statement_imports) */
export function resumoImport(store, i) {
  const es = linhasDo(store, i.id);
  const soma = es.filter((e) => e.status !== 'ignored').reduce((s, e) => s + num(e.amount), 0);
  return { id: i.id, file_name: i.file_name ?? null, period_start: i.period_start ?? null, period_end: i.period_end ?? null, created_at: i.created_at, status: i.status,
    total_entries: es.length, pending_count: es.filter((e) => e.status === 'pending').length, difference: r2(num(i.ledger_balance) - (num(i.opening_balance) + soma)) };
}

export function casar(ctx, e, bt, { tipo = 'existing', confianca = 'manual', billId = null, groupId = null, diferenca = 0 } = {}) {
  const m = ctx.db.insert('reconciliation_matches', { company_id: e.company_id, entry_id: e.id, bank_transaction_id: bt.id, match_type: tipo, bill_id: billId, confidence: confianca,
    value_difference: r2(diferenca), group_id: groupId, created_by: ctx.userId, created_at: agoraIso() }, { companyId: e.company_id });
  atualizar(ctx, 'bank_statement_entries', { id: e.id }, { status: 'matched' });
  return m;
}

/** desfaz uma linha (reconcile_unmatch_entry): existing solta o vínculo; created apaga o lançamento; bill_settlement estorna a baixa */
export function desfazer(ctx, e) {
  const { store } = ctx;
  let ms = casamentosDa(store, e.id);
  const grupo = ms.find((m) => m.group_id)?.group_id;
  const linhasGrupo = grupo ? store.rows('reconciliation_matches').filter((m) => m.group_id === grupo).map((m) => m.entry_id) : [e.id];
  if (grupo) ms = store.rows('reconciliation_matches').filter((m) => m.group_id === grupo);
  for (const m of ms) {
    if (m.match_type === 'created' && m.bank_transaction_id) remover(ctx, 'bank_transactions', (b) => b.id === m.bank_transaction_id);
    if (m.match_type === 'bill_settlement' && m.bank_transaction_id) {
      const pg = store.rows('bill_payments').filter((p) => p.bank_transaction_id === m.bank_transaction_id);
      for (const p of pg) {
        const b = store.rows('financial_bills').find((x) => x.id === p.bill_id);
        if (b) {
          const pago = r2(num(b.paid_amount) - num(p.amount));
          atualizar(ctx, 'financial_bills', { id: b.id }, { paid_amount: pago, status: pago > 0.005 ? 'partial' : 'pending', paid_at: pago > 0.005 ? b.paid_at : null, updated_at: agoraIso() });
        }
      }
      ctx.db.remove('bill_payments', (p) => p.bank_transaction_id === m.bank_transaction_id);
      remover(ctx, 'bank_transactions', (b) => b.id === m.bank_transaction_id);
    }
  }
  const ids = new Set(ms.map((m) => m.id));
  ctx.db.remove('reconciliation_matches', (m) => ids.has(m.id));
  for (const id of new Set(linhasGrupo)) atualizar(ctx, 'bank_statement_entries', { id }, { status: 'pending' });
  return ms;
}

/** pay_financial_bill de uma conta inteira por transferência na data da linha (o que reconcile_settle_bill chama) */
export function baixarConta(ctx, e, bill) {
  const dia = diaBR(e.posted_at);
  const pagar = bill.direction === 'payable';
  const valor = r2(Math.abs(num(e.amount)));
  const grupo = crypto.randomUUID();
  const bt = inserir(ctx, 'bank_transactions', {
    company_id: e.company_id, bank_account_id: e.bank_account_id, type: pagar ? 'withdrawal' : 'deposit', amount: valor, description: `Pagamento: ${bill.description}`,
    category_id: bill.category_id ?? null, cost_center_id: bill.cost_center_id ?? null, transaction_at: `${dia}T15:00:00.000Z`, group_id: grupo, created_by: ctx.userId,
    partner_id: bill.partner_id ?? null, partner_type: bill.partner_type ?? null, payment_method: 'transfer', source: 'manual',
  });
  ctx.db.insert('bill_payments', { company_id: e.company_id, bill_id: bill.id, amount: valor, paid_date: dia, payment_method: 'transfer', bank_account_id: e.bank_account_id,
    bank_transaction_id: bt.id, group_id: grupo, created_by: ctx.userId, currency: 'BRL', created_at: agoraIso() }, { companyId: e.company_id });
  const pago = r2(num(bill.paid_amount) + valor);
  atualizar(ctx, 'financial_bills', { id: bill.id }, { paid_amount: pago, status: pago + 0.005 >= num(bill.amount) ? 'paid' : 'partial', paid_at: `${dia}T15:00:00.000Z`, updated_at: agoraIso() });
  return bt;
}

export { addDias, diaBR };
