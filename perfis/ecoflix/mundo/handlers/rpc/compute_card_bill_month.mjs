// compute_card_bill_month(p_card_account_id, p_date) (app 1.60.18: 20260904100100_credit_card_rpcs.sql): em que fatura cai a compra. Dia do fechamento
// (padrão 10, mês curto limita ao último dia) já é da fatura do mês seguinte. Devolve o dia 1 do mês de referência. T14 cap03 (Cartão de crédito).
export default (a, { store, RpcError }) => {
  if (!a.p_card_account_id || !a.p_date) return null;
  const c = store.rows('bank_accounts').find((b) => b.id === a.p_card_account_id);
  if (!c) throw new RpcError(`Cartão não encontrado (id ${a.p_card_account_id}).`);
  const [y, m, d] = String(a.p_date).slice(0, 10).split('-').map(Number);
  const fecha = Math.min(c.closing_day || 10, new Date(Date.UTC(y, m, 0)).getUTCDate());
  const ref = d >= fecha ? new Date(Date.UTC(y, m, 1)) : new Date(Date.UTC(y, m - 1, 1));
  return ref.toISOString().slice(0, 10);
};
