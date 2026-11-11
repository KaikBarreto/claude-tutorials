// reconcile_settle_bill (T14 cap08, "Baixar conta"): baixa a conta inteira na data da linha (pay_financial_bill por transferência: lançamento
// "Pagamento: <conta>" com a categoria e o centro da conta) e casa a linha com esse lançamento (match_type bill_settlement).
import { num } from '../../lib/eco.mjs';
import { linha, pendente, casar, baixarConta } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const e = linha(ctx, a.p_entry_id);
  pendente(ctx, e);
  const bill = store.rows('financial_bills').find((b) => b.id === a.p_bill_id);
  if (!bill) throw new RpcError('Conta não encontrada.');
  if (bill.company_id !== e.company_id) throw new RpcError('Conta pertence a outra empresa.');
  if (!['pending', 'partial'].includes(bill.status)) throw new RpcError('Esta conta não está em aberto.');
  if (bill.direction === 'receivable' && num(e.amount) <= 0) throw new RpcError('Conta a receber exige uma entrada (crédito) no extrato.');
  if (bill.direction === 'payable' && num(e.amount) >= 0) throw new RpcError('Conta a pagar exige uma saída (débito) no extrato.');
  const resta = num(bill.amount) - num(bill.paid_amount);
  if (Math.abs(resta - Math.abs(num(e.amount))) > 0.01) throw new RpcError(`O valor da linha (R$ ${Math.abs(num(e.amount))}) não bate com o saldo devedor da conta (R$ ${resta}). Baixa parcial fora do MVP.`);
  const bt = baixarConta(ctx, e, bill);
  casar(ctx, e, bt, { tipo: 'bill_settlement', billId: bill.id });
  return bt.id;
};
