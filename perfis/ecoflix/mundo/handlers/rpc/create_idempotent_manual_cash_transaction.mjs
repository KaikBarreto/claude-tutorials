// Lançamento manual no caixa (entrada, saída/despesa) com chave de idempotência, como a função SQL.
import { inserir, agoraMs } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const cid = a.p_company_id || ctx.companyId;
  if (!a.p_client_request_id) throw new RpcError('client_request_id é obrigatório.', '22023');
  if (!['withdrawal', 'expense', 'deposit'].includes(a.p_type)) throw new RpcError(`Tipo de lançamento manual inválido: ${a.p_type}`, '22023');
  if (!(Number(a.p_amount) > 0)) throw new RpcError('O valor do lançamento deve ser maior que zero.', '22023');
  const ja = store.rows('cash_transactions').find((c) => c.company_id === cid && c.client_request_id === a.p_client_request_id);
  if (ja) return [{ id: ja.id, already_existed: true }];
  const cx = store.rows('cash_register').find((c) => c.id === a.p_cash_register_id);
  if (!cx || cx.company_id !== cid || cx.status !== 'open') throw new RpcError('CASH_REGISTER_CLOSED: caixa não encontrado, fechado ou de outra empresa.');
  const row = inserir(ctx, 'cash_transactions', {
    type: a.p_type, amount: Number(a.p_amount), description: a.p_description, cash_register_id: cx.id, company_id: cid, created_by: ctx.userId || a.p_created_by,
    category_id: a.p_category_id || null, transaction_at: a.p_transaction_at || new Date(agoraMs()).toISOString(), excluded_from_dre: !!a.p_excluded_from_dre,
    partner_type: a.p_partner_type || null, partner_id: a.p_partner_id || null, cost_center_id: a.p_cost_center_id || null, client_request_id: a.p_client_request_id,
  });
  return [{ id: row.id, already_existed: false }];
};
