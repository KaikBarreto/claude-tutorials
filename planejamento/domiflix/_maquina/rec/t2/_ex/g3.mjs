export default async ({ page, shot, settle, base, log }) => {
  await page.goto(base + '/dashboard'); await settle(); await page.waitForTimeout(1500);
  const nav = (u) => page.evaluate((u) => { const idx = ((window.history.state && window.history.state.idx) ?? 0) + 1; window.history.pushState({ usr: null, key: 'k' + idx, idx }, '', u); window.dispatchEvent(new PopStateEvent('popstate', { state: window.history.state })); }, u);
  await nav('/configuracoes'); await settle(); await page.waitForTimeout(1500);
  await nav('/configuracoes?tab=usuarios'); await settle(); await page.waitForTimeout(3000);
  await shot('g3');
  log('url ' + page.url());
  log('body: ' + (await page.locator('main').last().innerText()).slice(0, 300).replace(/\n/g, ' | '));
};
