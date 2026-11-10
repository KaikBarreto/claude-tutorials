export default async ({ page, shot, settle, base, log }) => {
  await page.goto(base + '/configuracoes?tab=usuarios'); await settle(); await page.waitForTimeout(2500);
  const r = await page.evaluate(() => [...document.querySelectorAll('*')].filter(e => e.children.length === 0 && /usuários •/.test(e.textContent)).map(e => e.tagName + ' ' + e.className.slice(0,60) + ' | main? ' + !!e.closest('main') + ' | ' + e.parentElement.tagName));
  log(JSON.stringify(r));
  log('main count ' + await page.locator('main').count() + ' | main p match ' + await page.locator('main p', { hasText: 'usuários •' }).count());
};
