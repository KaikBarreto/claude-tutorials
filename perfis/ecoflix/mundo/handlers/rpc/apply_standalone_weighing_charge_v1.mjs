// Cobrança da pesagem avulsa (T8, app 1.59.163+): espelha apply_standalone_weighing_charge_v1 da migration
// 20261111193000_standalone_weighing_financial_charge.sql. Ticket avulso pendente com weighing_fee > 0: lança a receita na categoria
// "Serviço de pesagem" (criada se faltar) em dinheiro no caixa (depósito idempotente), por Pix/transferência na conta bancária, ou no
// saldo do cliente (movimento weighing_charge + conta a receber), e marca o ticket como charged. Idempotente (ticket já cobrado volta
// com already_existed). As mensagens de erro são as da migration.
import { inserir, atualizaSaldo, agoraMs, r2, num } from '../../lib/eco.mjs';
import caixaManual from './create_idempotent_manual_cash_transaction.mjs';
import bancoManual from './create_manual_bank_transaction.mjs';

export function cobrarPesagemAvulsa(ctx, ticketId, cid, intent) {
  const { store, RpcError } = ctx;
  const t = store.rows('weighing_tickets').find((x) => x.id === ticketId && x.company_id === cid);
  if (!t) throw new RpcError('Ticket de pesagem não encontrado para esta empresa.', 'WT004');
  if (t.standalone_charge_status === 'charged') {
    return { ticket_id: t.id, charge_status: 'charged', already_existed: true, cash_transaction_id: t.standalone_cash_transaction_id ?? null,
      bank_transaction_id: t.standalone_bank_transaction_id ?? null, balance_movement_id: t.standalone_balance_movement_id ?? null,
      receivable_id: t.standalone_receivable_id ?? null };
  }
  if (t.ticket_kind !== 'standalone' || t.status !== 'pending') throw new RpcError('A cobrança só pode ser lançada em uma pesagem avulsa finalizada.', 'WT006');
  const fee = r2(t.weighing_fee);
  if (fee <= 0) throw new RpcError('Informe um valor maior que zero para cobrar a pesagem.', '22023');
  if (!intent || typeof intent !== 'object' || Array.isArray(intent)) throw new RpcError('Confirme a forma de pagamento da pesagem.', '22023');
  const cash = r2(intent.cash_amount), transfer = r2(intent.transfer_amount), balance = r2(intent.balance_amount);
  if (cash < 0 || transfer < 0 || balance < 0 || Math.abs(cash + transfer + balance - fee) > 0.005) {
    throw new RpcError('A soma das formas de pagamento deve ser igual ao valor da pesagem.', '22023');
  }
  const caixaId = intent.cash_register_id || null, contaId = intent.bank_account_id || null, venc = intent.balance_due_date || null;
  if (cash > 0 && !caixaId) throw new RpcError('Selecione o caixa que recebeu o dinheiro.', '22023');
  if (transfer > 0 && !contaId) throw new RpcError('Selecione a conta bancária que recebeu o Pix/transferência.', '22023');
  if (balance > 0 && (!t.customer_supplier_id || t.customer_supplier_type !== 'customer')) {
    throw new RpcError('Selecione um cliente para lançar a pesagem no saldo.', '22023');
  }
  let cat = store.rows('financial_categories').find((c) => c.company_id === cid && c.name === 'Serviço de pesagem' && c.type === 'income');
  if (!cat) cat = inserir(ctx, 'financial_categories', { company_id: cid, name: 'Serviço de pesagem', type: 'income', color: '#16A34A', is_system: true });
  const desc = `Serviço de pesagem avulsa ${t.ticket_ref || '#' + t.ticket_number}`;
  const parceiro = t.customer_supplier_id || null, tipoParceiro = parceiro ? 'customer' : null;
  let caixaTx = null, bancoTx = null, movId = null, receberId = null;
  if (cash > 0) {
    caixaTx = caixaManual({ p_type: 'deposit', p_amount: cash, p_description: desc, p_cash_register_id: caixaId, p_company_id: cid, p_category_id: cat.id,
      p_transaction_at: t.created_at, p_excluded_from_dre: false, p_partner_id: parceiro, p_partner_type: tipoParceiro, p_client_request_id: ticketId,
      p_created_by: t.created_by }, ctx)[0].id;
  }
  if (transfer > 0) {
    bancoTx = bancoManual({ p_type: 'deposit', p_amount: transfer, p_description: desc, p_bank_account_id: contaId, p_company_id: cid, p_category_id: cat.id,
      p_transaction_at: t.created_at, p_group_id: ticketId, p_excluded_from_dre: false, p_partner_id: parceiro, p_partner_type: tipoParceiro,
      p_payment_method: 'transfer', p_created_by: t.created_by }, ctx)[0].id;
  }
  if (balance > 0) {
    const saldo = atualizaSaldo(ctx, cid, 'customer', parceiro, num(balance));
    movId = inserir(ctx, 'balance_movements', { company_id: cid, balance_id: saldo.id, entity_type: 'customer', entity_id: parceiro,
      movement_type: 'weighing_charge', amount: balance, description: desc, order_id: ticketId, payment_method: 'balance', group_id: ticketId,
      created_by: ctx.userId || t.created_by, transaction_at: t.created_at }).id;
    receberId = inserir(ctx, 'financial_bills', { company_id: cid, direction: 'receivable', description: desc, category_id: cat.id, amount: balance,
      paid_amount: 0, due_date: venc, status: 'pending', partner_type: 'customer', partner_id: parceiro, order_id: ticketId, order_type: 'weighing_ticket',
      source_type: 'weighing_ticket_charge', source_id: ticketId, is_projection: false, created_by: ctx.userId || t.created_by }).id;
  }
  Object.assign(t, { payment_intent: intent, standalone_charge_status: 'charged', standalone_charge_group_id: ticketId, standalone_cash_transaction_id: caixaTx,
    standalone_bank_transaction_id: bancoTx, standalone_balance_movement_id: movId, standalone_receivable_id: receberId, updated_at: new Date(agoraMs()).toISOString() });
  store.table('weighing_tickets').touch();
  return { ticket_id: ticketId, charge_status: 'charged', already_existed: false, cash_transaction_id: caixaTx, bank_transaction_id: bancoTx,
    balance_movement_id: movId, receivable_id: receberId };
}

export default (a, ctx) => cobrarPesagemAvulsa(ctx, a.p_ticket_id, a.p_company_id || ctx.companyId, a.p_payment_intent);
