// reconcile_find_in_other_accounts (T14): o mesmo valor (±0,01) em OUTRA conta da empresa ou no caixa, ±5 dias, ainda livre (só leitura).
import { num, diaBR, addDias } from '../../lib/eco.mjs';
import { linha, pedidoDe } from '../../lib/conciliacao.mjs';

const SINAL = { purchase: -1, withdrawal: -1, expense: -1 };
export default (a, ctx) => {
  const { store } = ctx;
  const e = linha(ctx, a.p_entry_id);
  const d = diaBR(e.posted_at), d1 = addDias(d, -5), d2 = addDias(d, 5);
  const dentro = (x) => x >= d1 && x <= d2;
  const ocupados = new Set(store.rows('reconciliation_matches').map((m) => m.bank_transaction_id));
  const cofre = store.rows('bank_accounts').filter((b) => b.company_id === e.company_id && b.kind === 'cash').sort((x, y) => Number(!!x.is_archived) - Number(!!y.is_archived) || String(x.created_at).localeCompare(String(y.created_at)))[0];
  const out = [];
  for (const bt of store.rows('bank_transactions')) {
    const ba = store.rows('bank_accounts').find((b) => b.id === bt.bank_account_id);
    if (!ba || ba.company_id !== e.company_id || bt.bank_account_id === e.bank_account_id || Math.abs(num(bt.amount) - num(e.amount)) > 0.01) continue;
    if (!dentro(bt.transaction_date || diaBR(bt.transaction_at)) || ocupados.has(bt.id)) continue;
    const o = pedidoDe(store, bt.order_id);
    out.push({ id: bt.id, source: 'bank', transaction_at: bt.transaction_at, created_at: bt.created_at, description: bt.description ?? null, amount: num(bt.amount), type: bt.type ?? null,
      group_id: bt.group_id ?? null, account_id: ba.id, account_name: ba.name, account_kind: ba.kind, cash_register_id: null, register_number: null, register_is_closed: null,
      order_id: bt.order_id ?? null, order_kind: o.order_kind, order_number: o.order_number, counterparty_name: o.counterparty_name });
  }
  for (const ct of store.rows('cash_transactions')) {
    if (ct.company_id !== e.company_id) continue;
    const v = num(ct.amount) * (SINAL[ct.type] || 1);
    if (Math.abs(v - num(e.amount)) > 0.01 || !dentro(ct.transaction_date || diaBR(ct.transaction_at || ct.created_at))) continue;
    const cr = store.rows('cash_register').find((c) => c.id === ct.cash_register_id);
    const o = pedidoDe(store, ct.order_id);
    out.push({ id: ct.id, source: 'cash', transaction_at: ct.transaction_at || ct.created_at, created_at: ct.created_at, description: ct.description ?? null, amount: v, type: ct.type ?? null,
      group_id: ct.group_id ?? null, account_id: cofre?.id ?? null, account_name: cofre?.name ?? 'Caixa', account_kind: 'cash', cash_register_id: ct.cash_register_id ?? null,
      register_number: cr?.register_number ?? null, register_is_closed: ct.cash_register_id ? (cr ? cr.status === 'closed' : true) : false,
      order_id: ct.order_id ?? null, order_kind: o.order_kind, order_number: o.order_number, counterparty_name: o.counterparty_name });
  }
  const T = (x) => new Date(x).getTime();
  return out.sort((x, y) => T(y.transaction_at) - T(x.transaction_at) || T(y.created_at) - T(x.created_at) || String(y.id).localeCompare(String(x.id))).slice(0, 5)
    .map(({ created_at, ...r }) => r);
};
