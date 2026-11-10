// Renderiza uma cena de Windows (cena_windows.html) no mesmo formato da gravação do robô: MP4 2560x1600 a 30 q/s, sem
// cursor, bt709 faixa TV, + <nome>.telemetry.json (mouse e cliques) + <nome>.actions.json (passos com rótulo, retângulo e
// instante). Assim a montagem trata a cena como um capítulo gravado: render_chapter.py desenha o cursor da skill, a câmera
// mira os cliques e os zooms/destaques do specs.json apontam para os rótulos (docs/10-cena-windows.md).
//
// uso: node cena_windows.cjs <cena.json> <saida.mp4>                       vídeo + telemetria + ações
//      node cena_windows.cjs <cena.json> <pasta> --stills 1.5,6,12.3 [--mira] quadros JPEG para conferir (--mira: ponto do cursor)
//      --cache <pasta> (padrão $CENA_WIN_CACHE ou /dev/shm/cena-windows: fonte da interface, de preparar.sh)
// A cena (JSON) aponta para as capturas do EcoTray (capturar_ecotray.py) e, se houver, para a gravação do robô que entra na
// área da página do navegador (gravada com "device": "windows", 1280x712 CSS, que enche a página na escala 1,5).
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const pw = (() => { for (const c of [process.env.PLAYWRIGHT_MODULE, 'playwright', '/opt/npm-tools/node_modules/playwright']) { try { if (c) return require(c); } catch (e) { /* próximo */ } } throw new Error('Playwright não encontrado (PLAYWRIGHT_MODULE)'); })();
const HERE = __dirname;
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [CENA, SAIDA] = args;
if (!CENA || !SAIDA) { console.error('uso: node cena_windows.cjs <cena.json> <saida.mp4> [--stills t1,t2 --mira]'); process.exit(1); }
const BASE = path.dirname(path.resolve(CENA));
const rel = p => p == null ? p : (path.isAbsolute(p) ? p : path.resolve(BASE, p));
const url = p => 'file://' + p.split(path.sep).map(encodeURIComponent).join('/');
const CACHE = opt('--cache', process.env.CENA_WIN_CACHE || '/dev/shm/cena-windows');
const FPS = 30;

function jpegs(stream, onFrame) { // separa os JPEG de um image2pipe (FFD8 ... FFD9)
  let buf = Buffer.alloc(0);
  stream.on('data', d => {
    buf = Buffer.concat([buf, d]);
    for (;;) {
      const s = buf.indexOf(Buffer.from([0xff, 0xd8])); if (s < 0) { buf = Buffer.alloc(0); return; }
      const e = buf.indexOf(Buffer.from([0xff, 0xd9]), s + 2); if (e < 0) { if (s > 0) buf = buf.subarray(s); return; }
      onFrame(buf.subarray(s, e + 2)); buf = buf.subarray(e + 2);
    }
  });
}

class Quadros { // lê a gravação em sequência, já na escala da área da página (px do dispositivo)
  constructor(video, w, h, ini) { this.video = video; this.w = w; this.h = h; this.ini = ini || 0; this.n = -1; this.atual = null; this.fila = []; this.fim = false; this.esperando = null; this.abrir(); }
  abrir() {
    this.p = spawn('ffmpeg', ['-v', 'error', '-ss', String(this.ini), '-i', this.video, '-an', '-vf',
      `fps=${FPS},scale=${this.w}:${this.h}:flags=lanczos:in_range=tv:in_color_matrix=bt709:out_range=pc:out_color_matrix=bt601`,
      '-f', 'image2pipe', '-c:v', 'mjpeg', '-q:v', '2', '-']);
    jpegs(this.p.stdout, f => { this.fila.push(f); if (this.esperando) { const r = this.esperando; this.esperando = null; r(); } });
    this.p.on('close', () => { this.fim = true; if (this.esperando) { const r = this.esperando; this.esperando = null; r(); } });
  }
  async quadro(k) { // k = índice desde o início do trecho; segura o último se a gravação acabar
    while (this.n < k) {
      if (!this.fila.length) { if (this.fim) break; await new Promise(r => { this.esperando = r; }); continue; }
      this.atual = this.fila.shift(); this.n++;
      if (this.fila.length > 90) this.p.stdout.pause(); else this.p.stdout.resume();
    }
    return this.atual;
  }
}

(async () => {
  const spec = JSON.parse(fs.readFileSync(CENA, 'utf8'));
  const capDir = rel(spec.capturas || 'capturas');
  const qj = JSON.parse(fs.readFileSync(path.join(capDir, 'quadros.json'), 'utf8'));
  const tela = spec.tela || qj.tela || [1920, 1200];
  const saidaPx = spec.saida || [2560, Math.round(2560 * tela[1] / tela[0])];
  const dsf = saidaPx[0] / tela[0];
  const nav = spec.navegador || {}; const pag = nav.pagina || {};
  const icone = rel(nav.favicon || spec.icone_app) || (qj.quadros && Object.values(qj.quadros).find(q => q.tipo === 'bandeja') ? path.join(capDir, Object.values(qj.quadros).find(q => q.tipo === 'bandeja').arquivo) : null);
  const kitFontes = path.resolve(HERE, '..', 'kit', 'fonts');
  const cfg = {
    spec, quadros: qj.quadros, tela, dsf, capturas: url(capDir), favicon: icone ? url(icone) : '', icone_app: icone ? url(rel(spec.icone_app) || icone) : '',
    pagina_img: pag.imagem ? url(rel(pag.imagem)) : null, mira: args.includes('--mira'),
    fonte_ui: fs.existsSync(path.join(CACHE, 'web', 'NotoSans.ttf')) ? url(path.join(CACHE, 'web', 'NotoSans.ttf')) : null,
    fontes_extra: [500, 600, 700].map(w => ['Montserrat', url(path.join(kitFontes, `Montserrat-${w}.ttf`)), w]).filter(f => fs.existsSync(decodeURIComponent(f[1].slice(7)))),
    arquivo_download: (spec.download || {}).arquivo, tamanho_download: (spec.download || {}).tamanho, download_vel: (spec.download || {}).velocidade,
    perfil: spec.perfil,
  };
  if (!cfg.fonte_ui) console.warn('AVISO: sem a fonte da interface (rode preparar.sh); usando a do sistema');
  let grav = null;
  if (pag.gravacao) {
    const g = pag.gravacao, tel = JSON.parse(fs.readFileSync(rel(g.telemetria), 'utf8'));
    const ac = g.acoes ? JSON.parse(fs.readFileSync(rel(g.acoes), 'utf8')) : { actions: [] };
    const v = tel.video; const vp = v.viewportCss || { width: v.width / (v.dsf || 2), height: v.height / (v.dsf || 2) };
    cfg.gravacao = { viewport: [vp.width, vp.height], dsf: v.dsf || v.width / vp.width, fps: v.fps || 30, amostras: tel.samples, acoes: ac.actions };
    grav = { video: rel(g.video) };
  }

  const browser = await pw.chromium.launch();
  const page = await browser.newPage({ viewport: { width: tela[0], height: tela[1] }, deviceScaleFactor: dsf });
  const avisos = []; page.on('console', m => { if (['warning', 'error'].includes(m.type())) avisos.push(m.text()); });
  page.on('pageerror', e => avisos.push('ERRO NA PÁGINA: ' + e.message));
  let quadroAtual = null;
  await page.route('**/*', r => {
    const u = r.request().url();
    if (u.startsWith('file:')) return r.continue();
    if (u.startsWith('http://grav.local/') && quadroAtual) return r.fulfill({ status: 200, contentType: 'image/jpeg', body: quadroAtual });
    return r.abort();
  });
  await page.goto(url(path.join(HERE, 'cena_windows.html')));
  const info = await page.evaluate(c => window.setup(c), cfg);
  if (info.erros && info.erros.length) { console.error('ERROS NA CENA:\n  ' + info.erros.join('\n  ')); await browser.close(); process.exit(2); }
  const dur = spec.duracao || 10;

  let leitor = null, carregado = -1;
  async function poeGravacao(k) {
    if (!grav || k == null) return;
    if (!leitor) {
      const box = await page.evaluate(() => { const g = document.querySelector('#grav'); return [g.offsetWidth, g.offsetHeight]; });
      leitor = new Quadros(grav.video, Math.round(box[0] * dsf / 2) * 2, Math.round(box[1] * dsf / 2) * 2, 0);
    }
    if (k === carregado) return;
    quadroAtual = await leitor.quadro(k); carregado = k;
    await page.evaluate(async k => { const g = document.querySelector('#grav'); g.src = `http://grav.local/${k}.jpg`; await g.decode().catch(() => {}); }, k);
  }

  const STILLS = opt('--stills', null);
  if (STILLS) {
    fs.mkdirSync(SAIDA, { recursive: true });
    for (const s of STILLS.split(',')) {
      const t = parseFloat(s); const r = await page.evaluate(t => window.R(t), t); await poeGravacao(r.quadroGrav);
      const f = path.join(SAIDA, `${spec.nome || 'cena'}_${t.toFixed(2)}.jpg`); await page.screenshot({ path: f, type: 'jpeg', quality: 92 });
    }
    if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
    await browser.close(); if (leitor && leitor.p) { leitor.p.stdout.destroy(); leitor.p.kill('SIGKILL'); }
    console.log(`ok: ${STILLS.split(',').length} quadros em ${SAIDA}`); process.exit(0);
  }

  const n = Math.round(dur * FPS), tmp = SAIDA.replace(/\.mp4$/, '.parcial.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-vf', 'scale=in_range=pc:in_color_matrix=bt601:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int+bicubic',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-threads', '2', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-r', String(FPS), '-movflags', '+faststart', tmp],
  { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    const r = await page.evaluate(t => window.R(t), i / FPS); await poeGravacao(r.quadroGrav);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`${spec.nome || 'cena'}: ${i}/${n} quadros (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  if (code !== 0) { await browser.close(); console.error('ffmpeg falhou', code); process.exit(1); }
  fs.renameSync(tmp, SAIDA);
  const ex = await page.evaluate(() => window.exportar());
  await browser.close();
  if (leitor && leitor.p) { leitor.p.stdout.destroy(); leitor.p.kill('SIGKILL'); }  // pausado, o ffmpeg ficaria preso no pipe
  const video = { width: saidaPx[0], height: saidaPx[1], fps: FPS, durationS: dur, dsf, viewportCss: { width: tela[0], height: tela[1] } };
  const base = SAIDA.replace(/\.mp4$/, '');
  const conta = ex.samples.reduce((o, s) => (o[s.type] = (o[s.type] || 0) + 1, o), {});
  fs.writeFileSync(base + '.telemetry.json', JSON.stringify({ video, clock: 't = segundos desde o 1o quadro do video', units: `pixels do video (${saidaPx[0]}x${saidaPx[1]})`,
    cursorKinds: 'arrow|pointer|text', counts: conta, origem: 'cena de Windows (cena_windows.html)', samples: ex.samples }));
  fs.writeFileSync(base + '.actions.json', JSON.stringify({ script: path.resolve(CENA), name: spec.nome || path.basename(base), video,
    clock: 't = segundos desde o 1o quadro do video', actions: ex.actions, marks: [], late: [], pageIssues: [], stats: { frames: n } }, null, 1));
  if (avisos.length) console.log('AVISOS:', [...new Set(avisos)].join(' | '));
  console.log(`ok ${SAIDA}: ${n} quadros, ${dur.toFixed(2)} s, ${((Date.now() - t0) / 1000).toFixed(0)} s de render; ${ex.actions.length} passos com rótulo, ${conta.click || 0} cliques`);
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
