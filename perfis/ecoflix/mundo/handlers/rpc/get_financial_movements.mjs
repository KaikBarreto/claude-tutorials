// Extrato de uma conta (Movimentações Bancárias), igual à função SQL: no cofre (kind cash) entram as linhas do caixa
// (cash_transactions; abertura/fechamento/transferência são internas e não mexem no saldo) e as bancárias do cofre; nas
// demais contas, só bank_transactions (signed_amount = amount x -1 em saída, como no SQL). Saldo após cada linha
// ancorado no saldo atual da conta; ordem do mais novo para o mais antigo; total_count para a paginação.
import { num, r2, diaDe, saldoConta } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const conta = store.rows('bank_accounts').find((b) => b.id === a.p_account_id && b.company_id === cid);
  if (!conta) return [];
  const linhas = [];
  if (conta.kind === 'cash') {
    for (const ct of store.rows('cash_transactions')) {
      if (ct.company_id !== cid) continue;
      const sinal = ['purchase', 'withdrawal', 'expense'].includes(ct.type) ? -1 : 1;
      linhas.push({ src: ct, source_table: 'cash_transactions', type: ct.type, signed_amount: num(ct.amount) * sinal, is_internal_transfer: ['opening', 'closing', 'transfer'].includes(ct.type), cash_register_id: ct.cash_register_id || null, origin_company_id: null });
    }
    for (const bt of store.rows('bank_transactions')) if (bt.bank_account_id === conta.id) linhas.push({ src: bt, source_table: 'bank_transactions', type: bt.type, signed_amount: num(bt.amount), is_internal_transfer: bt.type === 'transfer', cash_register_id: null, origin_company_id: bt.origin_company_id || null });
  } else {
    for (const bt of store.rows('bank_transactions')) if (bt.bank_account_id === conta.id) linhas.push({ src: bt, source_table: 'bank_transactions', type: bt.type, signed_amount: num(bt.amount) * (['withdrawal', 'expense'].includes(bt.type) ? -1 : 1), raw: num(bt.amount), is_internal_transfer: false, cash_register_id: null, origin_company_id: bt.origin_company_id || null });
  }
  const ts = (l) => l.src.transaction_at || l.src.created_at || '';
  linhas.sort((x, y) => ts(x).localeCompare(ts(y)) || String(x.src.created_at).localeCompare(String(y.src.created_at)) || String(x.src.id).localeCompare(String(y.src.id)));
  const valor = (l) => (conta.kind === 'cash' ? (l.is_internal_transfer ? 0 : l.signed_amount) : l.raw);
  const total = linhas.reduce((s, l) => s + valor(l), 0);
  let acc = saldoConta(store, cid, conta) - total;
  for (const l of linhas) { acc += valor(l); l.balance_after = r2(acc); }
  const cats = new Map(store.rows('financial_categories').map((c) => [c.id, c]));
  const caixas = new Map(store.rows('cash_register').map((c) => [c.id, c]));
  const perfis = new Map(store.rows('profiles').map((p) => [p.id, p.full_name]));
  const tipos = Array.isArray(a.p_types) && a.p_types.length ? a.p_types : null;
  const catsF = Array.isArray(a.p_category_ids) && a.p_category_ids.length ? a.p_category_ids : null;
  const filtradas = linhas.filter((l) => (!a.p_date_from || diaDe(l.src) >= a.p_date_from) && (!a.p_date_to || diaDe(l.src) <= a.p_date_to) && (!tipos || tipos.includes(l.type)) && (!catsF || catsF.includes(l.src.category_id))).reverse();
  const off = Number(a.p_offset) || 0;
  return filtradas.slice(off, off + (Number(a.p_limit) || 25)).map((l) => {
    const c = cats.get(l.src.category_id);
    return {
      id: l.src.id, created_at: l.src.created_at, transaction_at: l.src.transaction_at || l.src.created_at, type: l.type, signed_amount: r2(l.signed_amount),
      description: l.src.description, category_id: l.src.category_id || null, category_name: c?.name || null, category_color: c?.color || null,
      cash_register_id: l.cash_register_id, register_number: l.cash_register_id ? caixas.get(l.cash_register_id)?.register_number ?? null : null,
      operator_name: perfis.get(l.src.created_by) || null, source_table: l.source_table, is_internal_transfer: l.is_internal_transfer,
      order_id: l.src.order_id || null, balance_after: l.balance_after, total_count: filtradas.length, origin_company_id: l.origin_company_id, origin_company_name: null,
    };
  });
};
