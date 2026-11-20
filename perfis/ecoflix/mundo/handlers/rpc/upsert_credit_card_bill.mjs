// upsert_credit_card_bill(p_card_account_id, p_reference_month) (app 1.60.18: 20260904100100_credit_card_rpcs.sql): garante a fatura do mês (idempotente).
// Fechamento = dia de fechamento do cartão no mês de referência (limitado ao último dia); vencimento = dia de vencimento do mês seguinte. T14 cap03.
import { inserir } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const c = store.rows('bank_accounts').find((b) => b.id === a.p_card_account_id);
  if (!c) throw new RpcError(`Cartão não encontrado (id ${a.p_card_account_id}).`);
  if (c.kind !== 'card') throw new RpcError('A conta informada não é um cartão de crédito.');
  const [y, m] = String(a.p_reference_month).slice(0, 7).split('-').map(Number);
  const ref = `${y}-${String(m).padStart(2, '0')}-01`;
  const fim = (ano, mes) => new Date(Date.UTC(ano, mes, 0)).getUTCDate();
  const dia = (ano, mes, d) => `${ano}-${String(mes).padStart(2, '0')}-${String(Math.min(d, fim(ano, mes))).padStart(2, '0')}`;
  const ny = m === 12 ? y + 1 : y, nm = m === 12 ? 1 : m + 1;
  const closing = dia(y, m, c.closing_day || 10), due = dia(ny, nm, c.due_day || 10);
  const ex = store.rows('credit_card_bills').find((b) => b.card_account_id === c.id && b.reference_month === ref);
  if (ex) { ctx.db.update('credit_card_bills', { id: ex.id }, { closing_date: closing, due_date: due }); return ex.id; }
  return inserir(ctx, 'credit_card_bills', { company_id: c.company_id, card_account_id: c.id, reference_month: ref, closing_date: closing, due_date: due, status: 'open', amount_paid: 0 }).id;
};
