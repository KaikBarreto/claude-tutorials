// reconcile_match_entry_split(p_entry_id, p_bank_transaction_ids, p_confidence) (app 1.60.18: 20261002210000_conciliacao_uma_linha_para_n_lancamentos.sql): casa UMA
// linha do extrato com N lançamentos (um Pix que pagou dois pedidos). Pelo menos 2 lançamentos livres da mesma conta e mesmo sinal da linha, soma até R$ 2,00
// da linha; um vínculo por lançamento com o mesmo group_id e a diferença total no primeiro. Devolve o group_id. T14 cap17.
import { casar, linha, pendente } from '../../lib/conciliacao.mjs';
import { r2, num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const e = linha(ctx, a.p_entry_id);
  pendente(ctx, e);
  const ids = [...new Set(a.p_bank_transaction_ids || [])];
  if (ids.length < 2) throw new RpcError('Casar uma linha com vários lançamentos exige ao menos 2 lançamentos.');
  const bts = ids.map((id) => store.rows('bank_transactions').find((b) => b.id === id));
  if (bts.some((b) => !b)) throw new RpcError('Algum lançamento informado não existe.');
  const ocupados = new Set(store.rows('reconciliation_matches').map((m) => m.bank_transaction_id));
  if (bts.some((b) => ocupados.has(b.id))) throw new RpcError('Algum lançamento já está vinculado a outra linha.');
  if (bts.some((b) => b.bank_account_id !== e.bank_account_id)) throw new RpcError('Todos os lançamentos devem ser da mesma conta da linha.');
  const soma = r2(bts.reduce((s, b) => s + num(b.amount), 0));
  if (Math.sign(soma) !== Math.sign(num(e.amount))) throw new RpcError('Sinais opostos: a soma dos lançamentos não casa com a linha.');
  const dif = r2(num(e.amount) - soma);
  if (Math.abs(dif) > 2.0 + 1e-9) throw new RpcError(`Soma dos lançamentos (R$ ${soma}) não bate com a linha (R$ ${e.amount}): diferença de R$ ${dif} acima do limite de R$ 2.00.`);
  const grupo = crypto.randomUUID();
  const T = (x) => new Date(x.transaction_at).getTime();
  const primeiro = [...bts].sort((x, y) => T(x) - T(y) || String(x.id).localeCompare(String(y.id)))[0];
  bts.forEach((b) => casar(ctx, e, b, { confianca: a.p_confidence || 'manual', groupId: grupo, diferenca: b.id === primeiro.id ? dif : 0 }));
  return grupo;
};
