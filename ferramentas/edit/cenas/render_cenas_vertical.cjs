// Renderiza um capítulo ilustrado do formato VERTICAL 9:16 (cenas_vertical.html): vídeo 1080x1920 a 30 q/s que já é o QUADRO
// FINAL (palco escuro vertical + painel claro + cena), para o render_chapter_vertical.py e o finish.py --formato 9x16 usarem sem
// recompor. Mesma cadeia de cor da vinheta (JPEG -> x264 sem marcas, lido de volta com explicit=False), então não desbota.
// uso: node render_cenas_vertical.cjs <cap> <capNN.json da narração> <saida.mp4> [--cauda 1.2] [--html cenas_vertical.html]
//        [--de S] [--ate S] [--palco ../assets/fundo_escuro_9x16.png] [--dsf 1]
//        --de/--ate: renderiza só esse trecho do relógio da narração (o 1º quadro do vídeo é o instante --de; no JSON do capítulo
//        use audio_offset = -de). --dsf 2 desenha em 2160x3840 e reduz com ffmpeg (texto mais liso; ~4x mais lento).
//      node render_cenas_vertical.cjs <cap> <capNN.json> <pasta> --stills 1.5,6,12.3 [--guias]      (PNGs; --guias desenha a
//        área segura em magenta e a faixa da legenda do player em laranja)
//      node render_cenas_vertical.cjs <cap> <capNN.json> - --auditar [--passo 0.25] [--de S] [--ate S]
//        confere de 0,25 em 0,25 s tudo o que está visível: texto >= 44 px, caixas dentro da área segura (x 72-1008, y 180-1740),
//        no máximo 2 linhas, nada de texto na faixa da legenda (y 1420-1600). Sai com código 2 se houver ERRO (AVISO não reprova).
//        Exceções deliberadas: data-mini (texto menor), data-linhas="3" (até 3 linhas) no elemento ou num ancestral.
// A página expõe window.setup(dados) e window.R(t); recebe window.FORMATO (formato_9x16.json), window.PALCO (o palco 9x16),
// window.GUIAS e window.ICONS (lucide usados como ic('nome',...), achados sozinhos no HTML; npm i na pasta: lucide-static).
// Ver docs/09-aula-ilustrada.md ("Vertical 9:16"). Rode sob `flock $TUT_HOME/.heavy.lock nice -n 10` (render_todos_vertical.sh faz).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const HERE = __dirname;
const [cap, tempos, saida] = process.argv.slice(2);
const opt = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const has = k => process.argv.includes(k);
const FPS = 30, CAUDA = parseFloat(opt('--cauda', '1.2')), STILLS = opt('--stills', null), DSF = parseFloat(opt('--dsf', '1'));
const HTML = path.resolve(opt('--html', path.join(HERE, 'cenas_vertical.html')));
const PALCO = path.resolve(opt('--palco', path.join(HERE, '..', 'assets', 'fundo_escuro_9x16.png')));
const FORMATO = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'formato_9x16.json'), 'utf8'));
const LUCIDE = path.join(path.dirname(require.resolve('lucide-static/package.json', { paths: [HERE, path.dirname(HTML)] })), 'icons');
if (!fs.existsSync(PALCO)) { console.error(`falta o palco vertical ${PALCO}: rode python3 fundo_escuro_vertical.py`); process.exit(1); }
// ícones: todo texto entre aspas na página que for nome de um ícone do lucide (pega também os que vêm de listas)
const ICONS = [...new Set([...fs.readFileSync(HTML, 'utf8').matchAll(/['"]([a-z][a-z0-9-]{1,40})['"]/g)].map(m => m[1]))]
  .filter(n => fs.existsSync(path.join(LUCIDE, n + '.svg')));

// conferência dentro da página: devolve [{nivel, tipo, msg, txt, caixa}] do que está visível agora
const AUDITA = cfg => {
  const [sx0, sy0, sx1, sy1] = cfg.segura, [fy0, fy1] = cfg.faixa, tol = cfg.tol, out = [];
  const st = document.getElementById('st');
  const visivel = e => { let op = 1; for (let n = e; n && n !== document.body; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; op *= parseFloat(cs.opacity); } return op; };
  const lado = (c) => { const l = []; if (c[0] < sx0 - tol) l.push('esquerda'); if (c[1] < sy0 - tol) l.push('alto'); if (c[2] > sx1 + tol) l.push('direita'); if (c[3] > sy1 + tol) l.push('baixo'); return l; };
  const w = document.createTreeWalker(st, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode());) {
    const txt = n.textContent.replace(/\s+/g, ' ').trim(); if (!txt) continue;
    const pe = n.parentElement; if (visivel(pe) < 0.5) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const rs = [...r.getClientRects()].filter(q => q.width > 1 && q.height > 1); if (!rs.length) continue;
    const c = [Math.min(...rs.map(q => q.left)), Math.min(...rs.map(q => q.top)), Math.max(...rs.map(q => q.right)), Math.max(...rs.map(q => q.bottom))].map(v => Math.round(v));
    const fs = parseFloat(getComputedStyle(pe).fontSize), snip = txt.slice(0, 38);
    const tops = rs.map(q => q.top).sort((a, b) => a - b); let linhas = 1; for (let i = 1; i < tops.length; i++) if (tops[i] - tops[i - 1] > fs * 0.5) linhas++;
    if (fs < cfg.texto_min - 0.01 && !pe.closest('[data-mini]')) out.push({ nivel: 'ERRO', tipo: 'texto pequeno', msg: `${fs.toFixed(1)} px (< ${cfg.texto_min})`, txt: snip, caixa: c });
    const max = pe.closest('[data-linhas]') ? parseInt(pe.closest('[data-linhas]').dataset.linhas, 10) : cfg.linhas_max;
    if (linhas > max) out.push({ nivel: 'ERRO', tipo: 'linhas', msg: `${linhas} linhas (máx. ${max})`, txt: snip, caixa: c });
    const ld = lado(c); if (ld.length) out.push({ nivel: 'ERRO', tipo: 'fora da área segura', msg: ld.join('+'), txt: snip, caixa: c });
    if (c[3] > fy0 && c[1] < fy1) out.push({ nivel: 'AVISO', tipo: 'faixa da legenda', msg: `texto em y ${c[1]}-${c[3]} (faixa ${fy0}-${fy1})`, txt: snip, caixa: c });
  }
  for (const e of st.querySelectorAll('svg,img')) {  // ícones e imagens: só a área segura
    if (e.tagName !== 'IMG' && e.parentElement && e.parentElement.closest('svg')) continue;  // svg dentro de svg: só o de fora
    if (visivel(e) < 0.5) continue;
    const q = e.getBoundingClientRect(); if (q.width < 8 || q.height < 8) continue;
    const c = [q.left, q.top, q.right, q.bottom].map(v => Math.round(v)), ld = lado(c);
    if (ld.length) out.push({ nivel: 'ERRO', tipo: 'fora da área segura', msg: ld.join('+'), txt: `<${e.tagName.toLowerCase()}>`, caixa: c });
  }
  return out;
};

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
  const page = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: DSF });
  await page.route('**/*', r => r.request().url().startsWith('file:') ? r.continue() : r.abort());
  await page.addInitScript(`window.ICONS=${JSON.stringify(icons)};window.FORMATO=${JSON.stringify(FORMATO)};window.PALCO=${JSON.stringify('file://' + PALCO)};window.GUIAS=${has('--guias')};`);
  await page.goto('file://' + HTML);
  await page.evaluate(async () => { for (const w of [500, 600, 700, 800]) await document.fonts.load(`${w} 20px M`); await document.fonts.ready; });
  const imgs = async () => page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  await imgs();
  await page.evaluate(d => window.setup(d), dados);
  await imgs();
  await page.evaluate(async () => { await new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = window.PALCO; }); });  // o palco carregado antes do 1º quadro
  const avisos = []; page.on('console', m => { if (m.type() === 'warning') avisos.push(m.text()); });
  const de = parseFloat(opt('--de', '0')), ate = parseFloat(opt('--ate', String(N.dur + CAUDA)));

  if (has('--auditar')) {
    const passo = parseFloat(opt('--passo', '0.25')), vistos = new Map(); let nt = 0;
    const cfg = { segura: [FORMATO.segura.x0, FORMATO.segura.y0, FORMATO.segura.x1, FORMATO.segura.y1], faixa: [FORMATO.legenda_faixa.y0, FORMATO.legenda_faixa.y1],
      texto_min: FORMATO.texto_min, linhas_max: FORMATO.linhas_max, tol: 12 };
    for (let t = de; t <= ate + 1e-6; t += passo, nt++) {
      await page.evaluate(t => window.R(t), t);
      for (const o of await page.evaluate(AUDITA, cfg)) {
        const k = `${o.nivel}|${o.tipo}|${o.txt}`, v = vistos.get(k);
        if (v) { v.fim = t; v.n++; } else vistos.set(k, { ...o, ini: t, fim: t, n: 1 });
      }
    }
    const lista = [...vistos.values()].sort((a, c) => (a.nivel === 'ERRO' ? 0 : 1) - (c.nivel === 'ERRO' ? 0 : 1) || a.ini - c.ini);
    for (const o of lista) console.log(`${o.nivel}  ${o.tipo}: "${o.txt}" ${o.msg}  caixa ${o.caixa.join(',')}  de ${o.ini.toFixed(2)} a ${o.fim.toFixed(2)} s`);
    const erros = lista.filter(o => o.nivel === 'ERRO').length;
    if (avisos.length) console.log('AVISOS da página:', [...new Set(avisos)].join(' | '));
    console.log(`auditoria do cap${cap}: ${nt} instantes, ${erros} erro(s), ${lista.length - erros} aviso(s)`);
    await b.close(); process.exit(erros ? 2 : 0);
  }

  if (STILLS) {
    fs.mkdirSync(saida, { recursive: true });
    for (const s of STILLS.split(',')) {
      const t = parseFloat(s); await page.evaluate(t => window.R(t), t);
      await page.screenshot({ path: path.join(saida, `cap${String(cap).padStart(2, '0')}_${t.toFixed(2)}.png`), type: 'png' });
    }
    if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
    await b.close(); return;
  }

  const i0 = Math.round(de * FPS), n = Math.round(ate * FPS) - i0, tmp = saida.replace(/\.mp4$/, '.parcial.mp4');
  const vf = DSF !== 1 ? ['-vf', 'scale=1080:1920:flags=area'] : [];
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...vf,
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', tmp],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.R(t), (i0 + i) / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 96 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`cap${cap}: ${i}/${n} quadros (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error('ffmpeg falhou', code); process.exit(1); }
  fs.renameSync(tmp, saida);
  if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
  console.log(`ok ${saida}: ${n} quadros, ${(n / FPS).toFixed(2)} s (relógio da narração ${de.toFixed(2)} a ${ate.toFixed(2)}), ${((Date.now() - t0) / 1000).toFixed(0)} s de render`);
})();
