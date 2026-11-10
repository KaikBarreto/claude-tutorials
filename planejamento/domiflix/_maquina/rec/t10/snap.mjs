#!/usr/bin/env node
// Sementes do T10 a partir do estado real do fakebase (usa tools/snapshot-delta.mjs).
//   node rec/t10/snap.mjs base          reset + sementes de partida do T10 (cadeia de rec/t10/cadeia.json) -> .base-t10.json
//   node rec/t10/snap.mjs diff NN       compara o estado atual com a base e grava seeds-extra/t10/apos-capNN.json (acumulado)
// Rode `diff` logo depois de gravar o capítulo NN, na MESMA trava da gravação (o fakebase ainda tem o que o robô fez).
// A instância é a do T10 (porta 54328); FAKE_URL sobrescreve.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54328';
const CAD = JSON.parse(fs.readFileSync(path.join(HERE, 'cadeia.json'), 'utf8'));
const BASE = CAD.inicio;
const BASEFILE = path.join(HERE, '.base-t10.json');
// só o que o T10 cria ou altera ao vivo (o resto que mudar é avisado, não gravado)
const TABELAS = [
  'crm_pipelines', 'crm_stages', 'leads', 'lead_assignees', 'lead_interactions', 'crm_webhooks', 'crm_labels', 'crm_checklist_templates',
  'crm_pipeline_access', 'projects',
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
  console.log(`base do T10 gravada: ${Object.keys(out).length} tabelas (${BASE.join(' + ')})`);
} else if (cmd === 'diff') {
  if (!nn) throw new Error('uso: snap.mjs diff NN');
  const id = `t10/apos-cap${String(nn).padStart(2, '0')}`;
  const p = spawnSync('node', [TOOL, 'diff', BASEFILE, id, '--tabelas', TABELAS.join(',')], { stdio: 'inherit', env: { ...process.env, FAKE_URL: FAKE } });
  process.exit(p.status ?? 1);
} else {
  console.log('uso: snap.mjs base | snap.mjs diff NN');
}
