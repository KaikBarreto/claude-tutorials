export default async ({ page, shot, settle, base, log }) => {
  await page.goto(base + '/dashboard'); await settle();
  await page.goto(base + '/configuracoes?tab=usuarios'); await settle(); await page.waitForTimeout(1500);
  await page.locator('main').getByRole('button', { name: 'Configurações', exact: true }).click();
  await page.getByText('Configurações de Cargos').waitFor({ timeout: 8000 });
  await page.getByRole('button', { name: 'Novo Cargo', exact: true }).click();
  await page.waitForTimeout(800);
  const os = page.getByRole('switch', { name: 'Acesso à tela Ordens de Serviço', exact: true });
  await os.scrollIntoViewIfNeeded(); await os.click(); await page.waitForTimeout(600);
  const seta = page.getByRole('button', { name: 'Ver ações de Ordens de Serviço', exact: true });
  log('seta count ' + await seta.count() + ' expanded=' + await seta.getAttribute('aria-expanded'));
  await seta.click(); await page.waitForTimeout(800);
  log('expanded após clique=' + await seta.getAttribute('aria-expanded'));
  const sw = await page.locator('[role=dialog] [role=switch]').evaluateAll(els => els.map(e => e.getAttribute('aria-label') + ':' + e.getAttribute('aria-checked')));
  log(sw.join(' | '));
  await shot('g5');
};
