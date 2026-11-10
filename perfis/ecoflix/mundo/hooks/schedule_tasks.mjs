// T26 · triggers de schedule_tasks só para as tarefas do CRM (crm_opportunity_id preenchido; as da Agenda comum não mudam):
//  AFTER UPDATE OF status  crm_sync_task_checklist_and_automations_trigger (checklist ligado à tarefa e os gatilhos "Ao concluir
//                          uma tarefa" / "Quando tudo estiver concluído") e schedule_tasks_log_crm_status_change (histórico:
//                          'Tarefa "<título>" marcada como <status>.'). Lógica em lib/crm.mjs.
import { registraStatusDaTarefa, rodaAutomacoes, chaveEvento, isoAgora } from '../lib/crm.mjs';

const antes = new Map(); // id -> status antes do UPDATE em curso

export default {
  beforeUpdate(row) {
    if (row.crm_opportunity_id) antes.set(row.id, row.status);
  },
  afterUpdate(row, hc) {
    if (!antes.has(row.id)) return;
    const de = antes.get(row.id);
    antes.delete(row.id);
    if (!row.crm_opportunity_id || de === row.status) return;
    const opp = hc.store.rows('crm_opportunities').find((o) => o.id === row.crm_opportunity_id);
    if (opp && row.crm_checklist_id && (row.status === 'concluida' || de === 'concluida')) {
      const feito = row.status === 'concluida';
      opp.checklists = (opp.checklists || []).map((c) => (c.id === row.crm_checklist_id ? { ...c, items: (c.items || []).map((i) => ({ ...i, done: feito })) } : c));
      opp.updated_at = isoAgora();
      hc.store.table('crm_opportunities').touch();
    }
    if (row.status === 'concluida' && de !== 'concluida') {
      rodaAutomacoes(hc, row.crm_opportunity_id, 'task_completed', chaveEvento('task', row.crm_opportunity_id, row.id), row.title);
      rodaAutomacoes(hc, row.crm_opportunity_id, 'all_completed', chaveEvento('all', row.crm_opportunity_id));
    }
    registraStatusDaTarefa(hc, row, de);
  },
};
