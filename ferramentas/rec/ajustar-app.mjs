#!/usr/bin/env node
// Aplica na CÓPIA do código do app os ajustes do mundo (<mundo>/app/ajustes.json) para o build falar com o Supabase
// falso. Nunca rode no repositório do app (recusa pasta com .git).
//   node rec/ajustar-app.mjs <pasta-da-copia>          (o rec/setup-app.sh chama sozinho)
// ajustes.json:
//   "substituir": [{ "arquivo", "regex", "por" }]   cada regex tem de casar 1 vez (o app mudou? para e avisa)
//   "antesDoBuild": ["comando", ...]               roda na cópia antes do vite build (rec/run.sh build)
//   "foraDoBuild": ["pasta", ...]                  pastas do dist que não vão para <TUT_HOME>/app (vídeos do site etc.)
// Tokens em "por": {FAKE_URL} {FAKE_HOST} {ANON_KEY} {PROJECT_ID} (endereço gravado no build: env do mundo ou rec/env.json).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REC = path.dirname(fileURLToPath(import.meta.url));
const dir = path.resolve(process.argv[2] || '');
if (!process.argv[2] || !fs.existsSync(path.join(dir, 'package.json'))) {
  console.error('uso: node rec/ajustar-app.mjs <pasta-da-copia-do-app>');
  process.exit(2);
}
if (fs.existsSync(path.join(dir, '.git'))) {
  console.error(`${dir} tem .git: e o repositorio do app, nao uma copia. Nada foi mudado.`);
  process.exit(1);
}
const MUNDO = process.env.FAKE_MUNDO || path.join(REC, 'mundo');
const arq = path.join(MUNDO, 'app/ajustes.json');
if (!fs.existsSync(arq)) {
  console.log('sem ajustes do mundo (app/ajustes.json): nada a fazer');
  process.exit(0);
}
const base = JSON.parse(fs.readFileSync(path.join(REC, 'env.json'), 'utf8'));
let env = base;
try {
  env = { ...base, ...(JSON.parse(fs.readFileSync(path.join(MUNDO, 'mundo.json'), 'utf8')).env || {}) };
} catch {}
const u = new URL(env.fakeUrl);
const tokens = { FAKE_URL: env.fakeUrl.replace(/\/$/, ''), FAKE_HOST: u.host, ANON_KEY: env.anonKey, PROJECT_ID: env.projectId };
const troca = (s) => String(s).replace(/\{(\w+)\}/g, (m, k) => (k in tokens ? tokens[k] : m));

const aj = JSON.parse(fs.readFileSync(arq, 'utf8'));
let erros = 0;
for (const s of aj.substituir || []) {
  const f = path.join(dir, s.arquivo);
  if (!fs.existsSync(f)) {
    console.error(`FALTA ${s.arquivo} (ajuste: ${s.porque || s.regex})`);
    erros++;
    continue;
  }
  const txt = fs.readFileSync(f, 'utf8');
  const re = new RegExp(s.regex, 'g');
  const n = (txt.match(re) || []).length;
  if (n !== 1) {
    console.error(`${s.arquivo}: o ajuste casou ${n} vez(es) (esperado 1): /${s.regex}/ — o app mudou? Confira ${arq}`);
    erros++;
    continue;
  }
  fs.writeFileSync(f, txt.replace(re, () => troca(s.por)));
  console.log(`ajustado ${s.arquivo}: ${s.porque || s.regex}`);
}
if (erros) process.exit(1);
