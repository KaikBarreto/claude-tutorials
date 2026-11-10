// cap00/cap01: primeira tela, rodapé do menu, Configurações, aba Usuários e Permissões
export default async ({ page, shot, t, ms, log, settle, base }) => {
  await t('goto /dashboard', async () => { await page.goto(base + '/dashboard'); await settle(); });
  await ms(1200);
  log('url', page.url());
  await shot('c01-a-dashboard');
  const rodape = await page.evaluate(() => [...document.body.innerText.split('\n')].filter((l) => /v\s?1\.\d+\.\d+|Dominex v/i.test(l)));
  log('versão no rodapé:', JSON.stringify(rodape));
  const menu = await page.evaluate(() => [...document.querySelectorAll('aside a, aside button, nav a, nav button')].map((e) => (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\s+/g, ' ')).filter(Boolean).slice(0, 80));
  log('menu:', JSON.stringify(menu));
  await t('clique Configurações (rodapé)', () => page.getByRole('button', { name: 'Configurações', exact: true }).first().click());
  await settle(); await ms(900);
  log('url', page.url());
  await shot('c01-b-config');
  const tabs = await page.getByRole('tab').allTextContents();
  log('abas:', JSON.stringify(tabs));
  await t('aba Usuários e Permissões', () => page.getByRole('tab', { name: /Usuários e Permissões/ }).click());
  await settle(); await ms(900);
  log('url', page.url());
  await shot('c01-c-usuarios');
  const txt = await page.evaluate(() => document.querySelector('main')?.innerText.split('\n').map((l) => l.trim()).filter(Boolean).slice(0, 40));
  log('main:', JSON.stringify(txt));
  const botoes = await page.evaluate(() => [...document.querySelectorAll('main button')].map((b) => ({ t: (b.getAttribute('aria-label') || b.textContent || '').trim().replace(/\s+/g, ' '), r: (() => { const x = b.getBoundingClientRect(); return [Math.round(x.x), Math.round(x.y), Math.round(x.width), Math.round(x.height)]; })() })).filter((b) => b.t).slice(0, 30));
  log('botões do main:', JSON.stringify(botoes));
};
