export default async ({ page, shot, settle, base, log }) => {
  await page.goto(base + '/dashboard'); await settle();
  await page.goto(base + '/configuracoes?tab=usuarios'); await settle(); await page.waitForTimeout(1500);
  await page.locator('main').getByRole('button', { name: 'Configurações', exact: true }).click();
  await page.getByText('Configurações de Cargos').waitFor({ timeout: 8000 });
  await page.getByRole('button', { name: 'Novo Cargo', exact: true }).click();
  await page.waitForTimeout(800);
  const sw = (n) => page.getByRole('switch', { name: n, exact: true });
  const seta = (n) => page.getByRole('button', { name: `Ver ações de ${n}`, exact: true });
  await sw('Acesso à tela Agenda').click(); await seta('Agenda').click(); await sw('Ver Toda a Agenda').click();
  log('agenda seta expanded=' + await seta('Agenda').getAttribute('aria-expanded'));
  await sw('Acesso à tela Ordens de Serviço').scrollIntoViewIfNeeded(); await sw('Acesso à tela Ordens de Serviço').click(); await page.waitForTimeout(500);
  log('OS seta expanded=' + await seta('Ordens de Serviço').getAttribute('aria-expanded') + ' agenda=' + await seta('Agenda').getAttribute('aria-expanded'));
  await seta('Ordens de Serviço').click(); await page.waitForTimeout(600);
  log('OS seta depois=' + await seta('Ordens de Serviço').getAttribute('aria-expanded') + ' criarOS=' + await sw('Criar OS').count());
  await shot('g6');
};
