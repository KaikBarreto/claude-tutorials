// reconcile_search_split_candidates(p_entry_id, p_query) (app 1.60.18: 20261002210000_conciliacao_uma_linha_para_n_lancamentos.sql): as PARTES de uma linha que pagou
// vários lançamentos: mesma conta e mesmo sinal da linha, valor absoluto MENOR que o da linha, ainda livres, sem janela de data; com texto filtra por descrição,
// nº do pedido ou contraparte. Mesma forma de linha do reconcile_search_candidates; até 50, mais novos primeiro. T14 cap17.
import { num } from '../../lib/eco.mjs';
import { linha, candidato } from '../../lib/conciliacao.mjs';
const sem = (s) => String(s ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
export default (a, ctx) => {
  const { store } = ctx;
  const e = linha(ctx, a.p_entry_id);
  const q = String(a.p_query ?? '').trim();
  const ocupados = new Set(store.rows('reconciliation_matches').map((m) => m.bank_transaction_id));
  const T = (x) => new Date(x).getTime();
  return store.rows('bank_transactions').filter((bt) => bt.bank_account_id === e.bank_account_id && !ocupados.has(bt.id) && Math.sign(num(bt.amount)) === Math.sign(num(e.amount))
    && Math.abs(num(bt.amount)) < Math.abs(num(e.amount)) && ['deposit', 'withdrawal', 'expense', 'transfer'].includes(bt.type))
    .map((bt) => candidato(store, bt))
    .filter((c) => !q || [c.description, c.order_number, c.counterparty_name].some((v) => v != null && sem(v).includes(sem(q))))
    .sort((x, y) => T(y.transaction_at) - T(x.transaction_at) || String(y.id).localeCompare(String(x.id))).slice(0, 50)
    .map(({ order_ref, ...c }) => c);
};
