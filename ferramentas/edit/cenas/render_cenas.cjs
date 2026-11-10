// Renderiza um capítulo ilustrado (cenas.html) no lugar da gravação de tela: vídeo 2560x1600 a 30 q/s, mesmo formato
// do robô, para o render_chapter.py tratar igual (palco, vinheta, trilha, legendas).
// uso: node render_cenas.cjs <cap> <capNN.json da narração> <saida.mp4> [--cauda 1.2] [--html cenas.html] [--de S --ate S]
//      node render_cenas.cjs <cap> <capNN.json> <pasta> --stills 1.5,6,12.3      (quadros JPEG para conferir)
//      --de/--ate: só esse trecho do relógio da narração (o 1º quadro do vídeo é o instante --de). É o caso da ilustração
//      de conceito no meio de um capítulo gravado: --de = o "at" dela no specs.json, --ate = at + dur.
// A página (padrão: cenas.html ao lado) expõe window.setup(dados) e window.R(t); ícones lucide usados como ic('nome',...)
// são achados sozinhos no HTML (npm i na pasta: lucide-static). Ver docs/09-aula-ilustrada.md.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const HERE = __dirname;
const [cap, tempos, saida] = process.argv.slice(2);
const opt = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const FPS = 30, CAUDA = parseFloat(opt('--cauda', '1.2')), STILLS = opt('--stills', null);
const HTML = path.resolve(opt('--html', path.join(HERE, 'cenas.html')));
const LUCIDE = path.join(path.dirname(require.resolve('lucide-static/package.json', { paths: [HERE, path.dirname(HTML)] })), 'icons');
// ícones: todo texto entre aspas na página que for nome de um ícone do lucide (pega também os que vêm de listas)
const ICONS = [...new Set([...fs.readFileSync(HTML, 'utf8').matchAll(/['"]([a-z][a-z0-9-]{1,40})['"]/g)].map(m => m[1]))]
  .filter(n => fs.existsSync(path.join(LUCIDE, n + '.svg')));

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
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 2 });
  await page.route('**/*', r => r.request().url().startsWith('file:') ? r.continue() : r.abort());
  await page.addInitScript(`window.ICONS=${JSON.stringify(icons)};`);
  await page.goto('file://' + HTML);
  await page.evaluate(async () => { for (const w of [500, 600, 700, 800]) await document.fonts.load(`${w} 20px M`); await document.fonts.ready; });
  await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  await page.evaluate(d => window.setup(d), dados);
  await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  const avisos = []; page.on('console', m => { if (m.type() === 'warning') avisos.push(m.text()); });
  if (STILLS) {
    fs.mkdirSync(saida, { recursive: true });
    for (const s of STILLS.split(',')) {
      const t = parseFloat(s); await page.evaluate(t => window.R(t), t);
      await page.screenshot({ path: path.join(saida, `cap${String(cap).padStart(2, '0')}_${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 90 });
    }
    if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
    await b.close(); return;
  }
  const de = parseFloat(opt('--de', '0')), ate = parseFloat(opt('--ate', String(N.dur + CAUDA)));
  const i0 = Math.round(de * FPS), n = Math.round(ate * FPS) - i0, dur = n / FPS, tmp = saida.replace(/\.mp4$/, '.parcial.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', tmp],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.R(t), (i0 + i) / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log(`cap${cap}: ${i}/${n} quadros (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error('ffmpeg falhou', code); process.exit(1); }
  fs.renameSync(tmp, saida);
  if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
  console.log(`ok ${saida}: ${n} quadros, ${dur.toFixed(2)} s, ${((Date.now() - t0) / 1000).toFixed(0)} s de render`);
})();
