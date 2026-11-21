#!/usr/bin/env node
// T26 · refaz a cadeia de sementes dos capítulos 8 a 14 (app 1.60.22, aplicação de 21/11) SEM navegador: parte do apos-cap07 (que já
// existe: funil Sucata industrial, regras, automação "Agendar a visita", checklist e etiqueta) e repete, pelo REST do Supabase falso
// (os mesmos inserts e updates que a tela faz; os gatilhos do mundo, em hooks/crm_opportunities.mjs, fazem o resto), cada capítulo,
// gravando seeds-extra/t26/apos-capNN.json depois de cada um. Assim os capítulos não dependem da ordem do ensaio.
//   FAKE_URL=http://127.0.0.1:54326 TUT_SENHA=<8+ caracteres> node rec/t26/aux/t26_cadeia.mjs
// Cadeia: apos-cap07 -> apos-cap08 (automação "Preparar a proposta") -> apos-cap09 (Nova oportunidade, com telefone) -> apos-cap10 (cartão em
// "Em contato") -> apos-cap11 (ficha: Rafael, etiqueta, tarefa concluída, cartão em "Visita técnica") -> apos-cap12 (checklist todo marcado)
// -> apos-cap13 (80%, Telefone, comentário, tarefa "Ligar pro Paulo") -> apos-cap14 (tarefa "Enviar proposta" em andamento).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const FAKE = process.env.FAKE_URL;
if (!FAKE) throw new Error('defina FAKE_URL');
const SENHA = process.env.TUT_SENHA;
if (!SENHA || SENHA.length < 8) throw new Error('defina TUT_SENHA (8+ caracteres, só no ambiente)');
const here = path.dirname(fileURLToPath(import.meta.url));
const SX = path.resolve(here, '../../mundo/seeds-extra/t26');
const mundo = JSON.parse(fs.readFileSync(path.resolve(here, '../../mundo/mundo.json')));
const ANON = mundo.env.anonKey;
const RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908';
const CHAPARIA = 'a56865ab-8af5-53ee-a1d7-00c2536f0463';

await fetch(`${FAKE}/__dev/reset`, { method: 'POST' });
let r = await fetch(`${FAKE}/__dev/seed`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ files: ['t26/apos-cap07'] }) });
if (!r.ok) throw new Error('seed: ' + (await r.text()));
const tok = (await (await fetch(`${FAKE}/auth/v1/token?grant_type=password`, { method: 'POST', headers: { apikey: ANON, 'content-type': 'application/json' }, body: JSON.stringify({ email: 'rafael@reciclavalemetais.example', password: SENHA }) })).json()).access_token;
const H = { apikey: ANON, Authorization: `Bearer ${tok}`, 'content-type': 'application/json', Prefer: 'return=representation' };
const rest = async (m, p, b) => {
  const x = await fetch(`${FAKE}/rest/v1/${p}`, { method: m, headers: H, body: b ? JSON.stringify(b) : undefined });
  const t = await x.text();
  if (!x.ok) throw new Error(`${m} ${p}: ${x.status} ${t}`);
  return t ? JSON.parse(t) : null;
};
const estado = async (t) => (await fetch(`${FAKE}/__dev/state?table=${t}`)).json();
const TABELAS = ['crm_pipelines', 'crm_stages', 'crm_opportunities', 'crm_automation_rules', 'crm_automation_executions', 'crm_checklist_templates', 'crm_labels', 'crm_opportunity_activities'];
async function grava(nome, doc) {
  const out = { _doc: `T26 · estado do CRM no fim do capítulo (${nome}), gerado por rec/t26/aux/t26_cadeia.mjs: ${doc}` };
  for (const t of TABELAS) out[t] = await estado(t);
  out.schedule_tasks = (await estado('schedule_tasks')).filter((x) => x.crm_opportunity_id);
  fs.writeFileSync(path.join(SX, `${nome}.json`), JSON.stringify(out, null, 1));
  console.log(`${nome}: ` + Object.entries(out).filter(([k]) => !k.startsWith('_')).map(([k, v]) => `${k} ${v.length}`).join(', '));
}

const [suc] = await rest('GET', 'crm_pipelines?select=*&name=eq.Sucata%20industrial');
const cid = suc.company_id;
const etapas = Object.fromEntries((await rest('GET', `crm_stages?select=*&pipeline_id=eq.${suc.id}`)).map((s) => [s.name, s]));
const [modelo] = await rest('GET', 'crm_checklist_templates?select=*&name=eq.Documentos%20do%20fornecedor');
const [etiqueta] = await rest('GET', 'crm_labels?select=*&name=eq.Ind%C3%BAstria');

// ---- cap08: automação "Preparar a proposta" na Visita técnica (Aplicar checklist + Definir prazo do cartão)
await rest('POST', 'crm_automation_rules', {
  company_id: cid, pipeline_id: suc.id, trigger_stage_id: etapas['Visita técnica'].id, name: 'Preparar a proposta', trigger_type: 'stage_enter', trigger_config: {},
  actions: [
    { action: 'apply_checklist', config: { templateId: modelo.id, name: 'Documentos da {CLIENTE}', createTask: true, reentry: 'reuse' } },
    { action: 'set_due', config: { dueDays: 15, dayMode: 'calendar' } },
  ],
  enabled: true, position: 0,
});
await grava('apos-cap08', 'apos-cap07 + a automação "Preparar a proposta" (Visita técnica: Aplicar checklist e Definir prazo do cartão, 15 dias corridos)');

// ---- cap09: Nova oportunidade (Retalho de chapa da Metalúrgica Jequitibá, com telefone)
const [opp] = await rest('POST', 'crm_opportunities', {
  company_id: cid, pipeline_id: suc.id, stage_id: etapas['Novo'].id, title: 'Retalho de chapa da Metalúrgica Jequitibá', contact_name: 'Paulo Lacerda',
  contact_email: 'paulo.lacerda@metalurgicajequitiba.example', contact_phone: '(12) 90000-4120', value: 8400, notes: 'Quer retirada a cada quinze dias, com caçamba.',
  expected_close_date: '2026-11-30', assigned_to: null, customer_id: null, supplier_id: null, company_name: 'Metalúrgica Jequitibá', contact_role: 'Suprimentos',
  material_id: CHAPARIA, material_name: 'Chaparia', estimated_quantity: 12000, estimated_unit: 'Kg', transport_mode: 'Frota própria', start_date: null,
});
await grava('apos-cap09', 'apos-cap08 + a oportunidade da Jequitibá em Novo (telefone preenchido)');

// ---- cap10: arrasta para "Em contato" (a automação "Agendar a visita" cria a tarefa; a trava barra a ida à Visita técnica, sem efeito)
await rest('PATCH', `crm_opportunities?id=eq.${opp.id}`, { stage_id: etapas['Em contato'].id });
await rest('POST', 'rpc/reorder_company_crm_opportunities', { p_stage_id: etapas['Em contato'].id, p_ordered_ids: [opp.id] });
await rest('POST', 'rpc/reorder_company_crm_opportunities', { p_stage_id: etapas['Novo'].id, p_ordered_ids: [] });
await grava('apos-cap10', 'apos-cap09 + o cartão em Em contato com a tarefa "Agendar visita na Metalúrgica Jequitibá" (a ida à Visita técnica foi barrada)');

// ---- cap11: ficha (Rafael responsável, etiqueta Indústria, tarefa concluída) e o cartão passa para a Visita técnica (automação nova roda)
await rest('PATCH', `crm_opportunities?id=eq.${opp.id}`, { assigned_to: RAFAEL });
await rest('PATCH', `crm_opportunities?id=eq.${opp.id}`, { label_ids: [etiqueta.id] });
const [tarefa] = await rest('GET', `schedule_tasks?select=*&crm_opportunity_id=eq.${opp.id}`);
await rest('PATCH', `schedule_tasks?id=eq.${tarefa.id}`, { status: 'concluida' });
await rest('PATCH', `crm_opportunities?id=eq.${opp.id}`, { stage_id: etapas['Visita técnica'].id });
await rest('POST', 'rpc/reorder_company_crm_opportunities', { p_stage_id: etapas['Visita técnica'].id, p_ordered_ids: [opp.id] });
await rest('POST', 'rpc/reorder_company_crm_opportunities', { p_stage_id: etapas['Em contato'].id, p_ordered_ids: [] });
await grava('apos-cap11', 'apos-cap10 + Rafael responsável, etiqueta Indústria, tarefa da visita concluída, cartão em Visita técnica com o checklist "Documentos da Metalúrgica Jequitibá" 0/3, a tarefa vinculada e a previsão 25/11');

// ---- cap12: o checklist inteiro marcado (a tarefa vinculada conclui sozinha); o modelo aplicado a mais é removido no mesmo capítulo
const [atual] = await rest('GET', `crm_opportunities?select=*&id=eq.${opp.id}`);
const marcados = atual.checklists.map((c) => ({ ...c, items: c.items.map((i) => ({ ...i, done: true })) }));
await rest('PATCH', `crm_opportunities?id=eq.${opp.id}`, { checklists: marcados });
await grava('apos-cap12', 'apos-cap11 + checklist 3/3 e a tarefa vinculada concluída');

// ---- cap13: probabilidade 80, origem Telefone, comentário, tarefa "Ligar pro Paulo" (13/11)
await rest('PATCH', `crm_opportunities?id=eq.${opp.id}`, { probability: 80 });
await rest('PATCH', `crm_opportunities?id=eq.${opp.id}`, { source: 'Telefone' });
await rest('POST', 'crm_opportunity_activities', { company_id: cid, opportunity_id: opp.id, user_id: RAFAEL, kind: 'comment', body: 'Paulo pediu a proposta até sexta.' });
await rest('POST', 'schedule_tasks', { title: 'Ligar pro Paulo', crm_opportunity_id: opp.id, scheduled_date: '2026-11-13', priority: 'media', notify_on_day: true, notify_push: false, category: 'crm', company_id: cid, created_by: RAFAEL });
await grava('apos-cap13', 'apos-cap12 + probabilidade 80, origem Telefone, o comentário e a tarefa "Ligar pro Paulo" (13/11)');

// ---- cap14: tarefa "Enviar proposta" (12/11, Rafael, alta), arrastada para Em andamento
const [prop] = await rest('POST', 'schedule_tasks', { title: 'Enviar proposta', crm_opportunity_id: opp.id, assigned_to: RAFAEL, scheduled_date: '2026-11-12', priority: 'alta', notify_on_day: true, notify_push: false, category: 'crm', company_id: cid, created_by: RAFAEL });
await rest('PATCH', `schedule_tasks?id=eq.${prop.id}`, { status: 'em_andamento' });
await grava('apos-cap14', 'apos-cap13 + a tarefa "Enviar proposta" (12/11, Rafael, alta) em andamento');
