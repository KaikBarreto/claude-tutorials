// record_partner_balance_movement(p_company_id, p_entity_type, p_entity_id, p_amount, p_operation_type, p_payment_method,
// p_description, p_cash_register_id, p_bank_account_id, p_transaction_at, p_client_request_id) — app 1.60.10, migration
// 20261110235200_partner_balance_movement_atomic.sql. A "Nova Movimentação de Saldo" (components/BalancePaymentModal.tsx) deixou de
// fazer três chamadas (lançamento + update_balance + insert em balance_movements) e passou a esta RPC só: lança o dinheiro (caixa
// aberto ou conta bancária, fora da DRE, com o parceiro), soma o delta ao saldo (crédito +, débito −; parceiro duplo na linha
// `party`) e grava o movimento "payment" com o mesmo group_id (= p_client_request_id, a chave de idempotência). Devolve
// { movement_id, balance_id, balance, already_existed }. Usado por T04 (Pix de R$ 1.200,00 à Cooperativa), T07 (vale do Valdir),
// T13, T20 e T25.
import { inserir, atualizar, atualizaSaldo, agoraMs, num, r2 } from '../../lib/eco.mjs';
import cashManual from './create_idempotent_manual_cash_transaction.mjs';
import bankManual from './create_manual_bank_transaction.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const cid = a.p_company_id || ctx.companyId;
  if (!cid) throw new RpcError('Empresa não resolvida para a movimentação de saldo.', '42501');
  if (!['customer', 'supplier'].includes(a.p_entity_type)) throw new RpcError(`Tipo de parceiro inválido: ${a.p_entity_type}`, '22023');
  if (!a.p_entity_id) throw new RpcError('Parceiro obrigatório.', '22023');
  const valor = r2(num(a.p_amount));
  if (!(valor > 0)) throw new RpcError('O valor deve ser maior que zero.', '22023');
  if (!['credit', 'debit'].includes(a.p_operation_type)) throw new RpcError(`Operação inválida: ${a.p_operation_type}`, '22023');
  if (!['cash', 'transfer'].includes(a.p_payment_method)) throw new RpcError(`Forma de pagamento inválida: ${a.p_payment_method}`, '22023');
  if (!a.p_client_request_id) throw new RpcError('client_request_id é obrigatório.', '22023');
  const parceiro = store.rows(a.p_entity_type === 'customer' ? 'customers' : 'suppliers').find((x) => x.id === a.p_entity_id);
  if (!parceiro || parceiro.company_id !== cid) throw new RpcError('Parceiro não encontrado nesta empresa.', '42501');

  const req = a.p_client_request_id;
  const ja = store.rows('balance_movements').filter((m) => m.company_id === cid && m.group_id === req)
    .sort((x, y) => String(x.created_at).localeCompare(String(y.created_at)) || String(x.id).localeCompare(String(y.id)))[0];
  if (ja) {
    const b = store.rows('balances').find((x) => x.id === ja.balance_id && x.company_id === cid);
    return { movement_id: ja.id, balance_id: ja.balance_id, balance: b ? num(b.balance) : null, already_existed: true };
  }
  const pernaSolta = store.rows('cash_transactions').some((c) => c.company_id === cid && (c.group_id === req || c.client_request_id === req))
    || store.rows('bank_transactions').some((b) => (b.origin_company_id || b.company_id) === cid && (b.group_id === req || b.client_request_id === req));
  if (pernaSolta) throw new RpcError('BALANCE_PAY_PARTIAL_LEGACY: existe perna financeira sem movimento de saldo para esta requisição.', 'P0001');

  const delta = a.p_operation_type === 'debit' ? -valor : valor;
  // cliente: débito = ele pagou (entrada); crédito = a empresa devolveu (saída). Fornecedor: débito = a empresa pagou (saída).
  const tipoTx = a.p_entity_type === 'customer' ? (a.p_operation_type === 'debit' ? 'deposit' : 'withdrawal') : (a.p_operation_type === 'debit' ? 'withdrawal' : 'deposit');
  const quando = a.p_transaction_at || new Date(agoraMs()).toISOString();
  let cashId = null, bankId = null;
  if (a.p_payment_method === 'cash') {
    if (!a.p_cash_register_id) throw new RpcError('Caixa obrigatório para movimentação em dinheiro.', '22023');
    cashId = cashManual({ p_type: tipoTx, p_amount: valor, p_description: a.p_description, p_cash_register_id: a.p_cash_register_id, p_company_id: cid, p_transaction_at: quando, p_excluded_from_dre: true, p_partner_id: a.p_entity_id, p_partner_type: a.p_entity_type, p_client_request_id: req, p_created_by: ctx.userId }, ctx)[0].id;
    atualizar(ctx, 'cash_transactions', { id: cashId }, { group_id: req });
  } else {
    bankId = bankManual({ p_type: tipoTx, p_amount: valor, p_description: a.p_description, p_bank_account_id: a.p_bank_account_id, p_company_id: cid, p_cash_register_id: a.p_cash_register_id, p_transaction_at: quando, p_group_id: req, p_excluded_from_dre: true, p_partner_id: a.p_entity_id, p_partner_type: a.p_entity_type, p_payment_method: 'transfer', p_created_by: ctx.userId }, ctx)[0].id;
    atualizar(ctx, 'bank_transactions', { id: bankId }, { client_request_id: req });
  }
  const saldo = atualizaSaldo(ctx, cid, a.p_entity_type, a.p_entity_id, delta);
  const mov = inserir(ctx, 'balance_movements', {
    balance_id: saldo.id, company_id: cid, entity_type: a.p_entity_type, entity_id: a.p_entity_id, movement_type: 'payment', amount: delta,
    description: a.p_description || null, payment_method: a.p_payment_method, cash_register_id: a.p_payment_method === 'cash' ? a.p_cash_register_id : null,
    cash_transaction_id: cashId, bank_transaction_id: bankId, created_by: ctx.userId, group_id: req, transaction_at: quando, is_settled: false,
  });
  return { movement_id: mov.id, balance_id: saldo.id, balance: num(saldo.balance), already_existed: false };
};
