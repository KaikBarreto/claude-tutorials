// Renderiza a folha de estilos: node render.cjs [saida.jpg]   (padrão: ../../../../ecoflix/previa_ilustracoes/estilos_10.jpg, 3840x2160, JPEG 92)
// Rodar com nice -n 19. Um painel só, para conferir: node render.cjs saida.jpg estilo06.html
const { chromium } = require('playwright');
const path = require('path');
const saida = process.argv[2] || path.resolve(__dirname, '../../../../ecoflix/previa_ilustracoes/estilos_10.jpg'), um = process.argv[3];
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage({ viewport: um ? { width: 728, height: 880 } : { width: 3840, height: 2160 }, deviceScaleFactor: um ? 2 : 1 });
  pg.on('pageerror', e => console.error('[erro]', e.message)); pg.on('console', m => { if (m.type() === 'error') console.error('[console]', m.text()); });
  await pg.goto('file://' + path.join(__dirname, um || 'folha.html'), { waitUntil: 'domcontentloaded', timeout: 0 });
  await pg.waitForFunction('window.PRONTO === true', null, { timeout: 600000 });
  await pg.waitForTimeout(500);
  await pg.screenshot({ path: saida, type: 'jpeg', quality: 92 });
  await b.close(); console.log('ok', saida);
})().catch(e => { console.error(e); process.exit(1); });
