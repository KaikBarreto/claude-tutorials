export default async ({ page, shot, settle, base, log }) => {
  await page.goto(base + '/dashboard'); await settle(); await page.waitForTimeout(2500);
  await shot('g1-dashboard');
  log('dark gate: ' + await page.locator('[data-domiflix-intro]').count());
  log('body: ' + (await page.locator('body').innerText()).slice(0, 400).replace(/\n/g, ' | '));
  await page.goto(base + '/configuracoes?tab=usuarios'); await settle(); await page.waitForTimeout(2500);
  await shot('g1-config');
  log('body: ' + (await page.locator('body').innerText()).slice(0, 500).replace(/\n/g, ' | '));
};
