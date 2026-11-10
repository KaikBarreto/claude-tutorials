// T26 · reorder_company_crm_opportunities(p_stage_id, p_ordered_ids) (migration 20261002160000): renumera 0..N-1 os cartões da
// etapa na ordem do arraste; id repetido vale pela primeira ocorrência e id de outra etapa ou empresa é ignorado. Devolve quantos mudaram.
export default (a, { store, companyId }) => {
  const etapa = store.rows('crm_stages').find((s) => s.id === a.p_stage_id);
  if (!etapa || etapa.company_id !== companyId) return 0;
  const ids = [...new Set((Array.isArray(a.p_ordered_ids) ? a.p_ordered_ids : []).filter(Boolean).map(String))];
  let n = 0;
  ids.forEach((id, pos) => {
    const o = store.rows('crm_opportunities').find((x) => x.id === id && x.company_id === etapa.company_id && x.stage_id === etapa.id);
    if (o && Number(o.position) !== pos) {
      o.position = pos;
      n++;
    }
  });
  if (n) store.table('crm_opportunities').touch();
  return n;
};
