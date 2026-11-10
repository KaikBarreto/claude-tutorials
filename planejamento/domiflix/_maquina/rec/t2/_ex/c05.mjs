// cap08: Rafael logado. Parte de t2/apos-cap07.
const geom = (page, sel) => page.evaluate((s) => [...document.querySelectorAll(s)].map((e) => { const r = e.getBoundingClientRect(); return { t: (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; }), sel);
export default async ({ page, shot, t, ms, log, settle, base }) => {
  await t('goto /', async () => { await page.goto(base + '/'); await settle(); });
  await ms(1500);
  log('url inicial:', page.url());
  await shot('c08-a-inicio');
  log('menu:', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('aside a, aside button, nav a')].map((e) => (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\s+/g, ' ')).filter(Boolean).slice(0, 40))));
  log('links do menu (rect):', JSON.stringify(await geom(page, 'aside a')));
  log('textos modais:', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('[role=dialog], [role=alertdialog]')].map((e) => e.innerText.slice(0, 120)))));
  log('rodapé:', JSON.stringify((await page.evaluate(() => document.body.innerText.split('\n').filter((l) => /Dominex v|v1\.38/.test(l)))))); 
  await t('Área do Técnico', () => page.getByRole('link', { name: /Área do Técnico/ }).first().click());
  await settle(); await ms(1200);
  log('url:', page.url());
  await shot('c08-b-area');
  await t('Agenda', () => page.getByRole('link', { name: 'Agenda', exact: true }).first().click());
  await settle(); await ms(1200);
  log('url:', page.url());
  await shot('c08-c-agenda');
};
