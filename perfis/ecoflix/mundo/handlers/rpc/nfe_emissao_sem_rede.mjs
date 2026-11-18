// RPC nfe_emissao_sem_rede (migration 20261110160000_nfe_emissao_sem_rede; hooks/useNfeEmissaoSemRede.ts, aviso "Este tipo de ICMS ainda
// não pode ser emitido por aqui" da tela de Impostos): TRUE só quando a empresa emite em rota exclusiva do motor próprio
// (nfe_emission_routes com stage 'direct' e sem legacy_fallback_enabled). Empresa sem linha de rota (a Recicla Vale) = false.
export default (a, { store, companyId }) => {
  const cid = a?.p_company_id || companyId;
  let rotas = [];
  try { rotas = store.rows('nfe_emission_routes') || []; } catch { rotas = []; }
  return rotas.some((r) => r.company_id === cid && r.stage === 'direct' && !r.legacy_fallback_enabled);
};
