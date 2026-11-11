// pay_partner_balance (app 1.59.154: supabase/migrations/20261002220000_v2_recebimento_conta_matriz_pela_filial.sql): baixa total ou
// parcial do saldo (fiado) de um parceiro, a tela "Receber de <parceiro>" / "Pagar a <parceiro>". Grava balance_movements ("payment",
// "Baixa de saldo (Recebimento|Pagamento)", o delta que leva o saldo rumo a zero), atualiza o saldo e lança o dinheiro no caixa aberto ou
// na conta bancária: "Recebimento de saldo" / "Pagamento de saldo" fora da DRE (ou "... categorizado de saldo" com categoria, na DRE),
// às 12:00 (Brasília) do dia pago. Devolve o saldo novo. T13 cap10.
import { inserir, r2, num } from '../../lib/eco.mjs';

const brl = (v) => num(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const cid = ctx.companyId;
  if (!['customer', 'supplier', 'party'].includes(a.p_entity_type)) throw new RpcError(`Tipo de parceiro inválido (${a.p_entity_type}). Use customer, supplier ou party.`);
  if (!a.p_entity_id) throw new RpcError('Parceiro obrigatório.');
  const valor = r2(num(a.p_amount));
  if (!(valor > 0)) throw new RpcError('O valor da baixa deve ser maior que zero.');
  if (!['cash', 'transfer'].includes(a.p_payment_method)) throw new RpcError(`Forma de pagamento inválida (${a.p_payment_method}). Use cash ou transfer.`);
  const bal = store.rows('balances').find((b) => b.company_id === cid && b.entity_type === a.p_entity_type && b.entity_id === a.p_entity_id);
  const atual = num(bal?.balance);
  if (!bal || !atual) throw new RpcError('Este parceiro não possui saldo em aberto para dar baixa.');
  const receber = (['customer', 'party'].includes(a.p_entity_type) && atual > 0) || (a.p_entity_type === 'supplier' && atual < 0);
  if (valor > Math.abs(atual) + 0.01) throw new RpcError(`O valor da baixa (R$ ${brl(valor)}) excede o saldo em aberto do parceiro (R$ ${brl(Math.abs(atual))}).`);
  const delta = atual > 0 ? -valor : valor;
  const rotulo = receber ? 'Recebimento' : 'Pagamento';
  const tipo = receber ? 'deposit' : 'withdrawal';
  const categoria = a.p_category_id || null;
  const desc = categoria ? `${rotulo} categorizado de saldo` : `${rotulo} de saldo`;
  const txAt = `${a.p_paid_date}T15:00:00.000Z`;   // 12:00 em Brasília (v_tx_at da RPC)
  let caixa = null;
  if (a.p_cash_register_id) {
    caixa = store.rows('cash_register').find((c) => c.id === a.p_cash_register_id && c.status === 'open');
    if (!caixa) throw new RpcError(`CASH_REGISTER_NOT_OPEN: caixa ${a.p_cash_register_id} nao esta aberto (ja fechado ou inexistente)`);
  }
  const mov = inserir(ctx, 'balance_movements', {
    balance_id: bal.id, company_id: cid, entity_type: a.p_entity_type, entity_id: a.p_entity_id, movement_type: 'payment', amount: delta,
    description: `Baixa de saldo (${rotulo})`, payment_method: a.p_payment_method, created_by: ctx.userId || null,
  });
  db.update('balances', { id: bal.id }, { balance: r2(atual + delta) });
  let tx;
  if (a.p_payment_method === 'cash') {
    if (!caixa) throw new RpcError('Caixa obrigatório para baixa em dinheiro.');
    tx = inserir(ctx, 'cash_transactions', {
      type: tipo, amount: valor, description: desc, cash_register_id: caixa.id, company_id: cid, created_by: ctx.userId || null,
      transaction_at: txAt, excluded_from_dre: !categoria, category_id: categoria,
    });
    db.update('balance_movements', { id: mov.id }, { cash_transaction_id: tx.id });
  } else {
    if (!a.p_bank_account_id) throw new RpcError('Conta bancária obrigatória para baixa por transferência.');
    tx = inserir(ctx, 'bank_transactions', {
      type: tipo, amount: valor, description: desc, bank_account_id: a.p_bank_account_id, cash_register_id: a.p_cash_register_id || null,
      company_id: cid, created_by: ctx.userId || null, transaction_at: txAt, excluded_from_dre: !categoria, category_id: categoria, origin_company_id: cid,
    });
    db.update('balance_movements', { id: mov.id }, { bank_transaction_id: tx.id });
  }
  return r2(atual + delta);
};
