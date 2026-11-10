// Edge geocode-company (chamada pelo save do endereço da empresa, sem esperar resposta): no mundo a empresa já tem lat/lng do
// pátio em Taubaté (mundo.json "navegador.geolocalizacao"); nada muda.
export default (body, { store }) => {
  const c = store.rows('companies').find((x) => x.id === body?.company_id) || store.rows('companies')[0];
  return { success: true, lat: c?.lat ?? null, lng: c?.lng ?? null, status: c?.geocode_status || 'ok' };
};
