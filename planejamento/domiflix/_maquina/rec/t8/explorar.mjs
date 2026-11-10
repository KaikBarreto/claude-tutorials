#!/usr/bin/env node
// T8 · EXPLORAÇÃO (computador, 1280x800) (não é gravação): abre o app no Supabase falso da instância FAKE_URL e executa passos simples,
// tirando fotos (PNG, em px CSS) e despejando textos/HTML. Serve para descobrir seletores e testar arrastos antes de gravar.
//   (sob a trava) FAKE_URL=http://127.0.0.1:54325 FAKE_NOW=2026-11-03T09:00:00-03:00 nice -n 10 node rec/t8/explorar.mjs rec/t8/_ex/algo.json [--out rec/t8/_ex/out]
// O arquivo: { "seedExtra": [...], "user": "email opcional", "steps": [ {do, ...} ] }
// Passos: wheel{x,y,dx,dy} goto{url} click{target} dblclick{target} hover{target} type{target,text} press{key} wait{ms} waitFor{target|text|selector,timeout}
//         shot{name,full?,clip?} text{target|selector,name?} html{selector,max?} eval{js} list{selector,attr?} drag{target,to,steps?}
//         count{target} clock{set|forward} geo{lat,lng} upload{target,file} sig{target,pts?} scrolly{by,selector?}
// Alvos: os mesmos do robô (role/name/exact/text/placeholder/label/selector/within/hasText/nth).
import fs from 'node:fs';
import path from 'node:path';
import { launchBrowser, openSession, closeSession, settle } from '../recorder/browser.mjs';
import { locatorFor } from '../recorder/runner.mjs';
import { FAKE_URL, APP_URL } from '../recorder/env.mjs';

const argv = process.argv.slice(2);
const file = argv[0];
const outDir = path.resolve(argv.includes('--out') ? argv[argv.indexOf('--out') + 1] : path.join(path.dirname(file), 'out'));
fs.mkdirSync(outDir, { recursive: true });
const script = JSON.parse(fs.readFileSync(file, 'utf8'));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

await fetch(`${FAKE_URL}/__dev/reset`, { method: 'POST' });
if (script.seedExtra?.length) {
  const r = await fetch(`${FAKE_URL}/__dev/seed`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ files: script.seedExtra }) });
  if (!r.ok) throw new Error('seed: ' + (await r.text()));
}
const s = await openSession({ email: script.user, storage: script.storage, device: script.device });
const { page } = s;
// o screencast mantém o navegador produzindo quadros (sem ele o framer-motion, que anda por requestAnimationFrame, não termina as animações)
const cdp = await page.context().newCDPSession(page);
cdp.on('Page.screencastFrame', (f) => { cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 5, maxWidth: 160, maxHeight: 100, everyNthFrame: 1 });
const consoleErr = [];
if (process.env.EX_NET) page.on('request', (r) => { if (r.method() !== 'GET' && /\/rest\/v1\//.test(r.url())) console.log('   >> ' + r.method() + ' ' + r.url().replace(/^.*\/rest\/v1\//, '').slice(0, 110) + ' ' + String(r.postData() || '').slice(0, 160)); });
if (process.env.EX_CONSOLE) page.on('console', (m) => console.log('   [console.' + m.type() + '] ' + m.text().slice(0, 220)));
page.on('pageerror', (e) => consoleErr.push('pageerror: ' + String(e).slice(0, 300)));
const log = (...a) => console.log(...a);
let n = 0;
try {
  await page.goto(new URL(script.start || '/dashboard', APP_URL).href, { waitUntil: 'load', timeout: 120000 });
  await settle(s, { quietMs: 1500, timeoutMs: 60000 });
  for (const st of script.steps) {
    n++;
    const tag = `${String(n).padStart(2, '0')} ${st.do}`;
    try {
      switch (st.do) {
        case 'goto':
          await page.goto(new URL(st.url, APP_URL).href, { waitUntil: 'load', timeout: 120000 });
          await settle(s, { quietMs: 1200, timeoutMs: 60000 });
          break;
        case 'click': await locatorFor(page, st.target).click({ timeout: (st.timeout ?? 8) * 1000, force: !!st.force }); await sleep(st.after ?? 500); break;
        case 'dblclick': await locatorFor(page, st.target).dblclick({ timeout: 8000 }); await sleep(st.after ?? 500); break;
        case 'hover': await locatorFor(page, st.target).hover({ timeout: 8000 }); await sleep(st.after ?? 300); break;
        case 'type': await locatorFor(page, st.target).fill(st.text, { timeout: 8000 }); await sleep(st.after ?? 300); break;
        case 'press': await page.keyboard.press(st.key); await sleep(st.after ?? 300); break;
        case 'wait': await sleep(st.ms ?? 500); break;
        case 'wheel': await page.mouse.move(st.x, st.y); await page.mouse.wheel(st.dx ?? 0, st.dy ?? 0); await sleep(st.after ?? 700); break;
        case 'waitFor': {
          const t = st.target ?? (st.text !== undefined ? { text: st.text } : { selector: st.selector });
          await locatorFor(page, t).waitFor({ state: st.state || 'visible', timeout: (st.timeout ?? 10) * 1000 });
          break;
        }
        case 'count': log(`${tag}: ${await locatorFor(page, st.target).count()} elemento(s) visíveis`); break;
        case 'shot': {
          const p = path.join(outDir, `${st.name}.png`);
          await page.screenshot({ path: p, scale: 'css', fullPage: !!st.full, ...(st.clip ? { clip: st.clip } : {}) });
          log(`${tag}: foto ${p}`);
          break;
        }
        case 'text': {
          const loc = st.selector ? page.locator(st.selector).first() : locatorFor(page, st.target);
          const t = await loc.innerText({ timeout: 8000 });
          log(`${tag}${st.name ? ' [' + st.name + ']' : ''}:\n${t.slice(0, st.max ?? 3000)}`);
          break;
        }
        case 'html': {
          const h = await page.locator(st.selector).first().evaluate((e) => e.outerHTML);
          log(`${tag} [${st.selector}]:\n${h.slice(0, st.max ?? 3000)}`);
          break;
        }
        case 'eval': log(`${tag}: ${JSON.stringify(await page.evaluate(st.js)).slice(0, st.max ?? 3000)}`); break;
        case 'list': {
          const items = await page.locator(st.selector).evaluateAll((els, attr) => els.map((e) => (attr ? e.getAttribute(attr) : (e.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 120))), st.attr || null);
          log(`${tag} [${st.selector}] ${items.length}:\n  - ` + items.join('\n  - '));
          break;
        }
        case 'clock':
          if (st.forward !== undefined) await page.clock.fastForward(st.forward);
          else if (st.set) await page.clock.setSystemTime(new Date(st.set));
          break;
        case 'drag': {
          const src = locatorFor(page, st.target);
          await src.scrollIntoViewIfNeeded().catch(() => {});
          const sb = await src.boundingBox();
          let dx, dy;
          if (st.to && typeof st.to.x === 'number') ({ x: dx, y: dy } = st.to);
          else {
            const dl = locatorFor(page, st.to);
            await dl.scrollIntoViewIfNeeded().catch(() => {});
            const db = await dl.boundingBox();
            dx = db.x + db.width / 2; dy = db.y + db.height / 2;
          }
          const sx = sb.x + sb.width / 2, sy = sb.y + sb.height / 2;
          await page.mouse.move(sx, sy);
          await page.mouse.down();
          await sleep(200);
          await page.mouse.move(sx + 9, sy + 7, { steps: 4 });
          await page.mouse.move(dx, dy, { steps: st.steps ?? 25 });
          await sleep(300);
          await page.mouse.up();
          await sleep(st.after ?? 800);
          break;
        }
        case 'state': {
          const rows = await (await fetch(`${FAKE_URL}/__dev/state?table=${encodeURIComponent(st.table)}`)).json();
          const hit = rows.filter((r) => Object.entries(st.where || {}).every(([k, v]) => String(r[k]) === String(v)));
          log(`${tag} [${st.table}] ${hit.length}/${rows.length}: ` + JSON.stringify(hit.slice(0, st.max ?? 6).map((r) => (st.pick ? Object.fromEntries(st.pick.map((k) => [k, r[k]])) : r))).slice(0, 3000));
          break;
        }
        case 'geo': await s.context.setGeolocation({ latitude: st.lat, longitude: st.lng, accuracy: st.accuracy ?? 15 }); break;
        case 'upload': {
          const [fc] = await Promise.all([page.waitForEvent('filechooser', { timeout: 8000 }), locatorFor(page, st.target).click({ timeout: 8000 })]);
          await fc.setFiles(path.resolve(st.file));
          await sleep(st.after ?? 1500);
          break;
        }
        case 'sig': {
          const bb = await locatorFor(page, st.target).boundingBox();
          const pts = st.pts || [[0.15, 0.6, 0.35, 0.3, 0.5, 0.65, 0.7, 0.35, 0.85, 0.55]];
          for (const tr of pts) {
            const xy = tr.map((v, i) => (i % 2 ? bb.y + v * bb.height : bb.x + v * bb.width));
            await page.mouse.move(xy[0], xy[1]);
            await page.mouse.down();
            for (let i = 2; i < xy.length; i += 2) await page.mouse.move(xy[i], xy[i + 1], { steps: 8 });
            await page.mouse.up();
            await sleep(200);
          }
          await sleep(st.after ?? 600);
          break;
        }
        case 'scrolly': {
          await page.evaluate(({ by, selector }) => { const el = selector ? document.querySelector(selector) : window; el.scrollBy({ top: by, behavior: 'instant' }); }, { by: st.by, selector: st.selector || null });
          await sleep(st.after ?? 500);
          break;
        }
        default: throw new Error('passo desconhecido: ' + st.do);
      }
      if (['click', 'dblclick', 'press', 'drag', 'type'].includes(st.do)) { await settle(s, { quietMs: 400, timeoutMs: 15000 }).catch(() => {}); await sleep(st.settle ?? 350); }
      if (!['shot', 'text', 'html', 'eval', 'list', 'count', 'state'].includes(st.do)) log(`${tag}: ok${st.target ? ' ' + JSON.stringify(st.target).slice(0, 80) : st.url ? ' ' + st.url : ''}`);
    } catch (e) {
      log(`${tag}: FALHOU ${String(e.message || e).split('\n')[0]}`);
      await page.screenshot({ path: path.join(outDir, `falha-${String(n).padStart(2, '0')}.png`), scale: 'css' }).catch(() => {});
      if (!st.optional && script.stopOnFail !== false) break;
    }
  }
} finally {
  if (consoleErr.length) log('erros de página:', consoleErr.slice(0, 5));
  const bad = (s.diag.bad || []).filter((x) => !/\/auth\/v1\/user|406 GET .*form_responses/.test(x));
  if (bad.length) log('respostas >= 400:\n  ' + bad.slice(-12).join('\n  '));
  if (s.diag.console?.length) log('console:\n  ' + s.diag.console.slice(-8).map((c) => c.type + ' ' + c.text.slice(0, 200)).join('\n  '));
  if (s.diag.failed?.length) log('falhas de rede:\n  ' + s.diag.failed.slice(-6).join('\n  '));
  await closeSession(s).catch(() => {});
}
