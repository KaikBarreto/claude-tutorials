#!/usr/bin/env node
// Mostra as colunas de uma ou mais tabelas (do types.ts): node rec/fakebase/tools/cols.mjs customers service_orders
//   * = obrigatoria no insert (sem default e nao-nula);  ? = aceita null;  d = tem default no banco
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const schema = JSON.parse(fs.readFileSync(path.join(here, '../schema.json'), 'utf8'));
const names = process.argv.slice(2);
if (!names.length) {
  console.log(Object.keys(schema.tables).sort().join('\n'));
  process.exit(0);
}
for (const n of names) {
  const t = schema.tables[n] || schema.views?.[n];
  if (!t) {
    console.log(`${n}: nao existe no schema`);
    continue;
  }
  console.log(`== ${n} ==`);
  const cols = t.columns || t.cols || t;
  for (const [c, d] of Object.entries(cols)) {
    const flags = `${!d.n && !d.o ? '*' : ' '}${d.n ? '?' : ' '}${d.o ? 'd' : ' '}`;
    console.log(`  ${flags} ${c}: ${d.t}`);
  }
  const rels = t.rels || t.relationships || [];
  if (rels.length) console.log('  rel: ' + rels.map((r) => `${r.cols.join(',')}->${r.to}.${r.toCols.join(',')}`).join(' | '));
}
