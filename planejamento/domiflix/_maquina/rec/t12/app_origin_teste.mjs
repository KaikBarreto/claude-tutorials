// Teste da opção APP_ORIGIN do gravador (rec/recorder/app-origin.mjs): abre o app na origem de produto, confere que tudo vem
// do app local / Supabase falso, que nada sai para a rede e que o app não muda de comportamento.
//   FAKE_URL=http://127.0.0.1:54327 FAKE_NOW=2026-11-10T10:00:00-03:00 APP_ORIGIN=https://www.dominex.app \
//     flock $TUT_HOME/.heavy.lock nice -n 10 node rec/t12/app_origin_teste.mjs [rota ...]
import { openSession, closeSession, settle } from '../recorder/browser.mjs';
import { APP_URL, APP_ORIGIN } from '../recorder/env.mjs';

const rotas = process.argv.slice(2).filter((a) => a.startsWith('/'));
if (!rotas.length) rotas.push('/', '/clientes');
const anon = process.argv.includes('--anon');
const s = await openSession({ anonymous: anon, verboseNet: false });
const { page, context, diag } = s;
const porHost = new Map();
context.on('request', (r) => {
  const h = new URL(r.url()).host;
  porHost.set(h, (porHost.get(h) || 0) + 1);
});
const falhas = [];
context.on('requestfailed', (r) => falhas.push(`${r.method()} ${r.url().slice(0, 120)} :: ${r.failure()?.errorText}`));
for (const rota of rotas) {
  const t0 = Date.now();
  await page.goto(new URL(rota, APP_URL).href, { waitUntil: 'load', timeout: 90000 });
  await settle(s, { quietMs: 1200, timeoutMs: 40000 });
  const info = await page.evaluate(() => ({
    origin: location.origin, secure: window.isSecureContext, title: document.title, path: location.pathname,
    h1: (document.querySelector('h1,h2')?.textContent || '').slice(0, 80),
    body: (document.body.innerText || '').replace(/\s+/g, ' ').slice(0, 160),
  }));
  console.log(`[${rota}] ${Date.now() - t0}ms`, JSON.stringify(info));
}
console.log('hosts requisitados:', JSON.stringify([...porHost.entries()]));
console.log('appOrigin:', s.appOrigin ? JSON.stringify({ served: s.appOrigin.served, spaFallback: s.appOrigin.spaFallback, failed: s.appOrigin.failed }) : 'desligado');
console.log('externos desviados (net.mjs):', JSON.stringify(diag.externos.map((e) => `${e.method} ${e.url.slice(0, 100)}`)));
console.log('requisicoes que falharam:', falhas.length, JSON.stringify(falhas.slice(0, 8)));
console.log('console:', JSON.stringify(diag.console.slice(0, 6)));
console.log('pageErrors:', JSON.stringify(diag.pageErrors.slice(0, 3)));
console.log('respostas >= 400:', JSON.stringify(diag.bad.slice(0, 8)));
await page.screenshot({ path: new URL('./_teste_origem.png', import.meta.url).pathname });
await closeSession(s);
console.log('APP_ORIGIN =', APP_ORIGIN || '(desligado)');
