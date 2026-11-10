// T10 · gatilhos de leads (oportunidades do CRM):
//  - trg_leads_resolve_pipeline (20260918100000): leads.pipeline_id SEMPRE = funil da etapa; sem etapa, o funil padrao da empresa.
//  - trg_leads_sync_primary_assignee (20260917150000): leads.assigned_to espelha o responsavel principal em lead_assignees
//    (trocar/limpar assigned_to remove o principal antigo e cria o novo). O sentido contrario esta em hooks/lead_assignees.mjs.
//  - DEFAULTs do banco: status 'lead', value 0, listas vazias.
import { db } from '../core/db.mjs';
import { garantirFunilPadrao } from './crm_stages.mjs';

function resolverFunil(row, hc) {
  const etapa = row.stage_id ? db.first('crm_stages', { id: row.stage_id }) : null;
  if (etapa) {
    row.pipeline_id = etapa.pipeline_id;
    return;
  }
  const funil = row.pipeline_id ? db.first('crm_pipelines', { id: row.pipeline_id }) : null;
  if (!funil) row.pipeline_id = garantirFunilPadrao(row.company_id || hc.companyId);
}

function espelhar(lead) {
  const t = db.rows('lead_assignees');
  const mesmo = t.filter((a) => a.lead_id === lead.id);
  for (const a of mesmo.filter((x) => x.is_primary && x.user_id !== lead.assigned_to)) db.remove('lead_assignees', (r) => r === a);
  if (lead.assigned_to) {
    const ja = db.first('lead_assignees', (a) => a.lead_id === lead.id && a.user_id === lead.assigned_to);
    if (ja) {
      if (!ja.is_primary) db.update('lead_assignees', (r) => r === ja, { is_primary: true });
    } else {
      db.insert('lead_assignees', { lead_id: lead.id, user_id: lead.assigned_to, is_primary: true });
    }
  }
}

export default {
  beforeInsert(row, hc) {
    if (!row.status) row.status = 'lead';
    if (row.value === null || row.value === undefined) row.value = 0;
    resolverFunil(row, hc);
  },
  afterInsert(row) {
    if (row.assigned_to) espelhar(row);
  },
  beforeUpdate(row, patch, hc) {
    if ('stage_id' in patch || 'pipeline_id' in patch) {
      const tmp = { ...row, ...patch };
      resolverFunil(tmp, hc);
      patch.pipeline_id = tmp.pipeline_id;
    }
  },
  afterUpdate(row, hc) {
    // so quando assigned_to mudou em relacao ao principal gravado (evita refazer a cada PATCH de etapa/observacao)
    const prim = db.first('lead_assignees', (a) => a.lead_id === row.id && a.is_primary);
    if ((prim?.user_id ?? null) !== (row.assigned_to ?? null)) espelhar(row);
  },
};
