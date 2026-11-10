#!/usr/bin/env node
// Sementes do T15 a partir do estado real do fakebase (usa tools/snapshot-delta.mjs).
//   node rec/t15/snap.mjs base          reset + sementes de partida do T15 (cadeia de rec/t15/cadeia.json) -> .base-t15.json
//   node rec/t15/snap.mjs diff NN       compara o estado atual com a base e grava seeds-extra/t15/apos-capNN.json (acumulado)
// Rode `diff` logo depois de gravar o capítulo NN, na MESMA trava da gravação (o fakebase ainda tem o que o robô fez).
// A instância é a do T15 (porta 54336); FAKE_URL sobrescreve.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54336';
const CAD = JSON.parse(fs.readFileSync(path.join(HERE, 'cadeia.json'), 'utf8'));
const BASE = CAD.inicio;
const BASEFILE = path.join(HERE, '.base-t15.json');
// só o que o T15 cria ou altera ao vivo (o resto que mudar é avisado, não gravado)
const TABELAS = ['employees', 'employee_movements', 'financial_transactions', 'financial_categories', 'financial_accounts', 'time_settings', 'time_schedules', 'time_records', 'time_sheets', 'user_preferences'];
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
  console.log(`base do T15 gravada: ${Object.keys(out).length} tabelas (${BASE.join(' + ')})`);
} else if (cmd === 'diff') {
  if (!nn) throw new Error('uso: snap.mjs diff NN');
  const id = `t15/apos-cap${String(nn).replace(/^(\d)(b?)$/, '0$1$2')}`;
  const p = spawnSync('node', [TOOL, 'diff', BASEFILE, id, '--tabelas', TABELAS.join(',')], { stdio: 'inherit', env: { ...process.env, FAKE_URL: FAKE } });
  // Tabelas de ligação (sem coluna `id`) saem do diff como `_patch` com `match: { company_id }`: o patch casa TODAS as linhas da empresa e as
  // deixa iguais (corrompe o vínculo serviço/OS e serviço/equipamento de todas as OS). O T15 não altera linha existente dessas tabelas
  // (só cria linhas novas, que vão como inserção), então o `_patch` delas é descartado (04/11, 1.38.19).
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
