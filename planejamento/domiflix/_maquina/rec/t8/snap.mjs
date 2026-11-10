#!/usr/bin/env node
// Sementes do T8 a partir do estado real do fakebase (usa tools/snapshot-delta.mjs).
//   node rec/t8/snap.mjs base          reset + sementes de partida do T8 (cadeia de rec/t8/cadeia.json) -> .base-t8.json
//   node rec/t8/snap.mjs diff NN       compara o estado atual com a base e grava seeds-extra/t8/apos-capNN.json (acumulado)
// Rode `diff` logo depois de gravar o capítulo NN, na MESMA trava da gravação (o fakebase ainda tem o que o robô fez).
// A base é a instância do agente E (porta 54325); outro agente usa outra porta e outra base.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54325';
const BASE = JSON.parse(fs.readFileSync(path.join(HERE, 'cadeia.json'), 'utf8')).inicio;
const BASEFILE = path.join(HERE, '.base-t8.json');
const TABELAS = [
  'inventory', 'inventory_stock_levels', 'inventory_movements', 'stocks', 'stock_access', 'material_groups',
  'compras', 'compra_materiais', 'compra_cotacoes', 'compra_cotacao_precos', 'compra_ordens', 'compra_ordem_itens',
  'inventory_counts', 'inventory_count_stocks', 'inventory_count_items', 'nfe_imports', 'suppliers',
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
  console.log(`base do T8 gravada: ${Object.keys(out).length} tabelas (${BASE.join(' + ')})`);
} else if (cmd === 'diff') {
  if (!nn) throw new Error('uso: snap.mjs diff NN');
  const id = `t8/apos-cap${String(nn).padStart(2, '0')}`;
  const p = spawnSync('node', [TOOL, 'diff', BASEFILE, id, '--tabelas', TABELAS.join(',')], { stdio: 'inherit', env: { ...process.env, FAKE_URL: FAKE } });
  process.exit(p.status ?? 1);
} else {
  console.log('uso: snap.mjs base | snap.mjs diff NN');
}
