// reconcile_match_group(p_entry_ids, p_bank_transaction_id, p_confidence) (app 1.60.18: 20260818170000_reconcile_match_group.sql): casa N linhas do extrato com UM
// lançamento (o banco partiu em duas o que no sistema é um só). Mesma conta e extrato, todas pendentes, soma de mesmo sinal e até R$ 2,00 do lançamento;
// grava um vínculo por linha com o mesmo group_id e a diferença total na primeira. Devolve o group_id. T14 cap17.
import { casar, linha, pendente, agoraIso } from '../../lib/conciliacao.mjs';
import { r2, num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const ids = a.p_entry_ids || [];
  if (!ids.length) throw new RpcError('Nenhuma linha do extrato foi informada.');
  const bt = store.rows('bank_transactions').find((b) => b.id === a.p_bank_transaction_id);
  if (!bt) throw new RpcError('Lançamento não encontrado.');
  if (store.rows('reconciliation_matches').some((m) => m.bank_transaction_id === bt.id)) throw new RpcError('Este lançamento já está vinculado a outra(s) linha(s).');
  const es = ids.map((id) => linha(ctx, id));
  if (es.length < 2) throw new RpcError('Casar em grupo exige ao menos 2 linhas. Para 1 linha use o casamento simples.');
  es.forEach((e) => pendente(ctx, e));
  if (es.some((e) => e.bank_account_id !== bt.bank_account_id || e.import_id !== es[0].import_id)) throw new RpcError('Todas as linhas devem estar pendentes, na mesma conta/empresa do lançamento e no mesmo extrato.');
  const soma = r2(es.reduce((s, e) => s + num(e.amount), 0));
  if (Math.sign(soma) !== Math.sign(num(bt.amount))) throw new RpcError(`Sinais opostos: soma das linhas R$ ${soma} e lançamento R$ ${bt.amount} (não casa entrada com saída).`);
  const dif = r2(soma - num(bt.amount));
  if (Math.abs(dif) > 2.0 + 1e-9) throw new RpcError(`Soma das linhas (R$ ${soma}) não bate com o lançamento (R$ ${bt.amount}): diferença de R$ ${dif} acima do limite de R$ 2.00.`);
  const grupo = crypto.randomUUID();
  const primeira = [...es].sort((x, y) => String(x.posted_at).localeCompare(String(y.posted_at)) || String(x.id).localeCompare(String(y.id)))[0];
  for (const e of es) casar(ctx, e, bt, { confianca: a.p_confidence || 'manual', groupId: grupo, diferenca: e.id === primeira.id ? dif : 0 });
  return grupo;
};
