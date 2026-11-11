// Cópia do ferramentas/edit/cenas/render_cenas.cjs para o PILOTO 3D (T07 cap06, 11/11). O original não muda.
// Diferenças:
//  - Chromium com --allow-file-access-from-files: sem ela o import de módulo ES em file:// cai no CORS (origem "null") e
//    o three.module.min.js não carrega. O WebGL em si já funciona sem flag (SwiftShader); --enable-unsafe-swiftshader e
//    --ignore-gpu-blocklist só garantem o mesmo caminho em máquina sem GPU.
//  - --dsf N: escala do dispositivo (padrão 2 = 2560x1600, igual ao original); 1 = 1280x800 para conferência rápida.
//  - mede o tempo de cada quadro (R + captura) e imprime média/mín/máx; ignora os avisos de driver do WebGL.
//  - fontes e ícones achados pela posição do script (raiz do repositório = ../../../..).
// uso: node render_cenas3d.cjs <cap> <capNN.json> <saida.mp4> [--html cena3d.html] [--de S --ate S] [--dsf 2]
//      node render_cenas3d.cjs <cap> <capNN.json> <pasta> --stills 1.5,6,12.3 [--dsf 2]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const HERE = __dirname, RAIZ = path.resolve(HERE, '../../../..');
const [cap, tempos, saida] = process.argv.slice(2);
const opt = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const FPS = 30, CAUDA = parseFloat(opt('--cauda', '1.2')), STILLS = opt('--stills', null), DSF = parseFloat(opt('--dsf', '2'));
if (process.argv.includes('--stills') && !(STILLS || '').trim()) { console.error('render_cenas3d: --stills sem instantes'); process.exit(2); }
const HTML = path.resolve(opt('--html', path.join(HERE, 'cena3d.html')));
const LUCIDE = path.join(path.dirname(require.resolve('lucide-static/package.json',
  { paths: [HERE, path.dirname(HTML), path.join(RAIZ, 'ferramentas/edit/cenas')] })), 'icons');
const ICONS = [...new Set([...fs.readFileSync(HTML, 'utf8').matchAll(/['"]([a-z][a-z0-9-]{0,40})['"]/g)].map(m => m[1]))]
  .filter(n => fs.existsSync(path.join(LUCIDE, n + '.svg')));
const VIGIA_S = parseFloat(opt('--vigia', '90'));
let vigia = null;
const vivo = () => {
  clearTimeout(vigia);
  vigia = setTimeout(() => { console.error(`render_cenas3d: nada andou em ${VIGIA_S} s (cena travada?); saindo`); process.exit(3); }, VIGIA_S * 1000);
  vigia.unref();
};
vivo();
const ms = a => { const s = [...a].sort((x, y) => x - y); return `média ${(a.reduce((x, y) => x + y, 0) / a.length).toFixed(0)} ms, mín ${s[0].toFixed(0)}, máx ${s[s.length - 1].toFixed(0)}`; };

(async () => {
  const N = JSON.parse(fs.readFileSync(tempos, 'utf8'));
  const dados = { cap: parseInt(cap, 10), dur: N.dur, words: N.words.map(w => ({ w: w.w, linha: w.linha, s: w.s, e: w.e })),
    linhas: (N.linhas || []).map(l => ({ i: l.i, s: l.s, e: l.e })) };
  const icons = {};
  for (const n of ICONS) {
    const f = path.join(LUCIDE, n + '.svg');
    icons[n] = fs.readFileSync(f, 'utf8').replace(/<!--[\s\S]*?-->/g, '').replace(/width="24"/, '').replace(/height="24"/, '')
      .replace(/stroke-width="2"/, 'stroke-width="2.1"');
  }
  const b = await chromium.launch({ args: ['--allow-file-access-from-files', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await b.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: DSF });
  const erros = []; page.on('pageerror', e => erros.push(String(e)));
  await page.route('**/*', r => r.request().url().startsWith('file:') ? r.continue() : r.abort());
  await page.addInitScript(`window.ICONS=${JSON.stringify(icons)};`);
  const tc = Date.now();
  await page.goto('file://' + HTML + (opt('--qs', '') ? '?' + opt('--qs', '') : ''));   // --qs 'aa=0&sm=1024': variantes de custo
  await page.evaluate(async dir => {
    for (const w of [500, 600, 700, 800]) {
      let ok = false;
      try { ok = (await document.fonts.load(`${w} 20px M`)).some(f => f.status === 'loaded'); } catch (e) { ok = false; }
      if (!ok) document.fonts.add(await new FontFace('M', `url("file://${dir}/montserrat-latin-${w}-normal.woff2")`, { weight: String(w) }).load());
    }
    await document.fonts.ready;
  }, path.join(RAIZ, 'ferramentas/web/fonts'));
  vivo();
  if (!(await page.evaluate(() => typeof window.setup === 'function'))) {
    console.error('render_cenas3d: a página não expôs window.setup', erros.join(' | ')); process.exit(1);
  }
  await page.evaluate(d => window.setup(d), dados);
  vivo();
  console.log(`setup (carga + montagem + compilação dos shaders): ${((Date.now() - tc) / 1000).toFixed(1)} s`);
  const avisos = []; page.on('console', m => { if (m.type() === 'warning' && !/WebGL-|GL Driver|GPU stall/.test(m.text())) avisos.push(m.text()); });
  const tR = [], tS = [];
  if (STILLS) {
    fs.mkdirSync(saida, { recursive: true });
    for (const s of STILLS.split(',')) {
      const t = parseFloat(s);
      const a = Date.now(); await page.evaluate(t => window.R(t), t); const m = Date.now();
      await page.screenshot({ path: path.join(saida, `cap${String(cap).padStart(2, '0')}_${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 90 });
      tR.push(m - a); tS.push(Date.now() - m);
      vivo();
    }
    console.log(`quadros ${tR.length} a ${1280 * DSF}x${800 * DSF}: R(t) ${ms(tR)} | captura ${ms(tS)} | total ${ms(tR.map((x, i) => x + tS[i]))}`);
    if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
    if (erros.length) console.log('ERROS:', [...new Set(erros)].join(' | '));
    await b.close(); return;
  }
  const de = parseFloat(opt('--de', '0')), ate = parseFloat(opt('--ate', String(N.dur + CAUDA)));
  const i0 = Math.round(de * FPS), n = Math.round(ate * FPS) - i0, dur = n / FPS, tmp = saida.replace(/\.mp4$/, '.parcial.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', tmp],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    const a = Date.now(); await page.evaluate(t => window.R(t), (i0 + i) / FPS); const m = Date.now();
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    tR.push(m - a); tS.push(Date.now() - m);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    vivo();
    if (i % 150 === 0) console.log(`cap${cap}: ${i}/${n} quadros (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error('ffmpeg falhou', code); process.exit(1); }
  fs.renameSync(tmp, saida);
  if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
  if (erros.length) console.log('ERROS:', [...new Set(erros)].join(' | '));
  console.log(`quadros a ${1280 * DSF}x${800 * DSF}: R(t) ${ms(tR)} | captura ${ms(tS)}`);
  console.log(`ok ${saida}: ${n} quadros, ${dur.toFixed(2)} s, ${((Date.now() - t0) / 1000).toFixed(0)} s de render`);
})();
