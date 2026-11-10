#!/usr/bin/env node
// T2 · exploração da Dominex 1.38.9 (NÃO grava vídeo): abre o app como um usuário do Supabase falso e roda um cenário em JavaScript,
// com atalhos para tirar fotos (JPEG em CSS px, só para olhar), medir o tempo de cada gesto e imprimir fatos do DOM.
//   flock $TUT_HOME/.heavy.lock nice -n 10 env FAKE_URL=http://127.0.0.1:54324 FAKE_NOW=2026-11-03T09:00:00-03:00 \
//     node rec/t2/explorar.mjs rec/t2/_ex/cenario.mjs [e-mail do usuário] [--seed t2/inicio,t2/apos-cap04]
// O cenário exporta `default async ({ page, sess, shot, t, ms, log, settle, base }) => {...}`.
//   shot('nome')  salva rec/t2/_debug/nome.jpg      t(rotulo, fn)  mede e imprime quanto fn() levou
//   settle()      espera a rede assentar             base           endereço do app
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { openSession, closeSession, settle as settleNet } from '../recorder/browser.mjs';
import { APP_URL, FAKE_URL } from '../recorder/env.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const seedIdx = args.indexOf('--seed');
const seeds = seedIdx >= 0 ? args.splice(seedIdx, 2)[1].split(',').filter(Boolean) : null;
const [cenario, email] = args;
if (!cenario) {
  console.error('uso: node rec/t2/explorar.mjs <cenario.mjs> [email] [--seed t2/inicio,t2/apos-cap04]');
  process.exit(2);
}
const DEBUG = path.join(here, '_debug');
fs.mkdirSync(DEBUG, { recursive: true });

// Estado do backend: reset + sementes (como o gravador faz antes de cada gravação)
if (seeds) {
  await fetch(`${FAKE_URL}/__dev/reset`, { method: 'POST' });
  const r = await fetch(`${FAKE_URL}/__dev/seed`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ files: seeds }) });
  console.log('sementes:', r.status, (await r.text()).slice(0, 160));
}

const sess = await openSession({ email: email || undefined, telemetry: false });
const { page, diag } = sess;
const ms = (n) => new Promise((r) => setTimeout(r, n));
const log = (...a) => console.log(...a);
const shot = async (nome) => {
  const f = path.join(DEBUG, `${nome}.jpg`);
  await page.screenshot({ path: f, type: 'jpeg', quality: 70, scale: 'css' });
  console.log(`  [foto] ${path.relative(path.join(here, '..', '..'), f)}`);
};
const t = async (rotulo, fn) => {
  const t0 = Date.now();
  let r;
  try {
    r = await fn();
  } catch (e) {
    console.log(`  [${rotulo}] ERRO em ${Date.now() - t0} ms: ${String(e.message).split('\n')[0]}`);
    return undefined;
  }
  console.log(`  [${rotulo}] ${Date.now() - t0} ms`);
  return r;
};
try {
  const mod = await import(pathToFileURL(path.resolve(cenario)).href);
  await mod.default({ page, sess, shot, t, ms, log, settle: () => settleNet(sess), base: APP_URL });
} catch (e) {
  console.log('ERRO no cenário:', e.stack || e);
} finally {
  const ruido = (diag.console || []).filter((c) => !/realtime\/v1\/websocket/.test(c.text));
  console.log('console (fora o WS):', JSON.stringify(ruido.slice(0, 5)));
  console.log('erros de página:', JSON.stringify(diag.pageErrors.slice(0, 3)), '| falhas:', JSON.stringify(diag.failed.slice(0, 3)), '| >=400:', JSON.stringify(diag.bad.slice(0, 5)));
  await closeSession(sess);
}
