#!/usr/bin/env node
// Gera os "seeds extras" por capitulo (rec/fakebase/seeds-extra/<nome>.json) a partir do estado real do fakebase.
//
// Fluxo (cada capitulo regravavel sozinho: o roteiro dele carrega o estado que os anteriores deixaram, via `seedExtra`):
//   1. node rec/fakebase/tools/snapshot-delta.mjs base <base.json>
//        zera o fakebase (POST /__dev/reset, SEM extras) e guarda o estado de todas as tabelas como linha de base.
//   2. grave o capitulo N (com `--no-reset` se encadeando os capitulos na mesma sessao do fakebase).
//   3. node rec/fakebase/tools/snapshot-delta.mjs diff <base.json> t3/apos-capNN
//        compara o estado atual com a base e grava seeds-extra/t3/apos-capNN.json: linhas novas (tabela -> [linhas])
//        e linhas alteradas (_patch: { match:{id}, set:{campos} }). O arquivo e ACUMULADO (tudo o que mudou desde a base).
//   O roteiro do capitulo N+1 usa "seedExtra": ["t3/apos-capNN"].
// Instantes ISO recentes viram "@now-Nm" (relativos a hora em que o seed for aplicado); o resto fica literal.
// Opcao `--tabelas a,b,c` restringe as tabelas gravadas (padrao: as do T3); as demais que mudaram sao so avisadas.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54321';
const EXTRA_DIR = path.resolve(HERE, '../seeds-extra');
const T3_TABLES = [
  'customers', 'customer_portals', 'customer_contacts', 'customer_origins', 'lead_capture_forms', 'suppliers',
  'equipment', 'equipment_categories', 'equipment_field_config', 'equipment_number_counters', 'equipment_attachments', 'equipment_tasks',
];

const [cmd, a1, a2, ...rest] = process.argv.slice(2);
const flag = (n) => { const i = rest.indexOf(n); return i >= 0 ? rest[i + 1] : null; };
const get = async (u) => (await fetch(FAKE + u)).json();

async function dumpAll() {
  const counts = await get('/__dev/state');
  const out = {};
  for (const t of Object.keys(counts)) out[t] = await get(`/__dev/state?table=${encodeURIComponent(t)}`);
  return out;
}

const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$/;
function relTime(v, nowMs) {
  if (typeof v !== 'string' || !ISO.test(v)) return v;
  const diffMin = Math.round((nowMs - Date.parse(v)) / 60000);
  if (diffMin < 0 || diffMin > 360) return v; // so instantes recentes (criados durante a gravacao)
  return `@now-${diffMin}m`;
}
// os seeds usam "@now-300d" & cia: a cada reset o instante muda alguns segundos; isso nao e alteracao feita pelo capitulo
const sameValue = (a, b) => {
  if (typeof a === 'string' && typeof b === 'string' && ISO.test(a) && ISO.test(b)) return Math.abs(Date.parse(a) - Date.parse(b)) < 30 * 60 * 1000;
  return JSON.stringify(a) === JSON.stringify(b);
};
const rel = (row, nowMs) => Object.fromEntries(Object.entries(row).map(([k, v]) => [k, relTime(v, nowMs)]));

if (cmd === 'base') {
  if (!a1) throw new Error('uso: snapshot-delta.mjs base <base.json>');
  await fetch(FAKE + '/__dev/reset', { method: 'POST' });
  const all = await dumpAll();
  fs.mkdirSync(path.dirname(path.resolve(a1)), { recursive: true });
  fs.writeFileSync(a1, JSON.stringify(all));
  console.log(`base gravada em ${a1}: ${Object.keys(all).length} tabelas`);
} else if (cmd === 'diff') {
  if (!a1 || !a2) throw new Error('uso: snapshot-delta.mjs diff <base.json> <t3/apos-capNN> [--tabelas a,b]');
  const base = JSON.parse(fs.readFileSync(a1, 'utf8'));
  const now = await dumpAll();
  const allowed = new Set((flag('--tabelas') || T3_TABLES.join(',')).split(',').map((s) => s.trim()).filter(Boolean));
  const nowMs = Date.now();
  const out = {};
  const patch = {};
  const ignored = [];
  const keyOf = (r) => r.id ?? JSON.stringify([r.company_id, r.field_key, r.module_code]);
  for (const [table, rows] of Object.entries(now)) {
    const was = new Map((base[table] || []).map((r) => [keyOf(r), r]));
    const added = [];
    const changed = [];
    for (const r of rows) {
      const b = was.get(keyOf(r));
      if (!b) { added.push(rel(r, nowMs)); continue; }
      const set = {};
      for (const [k, v] of Object.entries(r)) if (!sameValue(v, b[k])) set[k] = relTime(v, nowMs);
      if (Object.keys(set).length) changed.push({ match: r.id !== undefined ? { id: r.id } : { company_id: r.company_id, field_key: r.field_key }, set });
    }
    const removed = [...was.keys()].filter((k) => !rows.some((r) => keyOf(r) === k));
    if (!added.length && !changed.length && !removed.length) continue;
    if (!allowed.has(table)) { ignored.push(`${table} (+${added.length} ~${changed.length} -${removed.length})`); continue; }
    if (removed.length) console.warn(`AVISO: ${table} perdeu ${removed.length} linha(s); o seed extra nao remove linhas`);
    if (added.length) out[table] = added;
    if (changed.length) patch[table] = changed;
  }
  if (Object.keys(patch).length) out._patch = patch;
  const file = path.resolve(EXTRA_DIR, `${a2.replace(/\.json$/, '')}.json`);
  if (!file.startsWith(EXTRA_DIR + path.sep)) throw new Error('destino fora de seeds-extra');
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(out, null, 1));
  const resumo = Object.entries(out).map(([t, v]) => (t === '_patch' ? `_patch(${Object.entries(v).map(([k, x]) => k + ':' + x.length).join(',')})` : `${t}:+${v.length}`));
  console.log(`gravado ${path.relative(path.resolve(HERE, '../../..'), file)}  ${resumo.join('  ')}`);
  if (ignored.length) console.log('tabelas que tambem mudaram e ficaram de fora:', ignored.join(', '));
} else {
  console.log('uso: snapshot-delta.mjs base <base.json> | diff <base.json> <t3/apos-capNN> [--tabelas a,b]');
  process.exit(2);
}
