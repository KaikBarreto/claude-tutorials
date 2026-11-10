#!/usr/bin/env node
// Sementes do T14 a partir do estado real do fakebase (usa tools/snapshot-delta.mjs).
//   node rec/t14/snap.mjs base          reset + sementes de partida do T14 (cadeia de rec/t14/cadeia.json) -> .base-t14-HHMM.json
//   node rec/t14/snap.mjs diff NN       compara o estado atual com a base e grava seeds-extra/t14/apos-capNN.json (acumulado)
// Rode `diff` logo depois de gravar o capítulo NN, na MESMA trava da gravação (o fakebase ainda tem o que o robô fez).
// UMA BASE POR FAKE_NOW (15:10 para os caps 0 a 11, 16:20 para o 12 e o 13): as sementes têm instantes relativos ("@now-30d"), e uma base
// de outro relógio faria TODA linha parecer alterada (o diff só tolera 30 min). O rodar.sh grava a base do relógio do capítulo ANTES de gravar.
// A instância é a do T14 (porta 54341); FAKE_URL sobrescreve.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54341';
const CAD = JSON.parse(fs.readFileSync(path.join(HERE, 'cadeia.json'), 'utf8'));
const BASE = CAD.inicio;
const RELOGIO = (process.env.FAKE_NOW || CAD.fake_now).slice(11, 16).replace(':', '');   // "1510" ou "1620"
const BASEFILE = path.join(HERE, `.base-t14-${RELOGIO}.json`);
// só o que o T14 cria ou altera ao vivo (o resto que mudar é avisado, não gravado)
const TABELAS = [
  'company_settings', 'company_fiscal_settings', 'fiscal_certificate_audit', 'consent_records', 'service_types',
  'nfse_emissions', 'nfse_events', 'nfse_auto_jobs', 'contracts',
  'inbound_nfe', 'inbound_nfse', 'dfe_sync_state', 'dfe_manifestacao_jobs', 'financial_transactions',
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
  fs.writeFileSync(BASEFILE, JSON.stringify({ ...out, __cadeia: { inicio: BASE, fake_now: process.env.FAKE_NOW || CAD.fake_now } }));
  console.log(`base do T14 (${RELOGIO}) gravada: ${Object.keys(out).length} tabelas (${BASE.join(' + ')})`);
} else if (cmd === 'diff') {
  if (!nn) throw new Error('uso: snap.mjs diff NN');
  if (!fs.existsSync(BASEFILE)) throw new Error(`sem a base ${path.basename(BASEFILE)}: rode "node rec/t14/snap.mjs base" (com o FAKE_NOW do capítulo) antes de gravar`);
  const id = `t14/apos-cap${String(nn).padStart(2, '0')}`;
  const p = spawnSync('node', [TOOL, 'diff', BASEFILE, id, '--tabelas', TABELAS.join(',')], { stdio: 'inherit', env: { ...process.env, FAKE_URL: FAKE } });
  process.exit(p.status ?? 1);
} else if (cmd === 'base-ok') {
  // a base existe e é da cadeia atual? (sai 0 se sim; o rodar.sh refaz a base quando não)
  try {
    const b = JSON.parse(fs.readFileSync(BASEFILE, 'utf8'));
    process.exit(JSON.stringify(b.__cadeia?.inicio) === JSON.stringify(BASE) ? 0 : 1);
  } catch {
    process.exit(1);
  }
} else {
  console.log('uso: snap.mjs base | snap.mjs diff NN | snap.mjs base-ok');
}
