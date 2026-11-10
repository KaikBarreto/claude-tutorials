// T26 · CRM/Kanban do tenant no Supabase falso: o que o banco do EcoSistema faz nos triggers e funções do CRM
// (migrations do commit de release f37573ea0: 20260929180000, 20261002160000, 20261005234137, 20261008120000 e
// 20261106170000_crm_regras_automacoes.sql), em memória. Usado por hooks/crm_opportunities.mjs, hooks/schedule_tasks.mjs
// e handlers/rpc/{ensure_company_crm_default_pipeline,reorder_company_crm_opportunities}.mjs.
//  - trava de etapa (crm_guard_stage_advance -> crm_assert_stage_ready): toda troca de stage_id confere as regras da
//    etapa de ORIGEM; as pendências saem juntas numa frase, erro P0001 (hint STAGE_REQUIREMENTS_PENDING);
//  - automações "Ao entrar nesta etapa" (crm_trigger_stage_automations): ao nascer na etapa, ao mudar de funil ou ao ir
//    para uma etapa de posição MAIOR; ações em ordem (crm_run_automation_event), uma execução por evento;
//  - histórico (crm_opportunities_log_stage_change e schedule_tasks_log_crm_status_change) e a linha "system" da
//    automação (metadata automation_executed, sem texto: é o que o banco grava).
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { agoraMs, hojeBR, addDias } from './eco.mjs';

// Núcleo do Supabase falso (o processo é o rec/fakebase/server.mjs): o erro HTTP no formato do PostgREST e o `db` com os
// DEFAULTs do banco. Pelo caminho do servidor, e não por caminho relativo: o mundo pode morar fora de rec/ (FAKE_MUNDO).
const NUCLEO = path.dirname(process.argv[1] || '');
const nucleo = async (rel) => {
  try {
    return await import(pathToFileURL(path.join(NUCLEO, rel)).href);
  } catch {
    return {};
  }
};
const { HttpError } = await nucleo('core/mutate.mjs');
const { db } = await nucleo('core/db.mjs');

export const isoAgora = () => new Date(agoraMs()).toISOString();
const ROTULO_STATUS = { pendente: 'Pendente', em_andamento: 'Em andamento', concluida: 'Concluída', cancelada: 'Cancelada' };
const encerrada = (t) => t.status === 'concluida' || t.status === 'cancelada';
const lista = (v) => (Array.isArray(v) ? v : []);
const itensDe = (c) => lista(c && c.items);

/** RAISE EXCEPTION do banco: 400 + corpo do PostgREST (o app mostra `message` no toast). */
export function erroBanco(message, code = 'P0001', hint = null) {
  const body = { code, details: null, hint, message };
  if (HttpError) return new HttpError(400, body);
  const e = new Error(message);
  e.body = body;
  return e;
}

/** crm_expand_automation_text: {NOME} = título do cartão, {CLIENTE} = empresa do cartão. */
export const expandir = (texto, opp) =>
  String(texto ?? '')
    .split('{{NOME}}').join(opp.title || '').split('{NOME}').join(opp.title || '')
    .split('{{CLIENTE}}').join(opp.company_name || '').split('{CLIENTE}').join(opp.company_name || '');

/** crm_automation_due_date: hoje + dias corridos, ou dias úteis (segunda a sexta, menos `holidays`). */
export function prazo(config = {}) {
  const dias = Math.min(3650, Math.max(0, Number.isFinite(Number(config.dueDays)) ? Math.trunc(Number(config.dueDays)) : 1));
  let d = hojeBR();
  if ((config.dayMode || 'calendar') !== 'business') return addDias(d, dias);
  const feriados = new Set(lista(config.holidays).map(String));
  for (let n = 0; n < dias; ) {
    d = addDias(d, 1);
    const dow = new Date(`${d}T12:00:00Z`).getUTCDay();
    if (dow >= 1 && dow <= 5 && !feriados.has(d)) n++;
  }
  return d;
}

/** crm_stage_missing_requirements: o que falta para o cartão sair da etapa (a atual, salvo `stageId`). */
export function faltas(store, opp, stageId = null) {
  const etapa = store.rows('crm_stages').find((s) => s.id === (stageId || opp.stage_id) && s.company_id === opp.company_id);
  const req = (etapa && etapa.requirements && typeof etapa.requirements === 'object') ? etapa.requirements : {};
  const tarefas = store.rows('schedule_tasks').filter((t) => t.crm_opportunity_id === opp.id);
  const checklists = lista(opp.checklists);
  const out = [];
  if (req.tasks && tarefas.some((t) => !encerrada(t))) out.push('Conclua as tarefas pendentes.');
  if (req.checklists && checklists.some((c) => itensDe(c).some((i) => !i.done))) out.push('Conclua todos os itens dos checklists.');
  if (req.assignee && !opp.assigned_to) out.push('Defina um responsável.');
  if (req.dueDate && !opp.expected_close_date) out.push('Defina uma previsão de fechamento.');
  if (req.customer && !opp.customer_id && !opp.supplier_id && !String(opp.company_name || '').trim()) out.push('Vincule ou informe a empresa do cartão.');
  if (req.description && !String(opp.notes || '').trim()) out.push('Preencha as observações do cartão.');
  for (const nome of lista(req.taskNames)) {
    const com = tarefas.filter((t) => t.title === nome);
    if (!com.length || com.some((t) => t.status !== 'concluida')) out.push(`Conclua a tarefa: ${nome}.`);
  }
  for (const nome of lista(req.checklistNames)) {
    const com = checklists.filter((c) => c.name === nome);
    if (!com.length || com.some((c) => !itensDe(c).length || itensDe(c).some((i) => !i.done))) out.push(`Conclua o checklist: ${nome}.`);
  }
  for (const it of lista(req.checklistItems)) {
    const ok = checklists.some((c) => c.name === it.checklistName && itensDe(c).some((i) => i.text === it.text && i.done));
    if (!ok) out.push(`Conclua o item “${it.text}” de ${it.checklistName}.`);
  }
  return [...new Set(out)];
}

/** crm_assert_stage_ready: barra a troca de etapa com as pendências numa frase só. */
export function assertEtapaPronta(store, opp) {
  const f = faltas(store, opp);
  if (f.length) throw erroBanco(f.join(' '), 'P0001', 'STAGE_REQUIREMENTS_PENDING');
}

function atividade(hc, opp, body, metadata) {
  return db.insert('crm_opportunity_activities', {
    company_id: opp.company_id, opportunity_id: opp.id, user_id: hc.userId || null, kind: 'system', body,
    metadata, created_at: isoAgora(),
  }, { companyId: opp.company_id });
}

/** crm_opportunities_log_stage_change */
export function registraTrocaDeEtapa(hc, opp, deStageId) {
  const nome = (id) => hc.store.rows('crm_stages').find((s) => s.id === id)?.name ?? null;
  const de = nome(deStageId);
  const para = nome(opp.stage_id);
  atividade(hc, opp, `Etapa alterada de "${de ?? 'etapa removida'}" para "${para ?? 'etapa desconhecida'}".`, {
    event: 'stage_changed', from_stage_id: deStageId, to_stage_id: opp.stage_id, from_stage_name: de, to_stage_name: para,
  });
}

/** schedule_tasks_log_crm_status_change */
export function registraStatusDaTarefa(hc, tarefa, deStatus) {
  const opp = hc.store.rows('crm_opportunities').find((o) => o.id === tarefa.crm_opportunity_id);
  if (!opp) return;
  atividade(hc, opp, `Tarefa "${tarefa.title}" marcada como ${ROTULO_STATUS[tarefa.status] ?? (tarefa.status || 'sem status')}.`, {
    event: 'task_status_changed', task_id: tarefa.id, task_title: tarefa.title, from_status: deStatus, to_status: tarefa.status,
  });
}

/** crm_create_automation_task (com reentry "reuse": a tarefa que a regra já criou para o cartão volta, sem duplicar). */
function criaTarefa(hc, regra, opp, config, tituloPadrao) {
  const { store } = hc;
  if ((config.reentry || 'reuse') !== 'new') {
    const ja = store.rows('schedule_tasks').filter((t) => t.company_id === opp.company_id && t.crm_opportunity_id === opp.id && t.crm_automation_rule_id === regra.id)
      .sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)))[0];
    if (ja) return ja;
  }
  let resp = config.userId || (lista(config.assigneeIds)[0] ?? null) || null;
  if (resp && !store.rows('profiles').some((p) => p.id === resp && p.company_id === opp.company_id)) resp = null;
  const autor = hc.userId || opp.created_by || opp.assigned_to;
  if (!autor) throw erroBanco('Não foi possível identificar o autor da tarefa automática');
  const prio = ['baixa', 'media', 'alta', 'urgente'].includes(config.priority) ? config.priority : 'media';
  return db.insert('schedule_tasks', {
    company_id: opp.company_id, created_by: autor, assigned_to: resp || opp.assigned_to || null,
    title: expandir(String(config.title || '').trim() ? config.title : tituloPadrao, opp),
    description: expandir(config.description, opp) || null, category: 'crm', scheduled_date: prazo(config), status: 'pendente',
    priority: prio, crm_opportunity_id: opp.id, crm_automation_rule_id: regra.id, crm_checklist_id: config.checklistId || null,
    created_at: isoAgora(), updated_at: isoAgora(),
  }, { companyId: opp.company_id });
}

let evento = 0;
export const chaveEvento = (tipo, ...partes) => `${tipo}:${partes.join(':')}:${Date.now()}-${++evento}`;

/** crm_run_automation_event: regras ativas da etapa ATUAL do cartão para o gatilho, em ordem; cada uma roda uma vez por evento. */
export function rodaAutomacoes(hc, oppId, gatilho, chave, nomeConcluido = null) {
  const { store } = hc;
  const opp = store.rows('crm_opportunities').find((o) => o.id === oppId);
  if (!opp) return 0;
  if (gatilho === 'all_completed') {
    const tarefaAberta = store.rows('schedule_tasks').some((t) => t.crm_opportunity_id === opp.id && !encerrada(t));
    const itemAberto = lista(opp.checklists).some((c) => itensDe(c).some((i) => !i.done));
    if (tarefaAberta || itemAberto) return 0;
  }
  const regras = store.rows('crm_automation_rules')
    .filter((r) => r.company_id === opp.company_id && r.pipeline_id === opp.pipeline_id && r.trigger_stage_id === opp.stage_id && r.trigger_type === gatilho && r.enabled)
    .sort((a, b) => (a.position ?? 0) - (b.position ?? 0) || String(a.created_at).localeCompare(String(b.created_at)) || String(a.id).localeCompare(String(b.id)));
  let feitas = 0;
  for (const regra of regras) {
    const cfg = regra.trigger_config || {};
    if (gatilho === 'task_completed' && String(cfg.taskName || '').trim() && expandir(cfg.taskName, opp) !== nomeConcluido) continue;
    if (gatilho === 'checklist_completed' && String(cfg.name || '').trim() && expandir(cfg.name, opp) !== nomeConcluido) continue;
    const ja = store.rows('crm_automation_executions').some((e) => e.rule_id === regra.id && e.opportunity_id === opp.id && e.event_key === chave);
    if (ja) continue;
    const exec = db.insert('crm_automation_executions', { company_id: opp.company_id, rule_id: regra.id, opportunity_id: opp.id, event_key: String(chave).slice(0, 300), status: 'running', created_at: isoAgora() }, { companyId: opp.company_id });
    try {
      for (const acao of lista(regra.actions)) {
        const c = acao.config || {};
        switch (acao.action) {
          case 'create_task':
            criaTarefa(hc, regra, opp, c, `Acompanhar ${opp.title}`);
            break;
          case 'set_due':
            opp.expected_close_date = prazo(c);
            break;
          case 'assign_user':
            if (!c.userId || !store.rows('profiles').some((p) => p.id === c.userId && p.company_id === opp.company_id)) throw erroBanco('Responsável da automação não pertence à empresa');
            opp.assigned_to = c.userId;
            break;
          case 'add_label':
            if (!c.labelId || !store.rows('crm_labels').some((l) => l.id === c.labelId && l.company_id === opp.company_id)) throw erroBanco('Etiqueta da automação não pertence à empresa');
            if (!lista(opp.label_ids).includes(c.labelId)) opp.label_ids = [...lista(opp.label_ids), c.labelId];
            break;
          case 'apply_checklist': {
            const existe = lista(opp.checklists).some((x) => x.automation_rule_id === regra.id);
            if (existe && (c.reentry || 'reuse') !== 'new') break;
            const modelo = c.templateId ? store.rows('crm_checklist_templates').find((t) => t.id === c.templateId && t.company_id === opp.company_id) : null;
            const itens = modelo ? lista(modelo.items) : lista(c.items);
            if (!itens.length) throw erroBanco('Checklist automático precisa ter itens');
            const id = randomUUID();
            const nome = expandir(String(c.name || '').trim() ? c.name : 'Checklist', opp);
            let tarefa = null;
            if (c.createTask) tarefa = criaTarefa(hc, regra, opp, { ...c, title: nome, checklistId: id }, nome);
            opp.checklists = [...lista(opp.checklists), {
              id, name: nome, automation_rule_id: regra.id, linked_task_id: tarefa ? tarefa.id : null,
              items: itens.map((it, k) => ({ id: `${id}-${k}`, text: expandir(typeof it === 'string' ? it : it.text, opp), done: false })),
            }];
            break;
          }
          default:
            // move_card e copy_card: a aula não usa; o falso não simula (a ação falha como no banco quando não acha o destino)
            throw erroBanco('Destino da automação indisponível');
        }
      }
      store.table('crm_opportunities').touch();
      Object.assign(exec, { status: 'completed', executed_at: isoAgora() });
      atividade(hc, opp, null, { event: 'automation_executed', rule_id: regra.id, rule_name: regra.name });
      feitas++;
    } catch (e) {
      Object.assign(exec, { status: 'failed', error_message: String(e.message || e).slice(0, 500), executed_at: isoAgora() });
      throw e;
    }
  }
  return feitas;
}

/** Posição de uma etapa (para "avançar": posição maior). */
export const posicaoEtapa = (store, id) => store.rows('crm_stages').find((s) => s.id === id)?.position ?? 0;

/** ensure_company_crm_default_pipeline: o "Funil de vendas" padrão com as cinco etapas, se a empresa não tem funil padrão. */
export function garanteFunilPadrao(companyId) {
  const padrao = db.rows('crm_pipelines').find((p) => p.company_id === companyId && p.is_default);
  if (padrao) return padrao.id;
  const agora = isoAgora();
  const funil = db.insert('crm_pipelines', { company_id: companyId, name: 'Funil de vendas', color: '#22c55e', position: 0, is_default: true, created_at: agora, updated_at: agora }, { companyId });
  const etapas = [['Novo', '#3b82f6', 0, false, false], ['Em contato', '#f59e0b', 1, false, false], ['Proposta', '#8b5cf6', 2, false, false], ['Ganho', '#22c55e', 3, true, false], ['Perdido', '#ef4444', 4, false, true]];
  for (const [name, color, position, is_won, is_lost] of etapas) {
    db.insert('crm_stages', { company_id: companyId, pipeline_id: funil.id, name, color, position, is_won, is_lost, created_at: agora, updated_at: agora }, { companyId });
  }
  return funil.id;
}
