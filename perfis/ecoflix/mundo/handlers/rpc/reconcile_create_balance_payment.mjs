// reconcile_create_balance_payment(p_entry_id, p_entity_type, p_entity_id, p_description, p_allow_existing_exact) (app 1.60.18: 20260909010000_reconcile_create_balance_payment.sql):
// "Saldo do cliente/fornecedor" da conciliação. A linha vira um lançamento espelho na conta (fora da DRE, descrição "Valor Pago a <parceiro>" ou "Valor Recebido
// de <parceiro>"), um movimento de baixa na conta-corrente do parceiro (cliente: saldo - valor da linha; fornecedor: saldo + valor) e o vínculo balance_payment.
// Devolve { bank_transaction_id, balance_movement_id }. T14 cap17.
import { casar, linha, pendente } from '../../lib/conciliacao.mjs';
import { inserir, r2, num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  if (!['customer', 'supplier'].includes(a.p_entity_type)) throw new RpcError('Tipo de parceiro inválido (esperado cliente ou fornecedor).');
  if (!a.p_entity_id) throw new RpcError('Selecione o parceiro para lançar a baixa de saldo.');
  const e = linha(ctx, a.p_entry_id);
  pendente(ctx, e);
  if (!num(e.amount)) throw new RpcError('Linha de valor zero não pode virar baixa de saldo.');
  const p = store.rows(a.p_entity_type === 'customer' ? 'customers' : 'suppliers').find((x) => x.id === a.p_entity_id && x.company_id === e.company_id);
  if (!p) throw new RpcError('Parceiro inválido: não pertence a esta empresa.');
  const nome = (p.name || '').trim() || 'parceiro';
  const desc = (a.p_description || '').trim() || (num(e.amount) > 0 ? `Valor Recebido de ${nome}` : `Valor Pago a ${nome}`);
  const grupo = crypto.randomUUID();
  const bt = inserir(ctx, 'bank_transactions', { company_id: e.company_id, bank_account_id: e.bank_account_id, type: num(e.amount) > 0 ? 'deposit' : 'withdrawal', amount: Math.abs(num(e.amount)),
    description: desc, transaction_at: e.posted_at, source: 'manual', partner_id: a.p_entity_id, partner_type: a.p_entity_type, excluded_from_dre: true, group_id: grupo, created_by: ctx.userId });
  const delta = a.p_entity_type === 'customer' ? -num(e.amount) : num(e.amount);
  let bal = store.rows('balances').find((b) => b.company_id === e.company_id && b.entity_id === a.p_entity_id);
  if (!bal) bal = inserir(ctx, 'balances', { company_id: e.company_id, entity_type: a.p_entity_type, entity_id: a.p_entity_id, balance: 0 });
  db.update('balances', { id: bal.id }, { balance: r2(num(bal.balance) + delta) });
  const mov = inserir(ctx, 'balance_movements', { balance_id: bal.id, company_id: e.company_id, entity_type: a.p_entity_type, entity_id: a.p_entity_id, movement_type: 'payment', amount: delta,
    description: desc, payment_method: 'transfer', created_by: ctx.userId, group_id: grupo, transaction_at: e.posted_at, transaction_date: String(e.posted_at).slice(0, 10), bank_transaction_id: bt.id });
  casar(ctx, e, bt, { tipo: 'balance_payment' });
  db.update('reconciliation_matches', { entry_id: e.id }, { balance_movement_id: mov.id });
  return { bank_transaction_id: bt.id, balance_movement_id: mov.id };
};
