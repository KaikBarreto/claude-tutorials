#!/usr/bin/env node
// Sementes do T4 a partir do estado real do fakebase (usa tools/snapshot-delta.mjs).
//   node rec/t4/snap.mjs base          reset + sementes de partida do T4 (t3/apos-cap10, t1/apos-cap13, t4/inicio) -> .base-t4.json
//   node rec/t4/snap.mjs diff NN       compara o estado atual com a base e grava seeds-extra/t4/apos-capNN.json (acumulado)
// Rode `diff` logo depois de gravar o capítulo NN (o fakebase ainda tem o que o robô fez).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54321';
const BASE = ['t3/apos-cap10', 't1/apos-cap13', 't4/inicio'];
const BASEFILE = path.join(HERE, '.base-t4.json');
const TABELAS = ['service_type_categories', 'service_types', 'task_types', 'form_templates', 'form_questions', 'form_template_service_types'];
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
  console.log(`base do T4 gravada: ${Object.keys(out).length} tabelas (${BASE.join(' + ')})`);
} else if (cmd === 'diff') {
  if (!nn) throw new Error('uso: snap.mjs diff NN');
  const id = `t4/novo-cap${String(nn).padStart(2, '0')}`;
  const p = spawnSync('node', [TOOL, 'diff', BASEFILE, id, '--tabelas', TABELAS.join(',')], { stdio: 'inherit', env: process.env });
  process.exit(p.status ?? 1);
} else {
  console.log('uso: snap.mjs base | snap.mjs diff NN');
}
