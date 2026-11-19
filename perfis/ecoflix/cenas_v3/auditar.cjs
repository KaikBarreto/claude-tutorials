// Kit v3 · verificação automática de acabamento: roda a cena em N instantes e chama window.auditar(t) (motor.js) em cada
// um. Acusa texto que não cabe na caixa, conteúdo parado cortado pela borda (margem de 40 px em 1280x800), conteúdo em
// cima do título, seta ou caixa com respiro abaixo do mínimo, sobreposição e quase-alinhamento. Sai com 1 se achar algo.
// uso (a aula inteira, pelas janelas do ilustracoes.json; tempos da fala em $TUT_HOME/tNN/narracao ou --tempos <pasta>):
//   node perfis/ecoflix/cenas_v3/auditar.cjs --aula planejamento/ecoflix/T08 [--id ilu01_quando_usar] [--passo 0.5]
// uso (um capítulo ou um trecho):
//   node perfis/ecoflix/cenas_v3/auditar.cjs <cena.html> <cap> <capNN.json> [--de S --ate S] [--passo 0.5]
// uso (página sem fala, ex.: a vitrine): node .../auditar.cjs vitrine.html 1 - --t 9 --dados '{"pagina":6}'
// --quadros <pasta>: grava um JPEG 1280x800 do primeiro instante de cada problema, com o problema marcado em vermelho.
// --lista: imprime todo instante de cada problema (o padrão junta: primeiro instante, último e quantas vezes).
// Não usa a trava nem captura vídeo (leve: ~0,2 s por instante); rode com nice -n 19 se houver robô gravando.
// --larg N: largura do desenho (1280 = 16:10; 1422 = 16:9). A altura é sempre 800.
const LARG = (() => { const i = process.argv.indexOf('--larg'); return i > 0 ? Number(process.argv[i + 1]) : 1280; })();
const fs = require('fs'), path = require('path');
const AQUI = __dirname, RAIZ = path.resolve(AQUI, '../../..'), CENAS = path.join(RAIZ, 'ferramentas/edit/cenas');
const { chromium } = require(require.resolve('playwright', { paths: [CENAS] }));
const arg = process.argv.slice(2), opt = (k, d) => { const i = arg.indexOf(k); return i >= 0 ? arg[i + 1] : d; }, tem = k => arg.includes(k);
const PASSO = parseFloat(opt('--passo', '0.5')), QUADROS = opt('--quadros', null);
const norm = w => w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%./-]+/g, '');
function palavra(N, [linha, p, n = 1], campo) {   // a mesma busca do W() do motor
  const alvo = norm(p); let k = 0;
  for (const w of N.words) if (w.linha === linha && norm(w.w).replace(/[.,:]$/, '') === alvo && ++k === n) return w[campo];
  k = 0; for (const w of N.words) if (w.linha === linha && norm(w.w).startsWith(alvo) && ++k >= n) return w[campo];
  throw new Error(`âncora não achada na fala: linha ${linha}, "${p}" (${n})`);
}
const lerN = f => JSON.parse(fs.readFileSync(f, 'utf8'));
// as rodadas: [{ html, cap, N (tempos), nome, instantes }]
const rodadas = [];
const instantes = (de, ate) => { const L = []; for (let t = de; t < ate - 1e-6; t += PASSO) L.push(+t.toFixed(3)); L.push(+ate.toFixed(3)); return L; };
if (tem('--aula')) {
  const aula = path.resolve(opt('--aula')), nn = path.basename(aula).toLowerCase(), so = opt('--id', null);
  const tdir = opt('--tempos', null) || [path.join(process.env.TUT_HOME || path.resolve(RAIZ, '../ecoflix'), nn, 'narracao'), path.join(aula, 'cenas/tempos')].find(d => fs.existsSync(path.join(d, 'cap00.json')) || fs.existsSync(d));
  for (const it of lerN(path.join(aula, 'cenas/ilustracoes.json'))) {
    if (!it.v3 || !/\.html$/.test(it.v3) || (so && it.id !== so)) continue;
    const N = lerN(path.join(tdir, `cap${String(it.cap).padStart(2, '0')}.json`));
    for (const j of it.janelas || [it]) { const de = palavra(N, j.de, 's'), ate = palavra(N, j.ate, 'e') + (j.cauda ?? it.cauda ?? .6);
      rodadas.push({ html: path.resolve(aula, it.v3), cap: it.cap, N, anexo: it.anexo ? 'file://' + path.resolve(process.env.TUT_HOME || '.', it.anexo) : null, nome: it.id + (it.janelas ? ` · janela ${j.janela}` : ''), instantes: instantes(de, ate) }); }
  }
} else {
  const [html, cap, tempos] = arg; if (!html || cap == null) { console.error('uso: node auditar.cjs --aula <pasta da aula> | <cena.html> <cap> <capNN.json | -> [--de S --ate S | --t S,S]'); process.exit(2); }
  const N = tempos && tempos !== '-' ? lerN(tempos) : { dur: 10, words: [], linhas: [] };
  const ts = opt('--t', null), de = parseFloat(opt('--de', '0')), ate = parseFloat(opt('--ate', String(N.dur + .6)));
  rodadas.push({ html: path.resolve(html), cap: parseInt(cap, 10), N, nome: path.basename(html) + ' cap ' + cap, instantes: ts ? ts.split(',').map(Number) : instantes(de, ate) });
}
if (!rodadas.length) { console.error('auditar: nenhuma cena v3 para verificar'); process.exit(2); }
const extra = JSON.parse(opt('--dados', '{}'));
(async () => {
  const LUCIDE = path.join(path.dirname(require.resolve('lucide-static/package.json', { paths: [CENAS] })), 'icons');
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); let total = 0; const resumo = [];
  for (const r of rodadas) {
    const icons = {}; for (const n of new Set([...fs.readFileSync(r.html, 'utf8').matchAll(/['"]([a-z][a-z0-9-]{0,40})['"]/g)].map(m => m[1]))) { const f = path.join(LUCIDE, n + '.svg');
      if (fs.existsSync(f)) icons[n] = fs.readFileSync(f, 'utf8').replace(/<!--[\s\S]*?-->/g, '').replace(/width="24"/, '').replace(/height="24"/, '').replace(/stroke-width="2"/, 'stroke-width="2.1"'); }
    const page = await b.newPage({ viewport: { width: LARG, height: 800 }, deviceScaleFactor: 1 }); const erros = []; page.on('pageerror', e => erros.push(String(e))); page.on('console', m => { if (/palavra não achada/.test(m.text())) erros.push('âncora W() sem palavra na fala: ' + m.text().replace('palavra não achada', '').trim()); });
    await page.route('**/*', q => q.request().url().startsWith('file:') ? q.continue() : q.abort());
    await page.addInitScript(`window.ICONS=${JSON.stringify(icons)};`); await page.goto('file://' + r.html);
    await page.evaluate(async dir => { for (const w of [500, 600, 700, 800]) { let ok = false; try { ok = (await document.fonts.load(`${w} 20px M`)).some(f => f.status === 'loaded'); } catch (e) { ok = false; }
      if (!ok) document.fonts.add(await new FontFace('M', `url("file://${dir}/montserrat-latin-${w}-normal.woff2")`, { weight: String(w) }).load()); } await document.fonts.ready; }, path.join(RAIZ, 'ferramentas/web/fonts'));
    await page.evaluate(d => window.setup(d), { cap: r.cap, dur: r.N.dur, words: r.N.words.map(w => ({ w: w.w, linha: w.linha, s: w.s, e: w.e })), linhas: (r.N.linhas || []).map(l => ({ i: l.i, s: l.s, e: l.e })), anexo: r.anexo, ...extra });
    if (!(await page.evaluate(() => typeof window.auditar === 'function'))) { console.error(`${r.nome}: a página não tem window.auditar (a cena usa o motor.js do kit v3?)`); process.exit(2); }
    const achados = new Map();   // chave → { tipo, msg, ts: [] }
    for (const t of r.instantes) { const P = await page.evaluate(t => window.auditar(t), t);
      for (const p of P) { if (!achados.has(p.chave)) { achados.set(p.chave, { ...p, ts: [] });
          if (QUADROS) { fs.mkdirSync(QUADROS, { recursive: true }); await page.evaluate(t => window.auditar(t, { marca: true }), t);
            await page.screenshot({ path: path.join(QUADROS, `${r.nome.replace(/[^a-z0-9]+/gi, '_')}_${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 85 }); } }
        achados.get(p.chave).ts.push(t); } }
    await page.close();
    console.log(`\n${r.nome} · ${r.instantes.length} instantes de ${r.instantes[0].toFixed(2)} a ${r.instantes[r.instantes.length - 1].toFixed(2)} s: ${achados.size ? achados.size + ' problema(s)' : 'sem problemas'}`);
    for (const a of achados.values()) console.log(`  [${a.tipo}] ${a.msg}\n      ${tem('--lista') ? a.ts.map(t => t.toFixed(2)).join(' ') : `de ${a.ts[0].toFixed(2)} a ${a.ts[a.ts.length - 1].toFixed(2)} s (${a.ts.length} instante${a.ts.length > 1 ? 's' : ''})`}`);
    if (erros.length) { console.log('  ERROS DA PÁGINA: ' + [...new Set(erros)].join(' | ')); total++; }
    total += achados.size; resumo.push(`${r.nome}: ${achados.size}`);
  }
  await b.close();
  console.log(`\nauditar: ${total} problema(s) em ${rodadas.length} janela(s)${total ? '' : ' · aprovado'}`);
  process.exit(total ? 1 : 0);
})();
