// Edge check-asaas-payment, SEM Asaas: o checkout pergunta a cada 5 s se a cobrança foi paga. Responde pela linha de subscription_payments
// gravada pelo create-group-payment (RECEIVED/CONFIRMED = pago). O "pagamento" da T22 é um passo de bastidor do robô (PATCH dessa linha para
// RECEIVED); nenhum dinheiro de verdade.
export default (body, { store, FunctionError }) => {
  const id = body?.payment_id;
  if (!id) throw new FunctionError(400, 'payment_id is required');
  const p = store.rows('subscription_payments').find((x) => x.asaas_payment_id === id);
  const st = p?.status || 'PENDING';
  return { status: st === 'RECEIVED' ? 'CONFIRMED' : st, is_paid: st === 'RECEIVED' || st === 'CONFIRMED', payment_id: id };
};
