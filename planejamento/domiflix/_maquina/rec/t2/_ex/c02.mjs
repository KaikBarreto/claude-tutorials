// cap02/03/04: cargos. Parte de t2/inicio (nenhum cargo).
const geom = (page, sel) => page.evaluate((s) => [...document.querySelectorAll(s)].map((e) => { const r = e.getBoundingClientRect(); return { t: (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 50), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; }), sel);
export default async ({ page, shot, t, ms, log, settle, base }) => {
  await page.goto(base + '/configuracoes?tab=usuarios'); await settle(); await ms(800);
  const main = page.locator('main');
  await t('abre cargos', () => main.getByRole('button', { name: 'Configurações', exact: true }).click());
  await settle(); await ms(700);
  await shot('c02-a-cargos-vazio');
  log('dialog texto:', JSON.stringify((await page.locator('[role=dialog]').innerText()).split('\n').map((l) => l.trim()).filter(Boolean)));
  log('dialog rect:', JSON.stringify(await geom(page, '[role=dialog]')));
  log('botões do dialog:', JSON.stringify(await geom(page, '[role=dialog] button')));
  await t('Novo Cargo', () => page.getByRole('button', { name: 'Novo Cargo' }).click());
  await ms(600);
  await shot('c02-b-novo-cargo');
  log('botões após Novo Cargo:', JSON.stringify(await geom(page, '[role=dialog] button')).slice(0, 1500));
  await t('nome', () => page.getByLabel('Nome *').fill('Técnico de Campo'));
  await t('descrição', () => page.getByLabel('Descrição').fill('Agenda, ferramentas e OS pelo link'));
  // contêiner rolável do diálogo
  const rolavel = await page.evaluate(() => { const d = document.querySelector('[role=dialog]'); const c = [...d.querySelectorAll('*')].filter((e) => { const s = getComputedStyle(e); return /(auto|scroll)/.test(s.overflowY) && e.scrollHeight > e.clientHeight + 4; }); return c.map((e) => { const r = e.getBoundingClientRect(); return { cls: e.className.toString().slice(0, 80), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), sh: e.scrollHeight }; }); });
  log('roláveis:', JSON.stringify(rolavel));
  const cats = await page.evaluate(() => [...document.querySelectorAll('[role=dialog] p')].filter((p) => /uppercase/.test(p.className) && /font-semibold/.test(p.className)).map((p) => { const r = p.getBoundingClientRect(); return { t: p.textContent.trim(), y: Math.round(r.y) }; }));
  log('categorias:', JSON.stringify(cats));
  // Agenda
  const swAg = page.getByRole('switch', { name: 'Acesso à tela Agenda' });
  await t('liga Agenda', () => swAg.click());
  await ms(300);
  log('Agenda marcada:', await swAg.getAttribute('aria-checked'));
  const sw = await geom(page, '[role=dialog] [role=switch]');
  log('primeiros switches:', JSON.stringify(sw.slice(0, 6)));
  await shot('c02-c-agenda-on');
  await t('seta da Agenda', () => page.getByRole('button', { name: 'Ver ações de Agenda' }).click());
  await ms(500);
  await shot('c02-d-agenda-acoes');
  log('ações da Agenda:', JSON.stringify(await geom(page, '[role=dialog] [role=switch]')).slice(0, 1200));
  await t('fecha a seta', () => page.getByRole('button', { name: 'Ver ações de Agenda' }).click());
  await ms(400);
  // Área do Técnico
  const swTec = page.getByRole('switch', { name: 'Acesso à tela Área do Técnico™' });
  await t('scroll até Área do Técnico', () => swTec.scrollIntoViewIfNeeded());
  await ms(300);
  log('swTec rect:', JSON.stringify(await swTec.boundingBox()));
  await t('liga Área do Técnico', () => swTec.click());
  await shot('c02-e-area-tecnico');
  // OS
  const setaOS = page.getByRole('button', { name: 'Ver ações de Ordens de Serviço' });
  await setaOS.scrollIntoViewIfNeeded(); await ms(300);
  await t('seta OS', () => setaOS.click());
  await ms(500);
  await shot('c03-a-os-acoes');
  log('texto OS:', JSON.stringify((await page.locator('[role=dialog]').innerText()).split('\n').map((l) => l.trim()).filter((l) => /Ações desta tela|A tela está|Criar OS|Editar OS|Excluir OS|Lançar|Resetar|campo|0\/6/.test(l))));
  const swCampo = page.getByRole('switch', { name: 'Editar OS em campo' });
  await t('liga Editar OS em campo', () => swCampo.click());
  await ms(300);
  log('contador OS:', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('[role=dialog] .tabular-nums')].map((e) => e.textContent.trim()).filter((x) => /\/6/.test(x)))));
  await shot('c03-b-os-campo');
  log('botões do rodapé:', JSON.stringify((await geom(page, '[role=dialog] button')).filter((b) => /Criar Cargo|Cancelar|Fechar|Close|×|X/i.test(b.t))));
  await t('Criar Cargo', () => page.getByRole('button', { name: 'Criar Cargo' }).click());
  await ms(500);
  await shot('c03-c-criado');
  log('toasts:', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('[data-sonner-toast], [role=status], li[data-state=open]')].map((e) => e.textContent.trim().slice(0, 100)))));
  await ms(900);
  log('lista:', JSON.stringify((await page.locator('[role=dialog]').innerText()).split('\n').map((l) => l.trim()).filter(Boolean)));
  log('botões da lista:', JSON.stringify(await geom(page, '[role=dialog] button')));

  // ---- cap04: Escritório
  await t('Novo Cargo (2)', () => page.getByRole('button', { name: 'Novo Cargo' }).click());
  await ms(500);
  await page.getByLabel('Nome *').fill('Escritório');
  await page.getByLabel('Descrição').fill('Atendimento, OS, orçamentos e financeiro do dia a dia');
  const busca = page.getByPlaceholder('Buscar tela ou ação...');
  await t('busca orcamento', () => busca.fill('orcamento'));
  await ms(400);
  await shot('c04-a-busca-orcamento');
  log('telas na busca:', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('[role=dialog] [role=switch]')].map((e) => e.getAttribute('aria-label')))));
  await t('liga Orçamentos', () => page.getByRole('switch', { name: 'Acesso à tela Orçamentos' }).click());
  await t('busca financeiro', () => busca.fill('financeiro'));
  await ms(500);
  await shot('c04-b-busca-financeiro');
  log('na busca financeiro:', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('[role=dialog] [role=switch]')].map((e) => e.getAttribute('aria-label') + (e.getAttribute('aria-checked') === 'true' ? ' [ON]' : '')))));
  await t('liga Financeiro', () => page.getByRole('switch', { name: 'Acesso à tela Financeiro', exact: true }).click());
  await t('liga Gerenciar Financeiro', () => page.getByRole('switch', { name: 'Gerenciar Financeiro' }).click());
  await ms(300);
  log('Excluir Lançamento Financeiro rect:', JSON.stringify(await page.getByRole('switch', { name: 'Excluir Lançamento Financeiro' }).boundingBox()));
  await shot('c04-c-financeiro-on');
  await t('Limpar busca', () => page.getByRole('button', { name: 'Limpar busca' }).click());
  await ms(500);
  for (const n of ['Dashboard', 'Agenda', 'Ordens de Serviço', 'Clientes e Fornecedores', 'Equipamentos']) {
    const s = page.getByRole('switch', { name: `Acesso à tela ${n}`, exact: true });
    await t(`liga ${n}`, async () => { await s.scrollIntoViewIfNeeded(); await s.click(); });
  }
  for (const [tela, acoes] of [['Agenda', ['Ver Toda a Agenda']], ['Ordens de Serviço', ['Criar OS', 'Editar OS']], ['Clientes e Fornecedores', ['Criar Cliente', 'Editar Cliente']]]) {
    await t(`seta ${tela}`, () => page.getByRole('button', { name: `Ver ações de ${tela}` }).click());
    await ms(300);
    for (const a of acoes) await t(`liga ${a}`, () => page.getByRole('switch', { name: a, exact: true }).click());
    await t(`fecha seta ${tela}`, () => page.getByRole('button', { name: `Ver ações de ${tela}` }).click());
  }
  await ms(300);
  log('contadores:', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('[role=dialog] .tabular-nums')].map((e) => e.textContent.trim()))));
  await shot('c04-d-tudo-ligado');
  await t('Criar Cargo (2)', () => page.getByRole('button', { name: 'Criar Cargo' }).click());
  await ms(1500);
  await shot('c04-e-lista');
  log('lista final:', JSON.stringify((await page.locator('[role=dialog]').innerText()).split('\n').map((l) => l.trim()).filter(Boolean)));
  log('botões da lista final:', JSON.stringify(await geom(page, '[role=dialog] button')));
  log('banco:', JSON.stringify(await (await fetch(process.env.FAKE_URL + '/__dev/state?table=permission_presets')).json()).slice(0, 1500));
};
