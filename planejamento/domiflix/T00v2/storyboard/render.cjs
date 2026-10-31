// Renderiza a folha do storyboard (storyboard.html + cenas.json) em PNG.
// uso: node render.cjs 16x9 ../storyboard_16x9.png [--so 2,7,15]
//      node render.cjs 9x16 ../storyboard_9x16.png
// Pesado: rodar sob a trava (flock "$TUT_HOME/.heavy.lock" nice -n 10 node render.cjs ...).
// Ícones (lucide-static), fontes e marca vêm da área de trabalho ($TUT_HOME, padrão ~/domiflix), embutidos como data URI.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os');
const HERE = __dirname;
const TUT = process.env.TUT_HOME || path.join(os.homedir(), 'domiflix');
const [fmt, saida] = process.argv.slice(2);
const opt = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const SO = opt('--so', null);

const ICONES = ['play', 'check', 'circle-check', 'x', 'graduation-cap', 'layers', 'bell-ring', 'headset', 'circle-help', 'user-round',
  'users', 'credit-card', 'clipboard-list', 'phone-call', 'hard-hat', 'banknote', 'arrow-right', 'arrow-down', 'sparkles', 'flag',
  'file-text', 'trending-up', 'file-signature', 'receipt', 'palette', 'video', 'monitor', 'smartphone', 'zoom-in', 'plus', 'minus',
  'clock', 'target', 'badge-check', 'circle-play', 'hourglass'];
const uri = (f, tipo) => `data:${tipo};base64,${fs.readFileSync(f).toString('base64')}`;

(async () => {
  const dados = JSON.parse(fs.readFileSync(path.join(HERE, 'cenas.json'), 'utf8'));
  const lucide = path.join(TUT, 't0/edit/cenas/node_modules/lucide-static/icons');
  dados.icones = {};
  for (const n of ICONES) {
    dados.icones[n] = fs.readFileSync(path.join(lucide, n + '.svg'), 'utf8').replace(/<!--[\s\S]*?-->/g, '')
      .replace(/width="24"/, '').replace(/height="24"/, '').replace(/stroke-width="2"/, 'stroke-width="2.2"');
  }
  const M = path.join(TUT, 'marca/assets');
  dados.imagens = {
    helmet_green: uri(path.join(M, 'helmet_green.png'), 'image/png'),
    logo_h_light: uri(path.join(M, 'logo_h_light.png'), 'image/png'),
    wordmark_light: uri(path.join(M, 'wordmark_light.png'), 'image/png'),
    domiflix_branco: uri(path.join(TUT, 'src-1.38.9/src/assets/domiflix-logo-horizontal-branco.png'), 'image/png'),
  };
  const fontes = [500, 600, 700, 800].map(w => `@font-face{font-family:M;font-weight:${w};src:url(${uri(path.join(TUT,
    `web/fonts/montserrat-latin-${w}-normal.woff2`), 'font/woff2')}) format('woff2')}
    @font-face{font-family:M;font-weight:${w};unicode-range:U+0100-024F;src:url(${uri(path.join(TUT,
    `web/fonts/montserrat-latin-ext-${w}-normal.woff2`), 'font/woff2')}) format('woff2')}`).join('\n');

  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
  await page.route('**/*', r => r.request().url().startsWith('file:') || r.request().url().startsWith('data:') ? r.continue() : r.abort());
  await page.addInitScript(`window.DADOS=${JSON.stringify(dados)};`);
  await page.goto('file://' + path.join(HERE, 'storyboard.html'));
  await page.addStyleTag({ content: fontes });
  await page.evaluate(async () => { for (const w of [500, 600, 700, 800]) await document.fonts.load(`${w} 20px M`); await document.fonts.ready; });
  await page.evaluate(([f, so]) => window.monta(f, so), [fmt, SO ? SO.split(',').map(Number) : null]);
  await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  const dim = await page.evaluate(() => ({ w: document.getElementById('folha').scrollWidth, h: document.body.scrollHeight }));
  await page.setViewportSize({ width: dim.w, height: 800 });
  await page.screenshot({ path: saida, fullPage: true });
  await b.close();
  console.log(`ok ${saida} (${dim.w} px de largura)`);
})();
