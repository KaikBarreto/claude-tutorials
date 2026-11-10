// T26 · triggers de crm_opportunities (CRM/Kanban do tenant; lógica em lib/crm.mjs, molde das migrations do commit de release):
//  BEFORE UPDATE OF stage_id  crm_guard_stage_advance_trigger: a etapa de ORIGEM barra a troca com as pendências (P0001);
//  AFTER INSERT / UPDATE      crm_opportunities_log_stage_change (histórico) e crm_trigger_stage_automations ("Ao entrar nesta
//                             etapa": ao nascer nela, ao mudar de funil ou ao avançar para uma etapa de posição maior);
//  AFTER UPDATE OF checklists crm_sync_checklist_tasks (tarefa ligada ao checklist e os gatilhos de checklist concluído).
// Ação de automação que falha desfaz a operação inteira, como a transação do banco.
import { assertEtapaPronta, registraTrocaDeEtapa, registraStatusDaTarefa, rodaAutomacoes, chaveEvento, posicaoEtapa, isoAgora } from '../lib/crm.mjs';

const antes = new Map(); // id -> cópia da linha antes do UPDATE em curso
const completo = (c) => Array.isArray(c?.items) && c.items.length > 0 && c.items.every((i) => i.done);

export default {
  beforeInsert(row, hc) {
    if (row.created_by == null) row.created_by = hc.userId || null; // DEFAULT auth.uid()
    if (!Array.isArray(row.label_ids)) row.label_ids = [];
    if (!Array.isArray(row.checklists)) row.checklists = [];
    if (row.probability == null) row.probability = 50;
    if (row.value == null) row.value = 0;
  },
  afterInsert(row, hc) {
    try {
      rodaAutomacoes(hc, row.id, 'stage_enter', chaveEvento('stage', row.id, row.stage_id));
    } catch (e) {
      const t = hc.store.table('crm_opportunities');
      t.rows = t.rows.filter((r) => r !== row);
      t.touch();
      throw e;
    }
  },
  beforeUpdate(row, patch, hc) {
    antes.set(row.id, JSON.parse(JSON.stringify(row)));
    if (patch.stage_id !== undefined && String(patch.stage_id) !== String(row.stage_id)) {
      try {
        assertEtapaPronta(hc.store, row);
      } catch (e) {
        antes.delete(row.id);
        throw e;
      }
    }
  },
  afterUpdate(row, hc) {
    const old = antes.get(row.id);
    antes.delete(row.id);
    if (!old) return;
    try {
      if (String(old.stage_id) !== String(row.stage_id)) {
        registraTrocaDeEtapa(hc, row, old.stage_id);
        if (String(old.pipeline_id) !== String(row.pipeline_id) || posicaoEtapa(hc.store, row.stage_id) > posicaoEtapa(hc.store, old.stage_id)) {
          rodaAutomacoes(hc, row.id, 'stage_enter', chaveEvento('stage', row.id, row.stage_id));
        }
      }
      if (JSON.stringify(old.checklists ?? []) !== JSON.stringify(row.checklists ?? [])) {
        for (const c of Array.isArray(row.checklists) ? row.checklists : []) {
          const antigo = (old.checklists || []).find((x) => x.id === c.id);
          const ok = completo(c);
          const tarefa = c.linked_task_id ? hc.store.rows('schedule_tasks').find((t) => t.id === c.linked_task_id && t.crm_opportunity_id === row.id) : null;
          const alvo = ok ? 'concluida' : 'pendente';
          if (tarefa && tarefa.status !== alvo) {
            const de = tarefa.status;
            Object.assign(tarefa, { status: alvo, updated_at: isoAgora() });
            hc.store.table('schedule_tasks').touch();
            registraStatusDaTarefa(hc, tarefa, de);
          }
          if (ok && !completo(antigo)) {
            rodaAutomacoes(hc, row.id, 'checklist_completed', chaveEvento('checklist', row.id, c.id), c.name);
            rodaAutomacoes(hc, row.id, 'all_completed', chaveEvento('all', row.id));
          }
        }
      }
    } catch (e) {
      for (const k of Object.keys(row)) if (!(k in old)) delete row[k];
      Object.assign(row, old);
      hc.store.table('crm_opportunities').touch();
      throw e;
    }
  },
};
