// "Próxima DPS: nº N" na Nova NFS-e (T17, app 1.60.10; hooks/useNfseSeries.ts, migration 20261113235000): o próximo número livre
// da série = o maior entre o último número da série (`nfse_series.last_nfse_number`) e o maior número já usado nas notas, mais um.
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const serie = Number(a.p_serie) || 1;
  const doEmitente = (r) => r.company_id === cid && (!a.p_fiscal_config_id || !r.fiscal_config_id || r.fiscal_config_id === a.p_fiscal_config_id);
  const s = store.rows('nfse_series').find((r) => doEmitente(r) && Number(r.serie_number) === serie);
  const usados = store.rows('nfse_invoices').filter((n) => doEmitente(n) && Number(n.serie || 1) === serie).map((n) => Number(n.nfse_number) || 0);
  return Math.max(Number(s?.last_nfse_number) || 0, ...usados) + 1;
};
