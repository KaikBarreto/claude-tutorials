// Telemetria do mouse e do teclado, no MESMO relogio dos quadros (segundos desde o 1o quadro do video).
// Duas fontes que se completam:
//   - pagina (inpage/telemetry.js): eventos reais como o navegador os viu, ja com o cursor CSS sob o ponteiro e o
//     retangulo do elemento alvo;
//   - robo (Node): cada passo que ele despachou (page.mouse.move etc.). Serve para completar o que a pagina nao ve
//     (iframes, teclas digitadas por insertText).
// O resultado e o telemetry.json que o editor usa para desenhar cursor, zoom e destaques.
import fs from 'node:fs';

const INPAGE = (name) => fs.readFileSync(new URL(`./inpage/${name}`, import.meta.url), 'utf8');
const r1 = (v) => Math.round(v * 10) / 10;
const r3 = (v) => Math.round(v * 1000) / 1000;
const MASK = '•'; // no lugar de qualquer tecla digitada num segredo (senha, valor de "$NOME")

export class Telemetry {
  constructor({ dsf = 2 } = {}) {
    this.dsf = dsf;
    this.fromPage = []; // eventos da pagina (t em ms epoch)
    this.fromNode = []; // passos do robo (t em ms epoch; x/y em px do video)
    this.lastNode = { x: null, y: null };
    this.keyRect = null; // retangulo do campo em que o robo esta digitando (px do video)
    this.clickRect = null; // retangulo do alvo que o robo esta clicando (px do video)
    this.extras = [];
    this.maskSpans = []; // intervalos (ms epoch) em que o robo digitou um segredo
    this.maskFrom = null;
  }

  /** Instala o binding e o observador em todo documento do contexto. */
  async install(context, { overlay = false } = {}) {
    await context.exposeBinding('__recTel', (_source, ev) => {
      if (ev && typeof ev === 'object' && typeof ev.t === 'number') this.fromPage.push(ev);
    });
    await context.addInitScript({ content: INPAGE('telemetry.js') });
    if (overlay) await context.addInitScript({ content: INPAGE('cursor.js') });
  }

  // ---- passos do robo (coordenadas em px CSS; guardamos em px do video) ----
  _v(x, y) {
    return { x: r1(x * this.dsf), y: r1(y * this.dsf) };
  }
  nodeMove(x, y) {
    const p = this._v(x, y);
    if (p.x === this.lastNode.x && p.y === this.lastNode.y) return;
    this.lastNode = p;
    this.fromNode.push({ type: 'move', t: Date.now(), ...p });
  }
  nodeButton(type, x, y, button = 'left') {
    const p = this._v(x, y);
    this.lastNode = p;
    this.fromNode.push({ type, t: Date.now(), ...p, button: button === 'right' ? 2 : button === 'middle' ? 1 : 0, rect: this.clickRect || undefined });
  }
  nodeClick(count, x, y, button = 'left') {
    const p = this._v(x, y);
    this.fromNode.push({ type: count === 2 ? 'dblclick' : 'click', t: Date.now(), ...p, button: button === 'right' ? 2 : 0, rect: this.clickRect || undefined });
  }
  nodeScroll(x, y, dy, dx = 0) {
    const p = this._v(x, y);
    this.fromNode.push({ type: 'scroll', t: Date.now(), ...p, deltaY: r1(dy), deltaX: r1(dx) });
  }
  nodeKey(key, x, y) {
    const p = this._v(x, y);
    this.fromNode.push({ type: 'key', t: Date.now(), ...p, key: this.maskFrom !== null ? MASK : key, rect: this.keyRect || undefined });
  }
  /**
   * Liga/desliga a mascara de teclas: enquanto ligada, o robo registra "•" no lugar da tecla e as teclas que a pagina
   * viu nesse intervalo tambem saem como "•" (ver finalize). Serve para texto vindo de "$NOME" e para campos de senha.
   */
  maskKeys(on) {
    if (on && this.maskFrom === null) this.maskFrom = Date.now();
    else if (!on && this.maskFrom !== null) {
      this.maskSpans.push({ from: this.maskFrom, to: Date.now() });
      this.maskFrom = null;
    }
  }
  /** Retangulo (px CSS) do campo que recebe a digitacao; vira o `rect` das teclas que a pagina nao enxergar. */
  setKeyTarget(boxCss) {
    this.keyRect = boxCss ? { x: r1(boxCss.x * this.dsf), y: r1(boxCss.y * this.dsf), w: r1(boxCss.width * this.dsf), h: r1(boxCss.height * this.dsf) } : null;
  }
  /** Retangulo (px CSS) do alvo que o robo vai clicar; completa o `rect` quando a pagina nao enxerga o elemento (iframe, menu que fecha). */
  setClickTarget(boxCss) {
    this.clickRect = boxCss ? { x: r1(boxCss.x * this.dsf), y: r1(boxCss.y * this.dsf), w: r1(boxCss.width * this.dsf), h: r1(boxCss.height * this.dsf) } : null;
  }
  /** Amostra manual (ex.: posicao inicial do ponteiro em t=0). */
  addExtra(sample) {
    this.extras.push(sample);
  }

  /**
   * Junta as duas fontes. `t0Ms` = instante (epoch ms) do 1o quadro; `endS` = duracao do video.
   * Amostras fora do video sao descartadas.
   */
  finalize({ t0Ms, endS }) {
    if (this.maskFrom !== null) this.maskKeys(false);
    // teclas que a pagina viu enquanto o robo digitava um segredo: viram "•" (sem code nem modificadores) ANTES de casar
    // com as do robo, que ja saem mascaradas — assim as duas fontes continuam se reconhecendo e nada vaza
    const masked = (s) => {
      if (s.type !== 'key' || !this.maskSpans.some((m) => s.t >= m.from - 30 && s.t <= m.to + 30)) return s;
      const { code, shift, ctrl, alt, meta, ...rest } = s;
      return { ...rest, key: MASK };
    };
    const page = this.fromPage.map(masked).sort((a, b) => a.t - b.t);
    const node = [...this.fromNode].sort((a, b) => a.t - b.t);
    const used = new Set();
    const tol = this.dsf + 0.6; // eventos de mouse da pagina chegam com px CSS inteiros: erro de ate 1 px CSS = dsf px de video
    const sameSpot = (a, b) => Math.abs(a.x - b.x) <= tol && Math.abs(a.y - b.y) <= tol;
    const close = (a, b) => b.t >= a.t - 25 && b.t <= a.t + 400;

    const extra = [];
    let lastKind = 'arrow';
    let pi = 0;
    for (const n of node) {
      // acha na pagina o evento equivalente (mesmo tipo, mesmo lugar, logo depois do despacho)
      while (pi < page.length && page[pi].t < n.t - 400) pi++;
      let hit = -1;
      for (let i = pi; i < page.length && page[i].t <= n.t + 400; i++) {
        const p = page[i];
        if (used.has(i) || p.type !== n.type || !close(n, p)) continue;
        // rolagem: casa tambem pelo delta (a pagina pode nao ver rodas que caem sobre um iframe, e sem o delta um evento
        // "perdido" roubaria o da roda seguinte e a roda ja vista seria contada duas vezes)
        if (n.type === 'key' ? p.key === n.key : n.type === 'scroll' ? sameSpot(n, p) && Math.abs(p.deltaY - n.deltaY) <= 1 : sameSpot(n, p)) {
          hit = i;
          break;
        }
      }
      if (hit >= 0) {
        used.add(hit);
        if (page[hit].cursor) lastKind = page[hit].cursor;
        if (n.rect && !page[hit].rect) page[hit].rect = n.rect;
        continue;
      }
      const s = { ...n, src: 'runner' };
      if (n.type === 'move') s.cursor = lastKind;
      extra.push(s);
    }

    // O Chrome pode juntar varias rodas seguidas num unico `wheel` (soma dos deltas). Esse evento da pagina ficou sem
    // par; se uma sequencia de rodas do robo (ainda "sem par") soma o mesmo delta, ela ja esta contada nele.
    page.forEach((p, i) => {
      if (p.type !== 'scroll' || used.has(i)) return;
      const cand = extra.filter((e) => e.type === 'scroll');
      for (let s = 0; s < cand.length; s++) {
        let sum = 0;
        for (let e = s; e < Math.min(cand.length, s + 8); e++) {
          if (!sameSpot(cand[e], p)) break;
          sum += cand[e].deltaY;
          if (Math.abs(sum - p.deltaY) <= 1 && e > s && p.t >= cand[s].t - 25 && p.t <= cand[e].t + 400) {
            for (let k = s; k <= e; k++) extra.splice(extra.indexOf(cand[k]), 1);
            used.add(i);
            return;
          }
          if (Math.abs(sum) > Math.abs(p.deltaY) + 1) break;
        }
      }
    });

    const all = [...page, ...extra, ...this.extras].sort((a, b) => a.t - b.t);
    const out = [];
    const counts = {};
    // Documento recem-carregado (navegacao completa, comum fora do SPA da Dominex): a pagina ainda nao viu o ponteiro e
    // manda a tecla com (0, 0), que levaria cursor e camera ao canto. O robo sabe onde o ponteiro esta: a tecla herda a
    // ultima posicao conhecida.
    let pos = null;
    for (const s of all) {
      if (s.type === 'key' && s.x === 0 && s.y === 0 && pos) {
        s.x = pos.x;
        s.y = pos.y;
      } else if (typeof s.x === 'number' && typeof s.y === 'number' && (s.x !== 0 || s.y !== 0)) pos = { x: s.x, y: s.y };
      const t = (s.t - t0Ms) / 1000;
      if (t < -0.02 || t > endS + 0.05) continue;
      const o = { t: r3(Math.max(0, t)), x: s.x, y: s.y, type: s.type };
      if (s.type === 'move') {
        o.cursor = s.cursor || 'arrow';
        if (s.cursorRaw && s.cursorRaw !== 'auto' && s.cursorRaw !== 'default') o.cursorRaw = s.cursorRaw;
      }
      if (s.type === 'down' || s.type === 'up' || s.type === 'click' || s.type === 'dblclick') o.button = s.button ?? 0;
      if (s.kb) o.kb = true; // clique disparado pelo teclado: sem x/y; o editor não move o cursor, só orienta a câmera
      if (s.type === 'scroll') {
        o.deltaY = s.deltaY;
        if (s.deltaX) o.deltaX = s.deltaX;
      }
      if (s.type === 'key') {
        o.key = s.key;
        if (s.code) o.code = s.code;
        for (const m of ['shift', 'ctrl', 'alt', 'meta']) if (s[m]) o[m] = true;
      }
      if (s.rect) o.rect = s.rect;
      if (s.target) o.target = s.target;
      if (s.src) o.src = s.src;
      out.push(o);
      counts[o.type] = (counts[o.type] || 0) + 1;
    }
    // `key` da pagina nao tem rect quando o campo nao esta focado; usa o do robo se existir
    return { samples: out, counts, pageEvents: this.fromPage.length, runnerFilled: extra.length };
  }
}
