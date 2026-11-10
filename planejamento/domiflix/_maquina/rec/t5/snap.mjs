#!/usr/bin/env node
// Sementes do T5 a partir do estado real do fakebase (usa tools/snapshot-delta.mjs).
//   node rec/t5/snap.mjs base          reset + sementes de partida do T5 (cadeia de rec/t5/cadeia.json) -> .base-t5.json
//   node rec/t5/snap.mjs diff NN       compara o estado atual com a base e grava seeds-extra/t5/apos-capNN.json (acumulado)
// Rode `diff` logo depois de gravar o capítulo NN (o fakebase ainda tem o que o robô fez).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54322';
const BASE = JSON.parse(fs.readFileSync(path.join(HERE, 'cadeia.json'), 'utf8')).inicio;
const BASEFILE = path.join(HERE, '.base-t5.json');
const TABELAS = [
  'service_orders', 'service_order_assignees', 'service_order_service_types', 'service_order_equipment',
  'service_order_equipment_service_types', 'service_order_budget_items', 'service_ratings', 'service_rating_criteria',
  'teams', 'team_members', 'technician_locations', 'os_statuses', 'nps_settings', 'nps_criteria', 'user_preferences', 'customers',
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
  console.log(`base do T5 gravada: ${Object.keys(out).length} tabelas (${BASE.join(' + ')})`);
} else if (cmd === 'diff') {
  if (!nn) throw new Error('uso: snap.mjs diff NN');
  const id = `t5/apos-cap${String(nn).padStart(2, '0')}`;
  const p = spawnSync('node', [TOOL, 'diff', BASEFILE, id, '--tabelas', TABELAS.join(',')], { stdio: 'inherit', env: process.env });
  process.exit(p.status ?? 1);
} else {
  console.log('uso: snap.mjs base | snap.mjs diff NN');
}
