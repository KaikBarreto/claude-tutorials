// reconcile_match_existing (T14 caps 7, 10, 12, 13): liga a linha a um lançamento que já existe (match_type existing). Automático exige valor
// exato e a janela de 3 dias; manual tolera até R$ 2,00 do mesmo sinal (grava value_difference); p_allow_any_date pula a janela.
import { num } from '../../lib/eco.mjs';
import { linha, pendente, tipoOk, casar } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const e = linha(ctx, a.p_entry_id);
  pendente(ctx, e);
  const bt = store.rows('bank_transactions').find((b) => b.id === a.p_bank_transaction_id);
  if (!bt) throw new RpcError('Lançamento não encontrado.');
  if (bt.bank_account_id !== e.bank_account_id) throw new RpcError('Lançamento não pertence à mesma conta/empresa da linha.');
  const conf = a.p_confidence || 'manual';
  if (!['auto', 'manual'].includes(conf)) throw new RpcError(`confidence inválido (${conf}).`);
  if (!tipoOk(bt) && !(bt.order_id && bt.type === 'transfer')) throw new RpcError(`Tipo de lançamento ${bt.type} não pode ser conciliado.`);
  const dif = num(e.amount) - num(bt.amount);
  if (conf === 'auto' && Math.abs(dif) > 0.005) throw new RpcError(`Valor do lançamento (R$ ${bt.amount}) não bate com a linha do extrato (R$ ${e.amount}).`);
  if (Math.sign(num(bt.amount)) !== Math.sign(num(e.amount))) throw new RpcError(`Não é possível casar entrada com saída: lançamento R$ ${bt.amount} e linha R$ ${e.amount} têm sinais opostos.`);
  if (Math.abs(dif) > 2.0 + 1e-9) throw new RpcError(`Diferença de valor acima do limite: lançamento R$ ${bt.amount} e linha R$ ${e.amount} divergem em mais de R$ 2,00.`);
  if (!a.p_allow_any_date) {
    const d = Math.abs(new Date(bt.transaction_at).getTime() - new Date(e.posted_at).getTime());
    if (d > 3 * 86400000) throw new RpcError('Lançamento fora da janela de datas da linha.');
  }
  if (store.rows('reconciliation_matches').some((m) => m.bank_transaction_id === bt.id)) throw new RpcError('Este lançamento já está vinculado a outra linha.');
  casar(ctx, e, bt, { tipo: 'existing', confianca: conf, diferenca: dif });
  return null;
};
