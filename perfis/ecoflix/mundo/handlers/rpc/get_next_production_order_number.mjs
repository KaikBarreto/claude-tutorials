// Próximo número da ordem de produção, por empresa (T11): MAX(order_number) + 1, como a função SQL da 1.59.154 (20260820120200).
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  return store.rows('production_orders').filter((o) => o.company_id === cid).reduce((m, o) => Math.max(m, Number(o.order_number) || 0), 0) + 1;
};
