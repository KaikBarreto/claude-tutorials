// Próximo número de ordem de coleta (20260826120400): maior `numero` da empresa + 1. Usado pela "Nova ordem" e pelo portal.
export default (a, { store, companyId }) => {
  const co = a.p_company_id || companyId;
  return store.rows('collection_orders').filter((o) => o.company_id === co).reduce((m, o) => Math.max(m, Number(o.numero) || 0), 0) + 1;
};
