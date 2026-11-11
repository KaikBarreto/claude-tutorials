// reconcile_search_transfer_candidates (T14 cap07, "Casar com transferência"): grupos de duas pernas em contas próprias diferentes, líquidos
// em zero, com a perna da conta do extrato do valor das linhas e ainda livre (busca estrutural: não depende da descrição).
import { num, diaBR, addDias } from '../../lib/eco.mjs';
import { linha } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const ids = a.p_entry_ids || [];
  if (!ids.length) throw new RpcError('Selecione ao menos uma linha do extrato.');
  const es = ids.map((id) => linha(ctx, id));
  const e0 = es[0];
  if (es.some((e) => e.bank_account_id !== e0.bank_account_id || e.import_id !== e0.import_id || e.status !== 'pending'))
    throw new RpcError('Todas as linhas devem estar pendentes e pertencer ao mesmo extrato, conta e empresa.');
  const soma = es.reduce((s, e) => s + num(e.amount), 0);
  const dias = es.map((e) => diaBR(e.posted_at)).sort();
  const d1 = addDias(dias[0], -5), d2 = addDias(dias[dias.length - 1], 5);
  const ocupados = new Set(store.rows('reconciliation_matches').map((m) => m.bank_transaction_id));
  const contas = new Map(store.rows('bank_accounts').filter((b) => b.company_id === e0.company_id).map((b) => [b.id, b]));
  const out = [];
  for (const dest of store.rows('bank_transactions')) {
    if (dest.bank_account_id !== e0.bank_account_id || !dest.group_id || ocupados.has(dest.id) || Math.abs(num(dest.amount) - soma) > 0.01) continue;
    const dia = dest.transaction_date || diaBR(dest.transaction_at);
    if (dia < d1 || dia > d2) continue;
    const grupo = store.rows('bank_transactions').filter((b) => b.group_id === dest.group_id);
    if (grupo.length !== 2) continue;
    const outra = grupo.find((b) => b.id !== dest.id);
    if (!outra || outra.bank_account_id === dest.bank_account_id || !contas.has(outra.bank_account_id) || Math.abs(num(outra.amount) + num(dest.amount)) > 0.01) continue;
    const saida = num(dest.amount) < 0 ? dest : outra, entrada = saida === dest ? outra : dest;
    out.push({ bank_transaction_id: dest.id, transfer_group_id: dest.group_id, transaction_at: dest.transaction_at, description: dest.description ?? null, amount: num(dest.amount),
      source_transaction_id: saida.id, source_account_id: saida.bank_account_id, source_account_name: contas.get(saida.bank_account_id)?.name ?? null,
      destination_account_id: entrada.bank_account_id, destination_account_name: contas.get(entrada.bank_account_id)?.name ?? null });
  }
  const T = (x) => new Date(x).getTime();
  const p = new Date(e0.posted_at).getTime();
  return out.sort((x, y) => Math.abs(T(x.transaction_at) - p) - Math.abs(T(y.transaction_at) - p)).slice(0, 20);
};
