// T10 · gatilhos de lead_assignees (20260917150000): um unico principal por oportunidade (BEFORE rebaixa os outros) e
// leads.assigned_to espelha o principal (AFTER). Apagar o principal limpa leads.assigned_to.
import { db } from '../core/db.mjs';

function espelharNoLead(leadId, userId) {
  const lead = db.first('leads', { id: leadId });
  if (lead && (lead.assigned_to ?? null) !== (userId ?? null)) db.update('leads', { id: leadId }, { assigned_to: userId });
}

export default {
  beforeInsert(row) {
    if (row.is_primary === null || row.is_primary === undefined) row.is_primary = false;
    if (row.is_primary) {
      for (const o of db.rows('lead_assignees').filter((a) => a.lead_id === row.lead_id && a.user_id !== row.user_id && a.is_primary)) o.is_primary = false;
    }
  },
  afterInsert(row) {
    if (row.is_primary) espelharNoLead(row.lead_id, row.user_id);
  },
  beforeUpdate(row, patch) {
    if (patch.is_primary === true) {
      for (const o of db.rows('lead_assignees').filter((a) => a.lead_id === row.lead_id && a.user_id !== row.user_id && a.is_primary)) o.is_primary = false;
    }
  },
  afterUpdate(row) {
    if (row.is_primary) espelharNoLead(row.lead_id, row.user_id);
  },
  afterDelete(row) {
    if (row.is_primary) {
      const lead = db.first('leads', { id: row.lead_id });
      if (lead && lead.assigned_to === row.user_id) db.update('leads', { id: row.lead_id }, { assigned_to: null });
    }
  },
};
