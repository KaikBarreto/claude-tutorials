#!/usr/bin/env node
// Sementes do T11 a partir do estado real do fakebase (usa tools/snapshot-delta.mjs).
//   node rec/t11/snap.mjs base          reset + sementes de partida do T11 (cadeia de rec/t11/cadeia.json) -> .base-t11.json
//   node rec/t11/snap.mjs diff NN       compara o estado atual com a base e grava seeds-extra/t11/apos-capNN.json (acumulado)
// Rode `diff` logo depois de gravar o capítulo NN, na MESMA trava da gravação (o fakebase ainda tem o que o robô fez).
// A instância é a do agente do T11 (porta 54329); FAKE_URL sobrescreve.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54329';
const CAD = JSON.parse(fs.readFileSync(path.join(HERE, 'cadeia.json'), 'utf8'));
const BASE = CAD.inicio;
const BASEFILE = path.join(HERE, '.base-t11.json');
// só o que o T11 cria ou altera ao vivo (o resto que mudar é avisado, não gravado)
const TABELAS = [
  'responsible_technicians', 'contracts', 'contract_items', 'contract_environments', 'contract_plan_activities',
  'service_orders', 'service_order_service_types', 'service_order_equipment', 'service_order_equipment_service_types',
  'service_order_assignees', 'service_order_activities', 'financial_transactions', 'pmoc_documents',
  'form_templates', 'form_questions', 'user_notifications',
];
const TOOL = path.resolve(HERE, '../fakebase/tools/snapshot-delta.mjs');
const get = async (u) => (await fetch(FAKE + u)).json();

const [cmd, nn] = process.argv.slice(2);
if (cmd === 'base') {
  await fetch(FAKE + '/__dev/reset', { method: 'POST' });
  const r = await fetch(FAKE + '/__dev/seed', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ files: BASE }) });
  if (!r.ok) throw new Error('seed: ' + (await r.text()));
  const counts = await get('/__dev/state');
  const out = {};
  for (const t of Object.keys(counts)) out[t] = await get(`/__dev/state?table=${encodeURIComponent(t)}`);
  fs.writeFileSync(BASEFILE, JSON.stringify(out));
  console.log(`base do T11 gravada: ${Object.keys(out).length} tabelas (${BASE.join(' + ')})`);
} else if (cmd === 'diff') {
  if (!nn) throw new Error('uso: snap.mjs diff NN');
  const id = `t11/apos-cap${String(nn).padStart(2, '0')}`;
  const p = spawnSync('node', [TOOL, 'diff', BASEFILE, id, '--tabelas', TABELAS.join(',')], { stdio: 'inherit', env: { ...process.env, FAKE_URL: FAKE } });
  // Tabelas de ligação (sem coluna `id`) saem do diff como `_patch` com `match: { company_id }`: o patch casa TODAS as linhas da empresa e as
  // deixa iguais (corrompe o vínculo serviço/OS e serviço/equipamento de todas as OS). O T11 não altera linha existente dessas tabelas
  // (só cria linhas novas, que vão como inserção), então o `_patch` delas é descartado.
  const arq = path.resolve(HERE, '../fakebase/seeds-extra', id + '.json');
  if (p.status === 0 && fs.existsSync(arq)) {
    const d = JSON.parse(fs.readFileSync(arq, 'utf8'));
    const solto = [];
    for (const t of ['service_order_service_types', 'service_order_equipment_service_types']) {
      if (d._patch?.[t]) { solto.push(`${t}:${d._patch[t].length}`); delete d._patch[t]; }
    }
    if (d._patch && !Object.keys(d._patch).length) delete d._patch;
    fs.writeFileSync(arq, JSON.stringify(d, null, 1));
    if (solto.length) console.log('descartei _patch de tabelas de ligação (sem id):', solto.join(' '));
  }
  process.exit(p.status ?? 1);
} else {
  console.log('uso: snap.mjs base | snap.mjs diff NN');
}
