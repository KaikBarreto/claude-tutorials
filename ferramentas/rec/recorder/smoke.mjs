#!/usr/bin/env node
// Teste de fumaca do kit: abre as telas combinadas contra o Supabase falso e relata erros de console, falhas de
// rede, respostas >= 400 e o que o fakebase anotou em desconhecidos.log.
//   node rec/recorder/smoke.mjs                 clientes, detalhe do cliente (todas as abas), equipamentos, detalhe,
//                                               e criar um cliente pela tela (confere que aparece na lista)
//   node rec/recorder/smoke.mjs /os /contratos  rotas avulsas
//   opcoes: --headed  --shots (salva PNG em rec/.runtime/smoke/)  --no-create (pula a criacao do cliente)
// Termina com codigo 1 se houve erro de console, falha de rede, http >= 400 ou o cliente criado nao apareceu.
import fs from 'node:fs';
import path from 'node:path';
import { APP_URL, FAKE_URL, RUNTIME_DIR } from './env.mjs';
import { openSession, closeSession, settle } from './browser.mjs';

const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const routes = args.filter((a) => a.startsWith('/'));
const SHOTS = flag('--shots');
const SHOT_DIR = path.join(RUNTIME_DIR, 'smoke');
if (SHOTS) fs.mkdirSync(SHOT_DIR, { recursive: true });

const getJson = async (p) => (await fetch(`${FAKE_URL}${p}`)).json();
let knownUnknowns = new Set();
async function newUnknowns() {
  const { items } = await getJson('/__dev/unknowns');
  const out = [];
  for (const it of items) {
    const k = `${it.kind}|${it.name}`;
    if (!knownUnknowns.has(k)) {
      knownUnknowns.add(k);
      out.push(`${it.kind} ${it.name}${it.detail ? ' — ' + String(it.detail).slice(0, 100) : ''}`);
    }
  }
  return out;
}

const s = await openSession({ headed: flag('--headed') });
const { page, diag } = s;
let problems = 0;
let mark = { c: 0, e: 0, f: 0, b: 0 };

function delta(label) {
  const c = diag.console.slice(mark.c);
  const e = diag.pageErrors.slice(mark.e);
  const f = diag.failed.slice(mark.f);
  const b = diag.bad.slice(mark.b);
  mark = { c: diag.console.length, e: diag.pageErrors.length, f: diag.failed.length, b: diag.bad.length };
  const n = c.length + e.length + f.length + b.length;
  problems += n;
  console.log(`${n ? 'XX' : 'ok'}  ${label}${n ? `  (console ${c.length}, erros de pagina ${e.length}, falhas ${f.length}, http>=400 ${b.length})` : ''}`);
  for (const x of e) console.log(`      pageerror: ${x.split('\n')[0]}`);
  for (const x of c) console.log(`      console.${x.type}: ${x.text.split('\n')[0]}${x.url ? '  @' + x.url.replace(APP_URL, '') : ''}`);
  for (const x of f) console.log(`      falha: ${x}`);
  for (const x of b) console.log(`      http: ${x}`);
  return n;
}

async function visit(label, url, { wait = null, tabs = false } = {}) {
  const t0 = Date.now();
  await page.goto(APP_URL + url, { waitUntil: 'load', timeout: 60000 });
  if (wait) await page.waitForSelector(wait, { timeout: 20000 }).catch(() => console.log(`      (nao apareceu: ${wait})`));
  await settle(s, { quietMs: 800, timeoutMs: 25000 });
  await page.waitForTimeout(500);
  if (SHOTS) await page.screenshot({ path: path.join(SHOT_DIR, label.replace(/\W+/g, '_') + '.png'), scale: 'css' });
  delta(`${label}  [${url}]  ${Date.now() - t0}ms  -> ${page.url().replace(APP_URL, '')}`);
  for (const u of await newUnknowns()) console.log(`      desconhecido: ${u}`);

  if (tabs) {
    // abas da ficha (as duas primeiras, "Clientes" e "Fornecedores", sao da tela e nao da ficha)
    const names = (await page.locator('[role="tab"]').allInnerTexts()).map((t) => t.trim().replace(/\s+/g, ' ')).filter((t) => !/^(Clientes|Fornecedores)$/.test(t));
    console.log(`      ${names.length} abas da ficha: ${names.join(' | ')}`);
    for (let i = 0; i < names.length; i++) {
      const name = names[i];
      await page.getByRole('tab', { name, exact: true }).click({ timeout: 8000 }).catch((e) => console.log(`      (clique na aba "${name}" falhou: ${String(e.message).split('\n')[0]})`));
      await settle(s, { quietMs: 600, timeoutMs: 15000 });
      await page.waitForTimeout(350);
      if (SHOTS) await page.screenshot({ path: path.join(SHOT_DIR, `${label}_aba${i + 1}_${name}`.replace(/\W+/g, '_') + '.png'), scale: 'css' });
      delta(`   aba ${i + 1}/${names.length} "${name}"`);
      for (const u of await newUnknowns()) console.log(`      desconhecido: ${u}`);
    }
  }
}

// Criar um cliente pela tela: abre o formulario, digita o nome, "Criar", e confere no banco falso e na lista.
async function createCustomer() {
  const NAME = 'Casa de Carnes Boa Brasa';
  const t0 = Date.now();
  await page.goto(APP_URL + '/clientes', { waitUntil: 'load', timeout: 60000 });
  await settle(s, { quietMs: 800, timeoutMs: 25000 });
  await page.getByRole('button', { name: /Novo Cliente/ }).click({ timeout: 10000 });
  await page.waitForSelector('[role=dialog]', { timeout: 10000 });
  await page.getByPlaceholder('Nome do cliente').fill(NAME);
  await page.getByRole('button', { name: 'Criar', exact: true }).click();
  await settle(s, { quietMs: 1000, timeoutMs: 15000 });
  await page.waitForTimeout(1200);
  const rows = await getJson('/__dev/state?table=customers');
  const novo = rows.find((c) => c.name === NAME);
  await page.getByPlaceholder('Buscar clientes...').fill('Boa Brasa');
  await settle(s, { quietMs: 800, timeoutMs: 15000 });
  await page.waitForTimeout(500);
  const naLista = await page.getByText(NAME).count();
  if (SHOTS) await page.screenshot({ path: path.join(SHOT_DIR, 'cliente-criado.png'), scale: 'css' });
  const n = delta(`criar cliente pela tela  ${Date.now() - t0}ms  -> ${page.url().replace(APP_URL, '')}`);
  const ok = !!novo && naLista > 0;
  console.log(`${ok ? 'ok' : 'XX'}     banco falso: ${novo ? `gravado (codigo ${novo.public_short_code}, empresa ${String(novo.company_id).slice(0, 8)})` : 'NAO gravou'}; na lista: ${naLista ? 'aparece' : 'NAO aparece'}`);
  if (!ok) problems++;
  for (const u of await newUnknowns()) console.log(`      desconhecido: ${u}`);
  await fetch(`${FAKE_URL}/__dev/reset`, { method: 'POST' }); // nao deixa o cliente de teste para a proxima gravacao
  return n;
}

try {
  // primeira visita: aquece o app antes de medir (no vite dev ele pode recarregar sozinho ao otimizar dependencias)
  console.log('— aquecimento —');
  await page.goto(APP_URL + '/', { waitUntil: 'load', timeout: 120000 }).catch((e) => console.log('aquecimento:', e.message));
  await settle(s, { quietMs: 1500, timeoutMs: 60000 });
  await page.waitForTimeout(1500);
  delta('aquecimento  [/]  -> ' + page.url().replace(APP_URL, ''));
  for (const u of await newUnknowns()) console.log(`      desconhecido: ${u}`);

  if (routes.length) {
    for (const r of routes) await visit(r, r);
  } else {
    const customers = await getJson('/__dev/state?table=customers');
    const equip = await getJson('/__dev/state?table=equipment');
    const cust = customers.find((c) => /Padaria/i.test(c.name)) || customers[0];
    const eq = equip.find((e) => e.customer_id === cust.id) || equip[0];
    await visit('clientes', '/clientes', { wait: 'text=Padaria' });
    await visit('cliente-detalhe', `/clientes/${cust.id}`, { tabs: true });
    await visit('equipamentos', '/equipamentos');
    await visit('equipamento-detalhe', `/equipamentos/${eq.id}`);
    if (!flag('--no-create')) await createCustomer();
  }
} finally {
  console.log(`\n${problems ? 'COM PROBLEMAS' : 'SEM PROBLEMAS'}: ${problems} ocorrencia(s). externos desviados: ${new Set(diag.externos.map((x) => new URL(x.url).hostname)).size} host(s) ${[...new Set(diag.externos.map((x) => new URL(x.url).hostname))].join(', ')}`);
  await closeSession(s);
  if (problems) process.exitCode = 1;
}
