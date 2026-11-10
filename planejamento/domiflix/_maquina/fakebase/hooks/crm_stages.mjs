// T10 · gatilhos de crm_stages (supabase/migrations/20260918100000_crm_multi_pipeline.sql):
//  (i) trg_crm_stages_resolve_pipeline: etapa SEM pipeline_id vai para o funil padrao da empresa; se nao ha funil, o banco cria o
//      "Funil de Vendas" (is_default, posicao 0). E o que faz o "Começar com estágios padrão" funcionar (o app nao manda pipeline_id).
//  (ii) trg_crm_stages_propagate_pipeline: mudar a etapa de funil leva os leads dela junto (leads.pipeline_id).
import { db } from '../core/db.mjs';

/** ensure_default_crm_pipeline(company): padrao existente > primeiro funil comercial (promovido) > cria "Funil de Vendas". */
export function garantirFunilPadrao(companyId) {
  const funis = db.rows('crm_pipelines').filter((p) => p.company_id === companyId && !p.project_id);
  const padrao = funis.find((p) => p.is_default);
  if (padrao) return padrao.id;
  const primeiro = [...funis].sort((a, b) => (a.position ?? 0) - (b.position ?? 0) || String(a.created_at).localeCompare(String(b.created_at)))[0];
  if (primeiro) {
    db.update('crm_pipelines', { id: primeiro.id }, { is_default: true });
    return primeiro.id;
  }
  return db.insert('crm_pipelines', { company_id: companyId, name: 'Funil de Vendas', position: 0, is_default: true, color: '#2563EB', tracks_value: true }).id;
}

export default {
  beforeInsert(row, hc) {
    if (!row.pipeline_id) row.pipeline_id = garantirFunilPadrao(row.company_id || hc.companyId);
    if (row.is_won === null || row.is_won === undefined) row.is_won = false;
    if (row.is_lost === null || row.is_lost === undefined) row.is_lost = false;
    if (row.position === null || row.position === undefined) row.position = 0;
  },
  afterUpdate(row, hc) {
    const leads = hc.store.peek('leads');
    if (!leads) return;
    let mudou = false;
    for (const l of leads.rows) {
      if (l.stage_id === row.id && l.pipeline_id !== row.pipeline_id) {
        l.pipeline_id = row.pipeline_id;
        mudou = true;
      }
    }
    if (mudou) leads.touch();
  },
};
