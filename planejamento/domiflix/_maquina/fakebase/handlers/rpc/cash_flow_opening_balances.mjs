// RPC cash_flow_opening_balances(p_today date) → TABLE (account_id, balance) · 20261018230000_fluxo_de_caixa_previsto_base.sql:253-290
// Saldo de PARTIDA do DFC previsto (aba "DFC - Fluxo de Caixa" → "Previsto", cartão "Saldo atual"), por conta que não é cartão:
//   initial_balance + Σ(entrada − saída) das transações com is_paid, sem cancelamento, sem credit_card_bill_date (compra de cartão não é caixa),
//   paid_date preenchido e <= p_today. Mesma régua do cliente (`deriveForecastOpeningBalances`). Criado no T20.
export default async function cashFlowOpeningBalances({ p_today }, { db }) {
  const hoje = String(p_today || '').slice(0, 10) || new Date().toISOString().slice(0, 10);
  const contas = db.rows('financial_accounts').filter((a) => a.type !== 'cartao');
  const delta = new Map();
  for (const t of db.rows('financial_transactions')) {
    if (t.is_paid !== true || t.cancelled_at || t.credit_card_bill_date || !t.paid_date || !t.account_id) continue;
    if (String(t.paid_date).slice(0, 10) > hoje) continue;
    const v = Number(t.amount || 0) * (t.transaction_type === 'entrada' ? 1 : -1);
    delta.set(t.account_id, (delta.get(t.account_id) || 0) + v);
  }
  return contas.map((a) => ({ account_id: a.id, balance: Math.round((Number(a.initial_balance || 0) + (delta.get(a.id) || 0)) * 100) / 100 }));
}
