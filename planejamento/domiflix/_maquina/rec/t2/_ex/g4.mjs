export default async ({ page, shot, settle, base, log }) => {
  await page.goto(base + '/'); await settle(); await page.waitForTimeout(4000);
  await shot('g4'); log('url ' + page.url());
  log('body: ' + (await page.locator('body').innerText()).slice(0, 500).replace(/\n/g, ' | '));
};
