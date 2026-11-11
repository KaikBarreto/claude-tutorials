// reconcile_search_candidates (T14 cap10, "Buscar lançamento"): sem texto, os de valor exato (±0,01); com texto, até R$ 2,00 do mesmo sinal
// cuja descrição, nº do pedido, fornecedor ou cliente contém o texto. Qualquer data; só lançamentos livres da conta da linha.
import { num } from '../../lib/eco.mjs';
import { linha, candidato } from '../../lib/conciliacao.mjs';

const sem = (s) => String(s ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
export default (a, ctx) => {
  const { store } = ctx;
  const e = linha(ctx, a.p_entry_id);
  const q = String(a.p_query ?? '').trim();
  const ocupados = new Set(store.rows('reconciliation_matches').map((m) => m.bank_transaction_id));
  const T = (x) => new Date(x).getTime();
  return store.rows('bank_transactions').filter((bt) => bt.bank_account_id === e.bank_account_id && !ocupados.has(bt.id)
    && (q ? Math.abs(num(bt.amount) - num(e.amount)) <= 2.0 + 1e-9 && Math.sign(num(bt.amount)) === Math.sign(num(e.amount)) : Math.abs(num(bt.amount) - num(e.amount)) <= 0.01))
    .map((bt) => candidato(store, bt))
    .filter((c) => !q || [c.description, c.order_number, c.counterparty_name].some((v) => v != null && sem(v).includes(sem(q))))
    .sort((x, y) => T(y.transaction_at) - T(x.transaction_at) || String(y.id).localeCompare(String(x.id))).slice(0, 50)
    .map(({ order_ref, ...c }) => c);
};
