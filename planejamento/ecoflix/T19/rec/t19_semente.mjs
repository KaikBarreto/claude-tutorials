#!/usr/bin/env node
// T19 · grava o estado da instância FAKE_URL (logo depois do ensaio de um capítulo, na mesma trava) como semente extra:
//   FAKE_URL=http://127.0.0.1:54319 node rec/t19/t19_semente.mjs apos-cap03
// Tabelas do RH e do ponto inteiras (o mundo base não as tem); das outras (caixa, banco, categorias), só o que nasceu em 10/11 a
// partir das 08:29 (o mundo base termina às 08:30 e não tem nada nesse dia); e os acertos (_patch) da
// semente inicio (slug do tablet, nome da categoria da folha). O arquivo vai para rec/mundo/seeds-extra/t19/<nome>.json e o
// capítulo seguinte parte dele (seedExtra ["t19/<nome>"]).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const FAKE = process.env.FAKE_URL;
const nome = process.argv[2];
if (!FAKE || !nome || !/^[a-z0-9-]+$/.test(nome)) {
  console.error('uso: FAKE_URL=http://127.0.0.1:<porta> node rec/t19/t19_semente.mjs <nome>');
  process.exit(2);
}
const here = path.dirname(fileURLToPath(import.meta.url));
const dir = path.resolve(here, '../mundo/seeds-extra/t19');
const inicio = JSON.parse(fs.readFileSync(path.join(dir, 'inicio.json'), 'utf8'));
const INTEIRAS = ['employee_departments', 'employees', 'employee_movements', 'time_settings', 'time_records', 'time_sheets', 'time_schedules',
  'employee_absences', 'employee_absence_attachments', 'employee_ponto_pins'];
const DO_DIA = ['cash_register', 'cash_transactions', 'bank_transactions', 'financial_categories'];
const DESDE = '2026-11-10T11:29:00.000Z';
const ler = async (t) => {
  const r = await fetch(`${FAKE}/__dev/state?table=${t}`);
  if (!r.ok) throw new Error(`${t}: ${r.status}`);
  return r.json();
};
const out = { _doc: `T19 · estado depois do ensaio (${nome}), gravado por rec/t19/t19_semente.mjs em ${new Date().toISOString()}` };
for (const t of INTEIRAS) out[t] = await ler(t);
for (const t of DO_DIA) out[t] = (await ler(t)).filter((r) => String(r.created_at || r.opened_at || '') >= DESDE);
out._patch = inicio._patch;
if (!out.employees.length || !out.cash_register.length) {
  console.error(`semente ${nome}: estado vazio (funcionários ${out.employees.length}, caixas ${out.cash_register.length}): não gravei`);
  process.exit(3);
}
fs.writeFileSync(path.join(dir, `${nome}.json`), JSON.stringify(out));
console.log(`semente ${nome}: ` + Object.entries(out).filter(([k, v]) => !k.startsWith('_') && v.length).map(([k, v]) => `${k} ${v.length}`).join(', '));
