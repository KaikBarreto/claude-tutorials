// Executa um roteiro de acoes (JSON ou JS) no Dominex real, com o "fator humano", e grava o video.
// Ver rec/README.md para o formato do roteiro. Saidas: <nome>.mp4, <nome>.actions.json, <nome>.telemetry.json,
// <nome>.contact.jpg. O video sai SEM cursor; o editor desenha o cursor a partir da telemetria.
import fs from 'node:fs';
import path from 'node:path';
import { openSession, closeSession, settle, VIEWPORT, SCALE } from './browser.mjs';
import { startCapture } from './capture.mjs';
import { assemble, contactSheet, probeVideo } from './assemble.mjs';
import { makeRng, sleep, planMove, typingDelays, minJerk, clamp } from './human.mjs';
import { APP_URL, APP_ORIGIN, LOCAL_APP_URL, FAKE_URL, resolveMode } from './env.mjs';

const r1 = (v) => Math.round(v * 10) / 10;
const r3 = (v) => Math.round(v * 1000) / 1000;
const toVideoRect = (b) => (b ? { x: r1(b.x * SCALE), y: r1(b.y * SCALE), w: r1(b.width * SCALE), h: r1(b.height * SCALE) } : null);
const toVideoPt = (p) => ({ x: r1(p.x * SCALE), y: r1(p.y * SCALE) });

// ------------------------------------------------------------------------------------------------
// Entrada "humana": mouse e teclado do Playwright, passo a passo, com telemetria do robo.
// ------------------------------------------------------------------------------------------------
class Human {
  constructor(page, tel, rng, { pace = 1, cps = 11 } = {}) {
    this.page = page;
    this.tel = tel;
    this.rng = rng;
    this.pace = pace;
    this.cps = cps;
    this.x = null;
    this.y = null;
    this.moveSteps = 0;
  }

  /** Coloca o ponteiro num ponto sem trajetoria (so antes de gravar). */
  async teleport(x, y) {
    this.tel.nodeMove(x, y);
    await this.page.mouse.move(x, y);
    this.x = x;
    this.y = y;
  }

  /** Move ate (x,y) em passos curtos: curva leve, acelera e desacelera (0,5 a 0,9 s nos deslocamentos grandes). */
  async moveTo(x, y, { pace = this.pace } = {}) {
    if (this.x === null) return this.teleport(x, y);
    const plan = planMove({ x: this.x, y: this.y }, { x, y }, this.rng, { pace });
    const start = performance.now();
    let lx = this.x;
    let ly = this.y;
    for (;;) {
      const el = (performance.now() - start) / 1000;
      const done = el >= plan.duration;
      const p = done ? { x, y } : plan.at(el);
      const px = r1(p.x);
      const py = r1(p.y);
      if (px !== lx || py !== ly) {
        this.tel.nodeMove(px, py);
        await this.page.mouse.move(px, py);
        this.moveSteps++;
        lx = px;
        ly = py;
      }
      if (done) break;
      await sleep(5);
    }
    this.x = x;
    this.y = y;
  }

  /** Clique(s) na posicao atual. count 2 = duplo clique. */
  async press({ button = 'left', count = 1 } = {}) {
    const { x, y } = this;
    for (let i = 1; i <= count; i++) {
      this.tel.nodeButton('down', x, y, button);
      await this.page.mouse.down({ button, clickCount: i });
      await sleep(this.rng.range(55, 115));
      // registra ANTES de enviar: `mouse.up` so retorna quando a pagina termina de tratar o clique (pode levar 1 s numa
      // tela pesada) e o instante do despacho e o que se compara com o relogio da pagina
      this.tel.nodeButton('up', x, y, button);
      this.tel.nodeClick(1, x, y, button);
      if (i === 2) this.tel.nodeClick(2, x, y, button); // o navegador manda click, click e dblclick
      await this.page.mouse.up({ button, clickCount: i });
      if (i < count) await sleep(this.rng.range(70, 120));
    }
  }

  /** Rolagem suave com a roda (minimum-jerk) sobre a posicao atual do ponteiro. */
  async scrollBy(total, { duration, axis = 'y' } = {}) {
    const T = duration ?? clamp(0.45 + Math.abs(total) / 1400, 0.5, 1.7) * this.pace;
    const start = performance.now();
    let sent = 0;
    for (;;) {
      const el = (performance.now() - start) / 1000;
      const done = el >= T;
      const target = Math.round(total * (done ? 1 : minJerk(el / T)));
      const d = target - sent;
      if (d !== 0) {
        if (axis === 'x') {
          this.tel.nodeScroll(this.x ?? 0, this.y ?? 0, 0, d);
          await this.page.mouse.wheel(d, 0);
        } else {
          this.tel.nodeScroll(this.x ?? 0, this.y ?? 0, d);
          await this.page.mouse.wheel(0, d);
        }
        sent += d;
      }
      if (done) break;
      await sleep(10);
    }
  }

  /**
   * Digita caractere a caractere, com ritmo humano. Teclas da camada US (ASCII imprimivel, Enter, Tab) saem como
   * tecla de verdade (keydown/keypress/input/keyup); acentuados (ã, é, ç...) o Playwright nao tem como "apertar",
   * entao entram por insertText (so o evento `input`, igual ao que o navegador gera com tecla morta/IME).
   */
  async type(text, { cps = this.cps } = {}) {
    const delays = typingDelays(text, this.rng, { cps });
    let i = 0;
    for (const ch of text) {
      const key = ch === '\n' ? 'Enter' : ch === '\t' ? 'Tab' : ch;
      this.tel.nodeKey(key, this.x ?? 0, this.y ?? 0);
      if (key === 'Enter' || key === 'Tab' || /^[\x20-\x7e]$/.test(key)) await this.page.keyboard.press(key);
      else await this.page.keyboard.insertText(key);
      await sleep(delays[i++] ?? 90);
    }
  }

  async key(combo) {
    this.tel.nodeKey(combo, this.x ?? 0, this.y ?? 0);
    await this.page.keyboard.press(combo);
  }
}

// ------------------------------------------------------------------------------------------------
// Alvos (locators)
// ------------------------------------------------------------------------------------------------
/**
 * "Novo Cliente" ou { text | role+name(+checked) | selector | placeholder | label | testId | title | alt, hasText, within, nth, exact }.
 * `hasText` filtra pelo texto contido (util em combobox/select do Radix, cujo nome acessivel nao vem do conteudo).
 */
export function locatorFor(page, target) {
  const t = typeof target === 'string' ? { text: target } : target;
  if (!t || typeof t !== 'object') throw new Error('alvo (target) ausente no passo');
  const root = t.within ? page.locator(t.within).first() : page;
  const exact = !!t.exact;
  let loc;
  if (t.selector) loc = root.locator(t.selector);
  else if (t.role) {
    const opts = {};
    if (t.name !== undefined) Object.assign(opts, { name: t.name, exact });
    if (t.checked !== undefined) opts.checked = !!t.checked; // switch/checkbox/radio ligado ou desligado
    loc = root.getByRole(t.role, opts);
  }
  else if (t.placeholder) loc = root.getByPlaceholder(t.placeholder, { exact });
  else if (t.label) loc = root.getByLabel(t.label, { exact });
  else if (t.testId) loc = root.getByTestId(t.testId);
  else if (t.title) loc = root.getByTitle(t.title, { exact });
  else if (t.alt) loc = root.getByAltText(t.alt, { exact });
  else if (t.text !== undefined) loc = root.getByText(t.text, { exact });
  else throw new Error(`alvo sem selector/text/role/placeholder/label: ${JSON.stringify(t)}`);
  if (t.hasText !== undefined) loc = loc.filter({ hasText: t.hasText });
  const raw = loc;
  loc = loc.filter({ visible: true });
  loc = t.nth === 'last' ? loc.last() : loc.nth(Number.isInteger(t.nth) ? t.nth : 0);
  loc.__rec = { target: t, raw }; // para mensagens de erro: quantos elementos casam, visiveis ou nao
  return loc;
}

/**
 * Navegacao interna da SPA (pushState + popstate), sem recarregar o documento: os modulos das rotas ja abertas
 * continuam na memoria, como numa sessao real em uso. So vale com o app ja carregado.
 */
async function spaNavigate(page, url) {
  await page.evaluate((u) => {
    const idx = ((window.history.state && window.history.state.idx) ?? 0) + 1;
    window.history.pushState({ usr: null, key: Math.random().toString(36).slice(2, 10), idx }, '', u);
    window.dispatchEvent(new PopStateEvent('popstate', { state: window.history.state }));
  }, url);
}

const describeTarget = (t) => (typeof t === 'string' ? { text: t } : t);

// ------------------------------------------------------------------------------------------------
// Segredos: no passo `type`, o texto "$NOME" (so isso, o texto inteiro) vira a variavel de ambiente NOME — para usuario e
// senha de conta de DEMONSTRACAO. O valor so existe em memoria na hora de digitar: nunca vai para o log, o actions.json
// nem o telemetry.json (la fica o "$NOME" literal; as teclas saem como "•"). "$$NOME" digita o texto literal "$NOME".
// ------------------------------------------------------------------------------------------------
const SECRET_RE = /^\$([A-Za-z_][A-Za-z0-9_]*)$/;
const ESCAPED_RE = /^\$\$[A-Za-z_][A-Za-z0-9_]*$/;
const secretName = (text) => (typeof text === 'string' ? text.match(SECRET_RE)?.[1] ?? null : null);
const literalText = (text) => (ESCAPED_RE.test(text) ? text.slice(1) : text);

function readSecret(name) {
  const v = process.env[name];
  if (v === undefined) throw new Error(`variavel de ambiente ${name} nao definida (o passo type usa "$${name}"): defina-a antes de gravar, ex.: export ${name}=...`);
  if (v === '') throw new Error(`variavel de ambiente ${name} esta vazia (o passo type usa "$${name}")`);
  return v;
}

/** Variaveis "$NOME" dos passos type do roteiro (setup e steps) que faltam ou estao vazias neste ambiente. */
export function missingEnvVars(script) {
  const found = new Map();
  for (const [key, list] of [['setup', script?.setup], ['steps', script?.steps]]) {
    (list || []).forEach((st, i) => {
      const name = st?.do === 'type' ? secretName(st.text) : null;
      if (!name || process.env[name]) return;
      const m = found.get(name) || { name, empty: process.env[name] === '', where: [] };
      m.where.push(`${key}[${i}]`);
      found.set(name, m);
    });
  }
  return [...found.values()];
}

async function stableBox(loc, timeoutMs) {
  try {
    await loc.waitFor({ state: 'visible', timeout: timeoutMs });
  } catch (e) {
    throw new Error(await explainMissing(loc, timeoutMs, e));
  }
  let box = await loc.boundingBox();
  for (let i = 0; i < 14; i++) {
    await sleep(60);
    const b2 = await loc.boundingBox();
    if (b2 && box && Math.abs(b2.x - box.x) < 0.6 && Math.abs(b2.y - box.y) < 0.6 && Math.abs(b2.width - box.width) < 0.6 && Math.abs(b2.height - box.height) < 0.6) return b2;
    box = b2 ?? box;
  }
  if (!box) throw new Error('alvo sem caixa (nao renderizado)');
  return box;
}

/** Mensagem de erro util quando o alvo nao aparece: o alvo pedido e quantos elementos casam (visiveis ou nao). */
async function explainMissing(loc, timeoutMs, err) {
  const rec = loc.__rec;
  if (!rec) return String(err?.message || err).split('\n')[0];
  let n = null;
  try {
    n = await rec.raw.count();
  } catch (e) {}
  const t = JSON.stringify(rec.target);
  const dica =
    n === 0
      ? ' Nenhum elemento casa: confira o texto/papel (combobox/select do Radix nao tem nome: use { role: "combobox", hasText: "..." }; abas sao role "tab").'
      : n > 0
        ? ` ${n} elemento(s) casam mas nenhum ficou visivel (escondido, fora da tela ou atras de outro?). Use "nth" ou "within" para escolher.`
        : '';
  return `alvo nao encontrado em ${timeoutMs / 1000}s: ${t}.${dica}`;
}

/** Ponto de clique dentro da caixa: perto do centro, com folga humana, sempre dentro do alvo e da janela. */
function pickPoint(box, rng) {
  const mx = Math.min(10, box.width * 0.25);
  const my = Math.min(8, box.height * 0.25);
  const ox = clamp(rng.range(-0.2, 0.2) * box.width, -box.width / 2 + mx, box.width / 2 - mx);
  const oy = clamp(rng.range(-0.18, 0.18) * box.height, -box.height / 2 + my, box.height / 2 - my);
  return {
    x: clamp(box.x + box.width / 2 + ox, 2, VIEWPORT.width - 2),
    y: clamp(box.y + box.height / 2 + oy, 2, VIEWPORT.height - 2),
  };
}

// ------------------------------------------------------------------------------------------------
// Passos
// ------------------------------------------------------------------------------------------------
async function scrollContainerCenter(loc) {
  return loc.evaluate((el) => {
    let n = el.parentElement;
    while (n && n !== document.documentElement) {
      const s = getComputedStyle(n);
      if (/(auto|scroll)/.test(s.overflowY) && n.scrollHeight > n.clientHeight + 4) {
        const b = n.getBoundingClientRect();
        return { x: b.left + b.width / 2, y: b.top + b.height / 2 };
      }
      n = n.parentElement;
    }
    return { x: window.innerWidth / 2, y: window.innerHeight / 2 };
  });
}

/**
 * Retangulo do alvo e a parte dele que realmente aparece (intersecao com os ancestrais que cortam: overflow
 * auto/scroll/hidden/clip), mais o container com rolagem mais proximo em cada eixo.
 */
async function clipInfo(loc) {
  return loc.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const vis = { l: Math.max(0, r.left), t: Math.max(0, r.top), r: Math.min(innerWidth, r.right), b: Math.min(innerHeight, r.bottom) };
    let sy = null;
    let sx = null;
    for (let n = el.parentElement; n && n !== document.documentElement; n = n.parentElement) {
      const s = getComputedStyle(n);
      const cy = /(auto|scroll|hidden|clip)/.test(s.overflowY);
      const cx = /(auto|scroll|hidden|clip)/.test(s.overflowX);
      if (!cx && !cy) continue;
      const b = n.getBoundingClientRect();
      if (cy) {
        vis.t = Math.max(vis.t, b.top);
        vis.b = Math.min(vis.b, b.bottom);
      }
      if (cx) {
        vis.l = Math.max(vis.l, b.left);
        vis.r = Math.min(vis.r, b.right);
      }
      if (!sy && /(auto|scroll)/.test(s.overflowY) && n.scrollHeight > n.clientHeight + 4) sy = { x: b.left + b.width / 2, y: b.top + b.height / 2 };
      if (!sx && /(auto|scroll)/.test(s.overflowX) && n.scrollWidth > n.clientWidth + 4) sx = { x: b.left + b.width / 2, y: b.top + b.height / 2 };
    }
    return { rect: { x: r.left, y: r.top, w: r.width, h: r.height }, vis, sy, sx };
  });
}

/** Rola (com a roda, como uma pessoa) ate o alvo ficar na parte util da janela e fora de qualquer corte de container. */
async function ensureVisible(ctx, loc, box, timeoutMs) {
  const top = 96;
  const bottom = VIEWPORT.height - 70;
  for (let i = 0; i < 6; i++) {
    const cx = box.x + box.width / 2;
    const cy = box.y + box.height / 2;
    const info = await clipInfo(loc).catch(() => null);
    const inViewport = cy >= top && cy <= bottom && box.x + box.width > 0 && box.x < VIEWPORT.width;
    // corte por container (lista rolada, janela com rolagem, faixa de abas): o centro tem de estar na parte que aparece
    const mY = Math.min(6, box.height / 4);
    const mX = Math.min(6, box.width / 4);
    const clippedY = !!info && (cy < info.vis.t + mY || cy > info.vis.b - mY);
    const clippedX = !!info && (cx < info.vis.l + mX || cx > info.vis.r - mX);
    if (inViewport && !clippedY && !clippedX) return box;
    if (clippedX && !clippedY && info.sx) {
      // faixa horizontal (abas): leva o alvo ao centro do container
      await ctx.h.moveTo(info.sx.x, info.sx.y);
      await ctx.h.scrollBy(cx - info.sx.x, { axis: 'x' });
    } else if (clippedY && info.sy) {
      await ctx.h.moveTo(info.sy.x, info.sy.y);
      await ctx.h.scrollBy(cy - info.sy.y);
    } else {
      const c = await scrollContainerCenter(loc);
      await ctx.h.moveTo(c.x, c.y);
      await ctx.h.scrollBy(cy - (top + bottom) / 2);
    }
    await sleep(260);
    box = await stableBox(loc, timeoutMs);
  }
  return box;
}

async function moveToTarget(ctx, step, { allowScroll = true } = {}) {
  const timeoutMs = (step.timeout ?? ctx.script.timeout ?? 12) * 1000;
  const loc = locatorFor(ctx.page, step.target);
  let box = await stableBox(loc, timeoutMs);
  if (allowScroll && !step.noScroll) box = await ensureVisible(ctx, loc, box, timeoutMs); // noScroll: alvo fixo fora da faixa 96..altura-70 (cabeçalho/barra de baixo do celular): sem rolar à toa (~6 s)
  let pt = pickPoint(box, ctx.rng);
  await ctx.h.moveTo(pt.x, pt.y);
  // confere se o alvo continua onde estava (animacao/layout) e se e ele que esta sob o ponteiro
  const b2 = await loc.boundingBox().catch(() => null);
  if (b2 && (Math.abs(b2.x - box.x) > 2 || Math.abs(b2.y - box.y) > 2)) {
    box = b2;
    pt = pickPoint(box, ctx.rng);
    await ctx.h.moveTo(pt.x, pt.y);
  }
  const hit = await loc
    .evaluate((el, [x, y]) => {
      const h = document.elementFromPoint(x, y);
      return !!h && (el.contains(h) || h.contains(el));
    }, [pt.x, pt.y])
    .catch(() => true);
  const warn = hit ? null : 'ponteiro nao esta sobre o alvo (algo por cima?)';
  return { loc, box, pt, warn };
}

const dwell = (ctx, lo = 0.11, hi = 0.24) => sleep(ctx.rng.range(lo, hi) * 1000 * ctx.h.pace);

// Diagnostico de um "assentar" que estourou o tempo: o que ainda estava em voo e ha quanto tempo nao havia rede nova.
const notSettled = (session) => ({
  settled: false,
  pending: [...session.diag.inflight].slice(0, 4).map((r) => `${r.method()} ${r.url().replace(/^https?:\/\/[^/]+/, '').slice(0, 90)}`),
  inflight: session.diag.inflight.size,
  quietMs: Date.now() - session.diag.lastNet,
});

const STEPS = {
  async goto(ctx, step) {
    const url = new URL(step.url, APP_URL);
    const route = url.pathname + url.search + url.hash;
    // com o app ja carregado a troca de rota e interna (sem recarregar, modulos das rotas aquecidas ficam na memoria);
    // `reload: true` forca carregar o documento de novo. So no fakebase (roteador da Dominex): num app qualquer (modo url)
    // o pushState nao e ouvido e a tela nao mudaria, entao o padrao la e carregar o documento; `spa: true` pede a interna
    if (ctx.appLoaded && !step.reload && (ctx.spaNav || step.spa)) {
      await spaNavigate(ctx.page, route);
      const ok = await settle(ctx.session, { quietMs: 500, timeoutMs: 25000 });
      await sleep(step.after ?? 200);
      return { url: step.url, spa: true, ...(ok ? {} : notSettled(ctx.session)) };
    }
    const t0 = Date.now();
    await ctx.page.goto(url.href, { waitUntil: 'load', timeout: 60000 });
    const loadMs = Date.now() - t0;
    ctx.appLoaded = true;
    const ok = await settle(ctx.session, { quietMs: 700, timeoutMs: 25000 });
    await sleep(step.after ?? 250);
    return { url: step.url, loadMs, ...(ok ? {} : notSettled(ctx.session)) };
  },

  async click(ctx, step) {
    const { box, pt, warn } = await moveToTarget(ctx, step);
    await dwell(ctx);
    const tAct = ctx.T();
    ctx.tel.setClickTarget(box);
    await ctx.h.press({ button: step.button || 'left', count: step.count || 1 });
    ctx.tel.setClickTarget(null);
    return { target: describeTarget(step.target), rect: toVideoRect(box), point: toVideoPt(pt), tAct: r3(tAct), warn };
  },
  async dblclick(ctx, step) {
    return STEPS.click(ctx, { ...step, count: 2 });
  },
  async rightclick(ctx, step) {
    return STEPS.click(ctx, { ...step, button: 'right' });
  },

  async hover(ctx, step) {
    const { box, pt, warn } = await moveToTarget(ctx, step);
    const tAct = ctx.T();
    await sleep((step.seconds ?? 0.9) * 1000);
    return { target: describeTarget(step.target), rect: toVideoRect(box), point: toVideoPt(pt), tAct: r3(tAct), warn };
  },

  async type(ctx, step) {
    const ref = secretName(step.text); // "$NOME" -> variavel de ambiente NOME (so em memoria; ver "Segredos" acima)
    const text = ref ? readSecret(ref) : literalText(String(step.text ?? ''));
    if (ref) ctx.secrets.set(ref, text);
    let out = {};
    let box = null;
    if (step.target && !step.noClick) {
      const r = await moveToTarget(ctx, step);
      box = r.box;
      await dwell(ctx);
      ctx.tel.setClickTarget(box);
      await ctx.h.press({});
      ctx.tel.setClickTarget(null);
      out = { target: describeTarget(step.target), rect: toVideoRect(box), point: toVideoPt(r.pt), warn: r.warn };
      await sleep(ctx.rng.range(160, 320));
    } else if (step.target) {
      const loc = locatorFor(ctx.page, step.target);
      box = await stableBox(loc, (step.timeout ?? 12) * 1000);
      out = { target: describeTarget(step.target), rect: toVideoRect(box) };
    }
    ctx.tel.setKeyTarget(box);
    if (step.clear) {
      await ctx.h.key('Control+A');
      await sleep(120);
      await ctx.h.key('Backspace');
      await sleep(220);
    }
    // segredo ("$NOME") ou campo de senha em foco: as teclas saem como "•" no telemetry.json (a pagina ja faz isso nos
    // campos de senha; o robo tem de fazer igual, senao as suas proprias amostras vazariam o que a pagina escondeu)
    const secret = !!ref || (await ctx.page.evaluate(() => window.__recSecretFocus?.() === true).catch(() => false));
    const tAct = ctx.T();
    if (secret) ctx.tel.maskKeys(true);
    try {
      await ctx.h.type(text, { cps: step.cps });
      if (step.submit) {
        await sleep(ctx.rng.range(260, 480));
        await ctx.h.key('Enter');
      }
    } finally {
      ctx.tel.maskKeys(false);
    }
    ctx.tel.setKeyTarget(null);
    // no actions.json vai o texto como esta no roteiro ("$NOME" literal), nunca o valor da variavel
    return { ...out, text: String(step.text ?? ''), tAct: r3(tAct), tEndTyping: r3(ctx.T()) };
  },

  async press(ctx, step) {
    const keys = Array.isArray(step.key) ? step.key : [step.key];
    const tAct = ctx.T();
    for (const k of keys) {
      for (let i = 0; i < (step.times ?? 1); i++) {
        await ctx.h.key(k);
        await sleep(step.delay ?? 120);
      }
    }
    return { key: step.key, tAct: r3(tAct) };
  },

  async scroll(ctx, step) {
    let out = {};
    if (step.target && step.by === undefined) {
      // so revelar o alvo
      const loc = locatorFor(ctx.page, step.target);
      const box = await stableBox(loc, (step.timeout ?? 12) * 1000);
      const b = await ensureVisible(ctx, loc, box, (step.timeout ?? 12) * 1000);
      return { target: describeTarget(step.target), rect: toVideoRect(b) };
    }
    if (step.target) {
      const loc = locatorFor(ctx.page, step.target);
      const box = await stableBox(loc, (step.timeout ?? 12) * 1000);
      await ctx.h.moveTo(box.x + box.width / 2, box.y + box.height / 2);
      out = { target: describeTarget(step.target), rect: toVideoRect(box) };
    } else if (step.point) {
      const p = step.point;
      await ctx.h.moveTo(p.x, p.y);
    } else {
      // area principal (a direita do menu lateral)
      await ctx.h.moveTo(step.x ?? 760, step.y ?? 460);
    }
    const tAct = ctx.T();
    // axis: "x" rola na horizontal (faixa de abas); sem axis, na vertical
    await ctx.h.scrollBy(step.by, { duration: step.duration, axis: step.axis === 'x' ? 'x' : 'y' });
    await sleep(step.after ?? 200);
    return { ...out, by: step.by, axis: step.axis === 'x' ? 'x' : 'y', tAct: r3(tAct) };
  },

  async select(ctx, step) {
    const r = await moveToTarget(ctx, step);
    const tag = await r.loc.evaluate((el) => el.tagName.toLowerCase());
    await dwell(ctx);
    const tAct = ctx.T();
    ctx.tel.setClickTarget(r.box);
    if (tag === 'select') {
      await ctx.h.press({});
      ctx.tel.setClickTarget(null);
      await sleep(250);
      await r.loc.selectOption(step.option.label ? { label: step.option.label } : { label: String(step.option) });
      return { target: describeTarget(step.target), rect: toVideoRect(r.box), option: step.option, tAct: r3(tAct) };
    }
    await ctx.h.press({});
    ctx.tel.setClickTarget(null);
    const optLoc = locatorFor(ctx.page, { role: 'option', name: String(step.option), exact: !!step.exact });
    const ob = await stableBox(optLoc, (step.timeout ?? 8) * 1000);
    const opt = pickPoint(ob, ctx.rng);
    await sleep(ctx.rng.range(180, 320));
    await ctx.h.moveTo(opt.x, opt.y);
    await dwell(ctx);
    ctx.tel.setClickTarget(ob);
    await ctx.h.press({});
    ctx.tel.setClickTarget(null);
    await sleep(220);
    return { target: describeTarget(step.target), rect: toVideoRect(r.box), option: step.option, optionRect: toVideoRect(ob), tAct: r3(tAct) };
  },

  /** Clica no botao que abre o seletor de arquivos e entrega o arquivo sem abrir a janela nativa (que nao aparece no video). */
  async upload(ctx, step) {
    // caminho relativo = relativo a pasta do roteiro
    const base = ctx.script._file ? path.dirname(ctx.script._file) : process.cwd();
    const files = [].concat(step.file).map((f) => path.resolve(base, f));
    for (const f of files) if (!fs.existsSync(f)) throw new Error(`arquivo nao encontrado: ${f}`);
    const { box, pt, warn } = await moveToTarget(ctx, step);
    await dwell(ctx);
    const tAct = ctx.T();
    const chooser = ctx.page.waitForEvent('filechooser', { timeout: (step.timeout ?? 8) * 1000 });
    ctx.tel.setClickTarget(box);
    await ctx.h.press({});
    ctx.tel.setClickTarget(null);
    const fc = await chooser.catch(() => {
      throw new Error('o clique nao abriu um seletor de arquivos (o alvo e o botao que abre o seletor?)');
    });
    await sleep(ctx.rng.range(350, 700)); // o "tempo de escolher o arquivo" na janela que nao aparece
    await fc.setFiles(files);
    await sleep(step.after ?? 500);
    return { target: describeTarget(step.target), rect: toVideoRect(box), point: toVideoPt(pt), file: files.map((f) => path.basename(f)), tAct: r3(tAct), warn };
  },

  /**
   * Arrasta de `target` ate `to` (um alvo ou { x, y } em px CSS), segurando o botao: serve para HTML5 drag and drop e
   * para bibliotecas por ponteiro (dnd-kit): pressiona, da um arranque curto, percorre o caminho e solta.
   * Opcao `hold`: segundos pairando sobre o destino antes de soltar (padrao 0,22 a 0,38 s).
   */
  async drag(ctx, step) {
    const src = await moveToTarget(ctx, step);
    await dwell(ctx);
    const tAct = ctx.T();
    ctx.tel.setClickTarget(src.box);
    const h = ctx.h;
    ctx.tel.nodeButton('down', h.x, h.y);
    await ctx.page.mouse.down();
    await sleep(ctx.rng.range(160, 280));
    await h.moveTo(h.x + 9, h.y + 7, { pace: 0.6 }); // arranque: passa do limite de ativacao do arrasto
    let dest;
    let destBox = null;
    if (step.to && typeof step.to.x === 'number' && typeof step.to.y === 'number') dest = { x: step.to.x, y: step.to.y };
    else {
      const loc = locatorFor(ctx.page, step.to);
      destBox = await stableBox(loc, (step.timeout ?? 12) * 1000);
      dest = pickPoint(destBox, ctx.rng);
    }
    await h.moveTo(dest.x, dest.y);
    // pairando sobre a area de soltar; `hold` (s) segura o item ali antes de soltar (ex.: o aviso "Solte aqui" fica visivel). Padrao: 0,22 a 0,38 s
    await sleep(step.hold !== undefined ? step.hold * 1000 : ctx.rng.range(220, 380));
    ctx.tel.setClickTarget(destBox);
    ctx.tel.nodeButton('up', h.x, h.y);
    await ctx.page.mouse.up();
    ctx.tel.setClickTarget(null);
    await sleep(step.after ?? 350);
    return { target: describeTarget(step.target), rect: toVideoRect(src.box), to: describeTarget(step.to), toRect: toVideoRect(destBox), tAct: r3(tAct), warn: src.warn };
  },

  /** Executa JavaScript na pagina (escape para preparar estado). `js` e uma expressao ou funcao; o retorno vai para `value`. */
  async eval(ctx, step) {
    const value = await ctx.page.evaluate(step.js);
    return { js: String(step.js).slice(0, 120), value: value === undefined ? undefined : JSON.parse(JSON.stringify(value)) };
  },

  // celular: posição do aparelho (A Caminho, Check-in e Finalizar pedem localização)
  // EcoTray falso (rec/recorder/ecotray-falso.mjs): material na balança e EcoTray aberto/fechado
  async balanca(ctx, step) {
    if (!ctx.session.ecotray) throw new Error('"balanca": o EcoTray falso está desligado neste roteiro ("ecotray": false?)');
    ctx.session.ecotray.peso(Number(step.peso) || 0, { subir: step.subir ?? 1.0, oscilar: step.oscilar ?? 1.0, balanca: step.balanca });
    if (step.seconds) await ctx.page.waitForTimeout(step.seconds * 1000);
  },
  async ecotray(ctx, step) {
    if (!ctx.session.ecotray) throw new Error('"ecotray": o EcoTray falso está desligado neste roteiro');
    if (step.ligado !== undefined) ctx.session.ecotray.ligar(!!step.ligado);
    if (step.seconds) await ctx.page.waitForTimeout(step.seconds * 1000);
  },
  async geo(ctx, step) {
    await ctx.session.context.setGeolocation({ latitude: step.lat, longitude: step.lng, accuracy: step.accuracy ?? 15 });
  },
  // relógio do navegador (precisa de FAKE_NOW): "forward": "01:25:00" avança o tempo (ex.: duração do atendimento)
  async clock(ctx, step) {
    if (step.forward !== undefined) await ctx.page.clock.fastForward(step.forward);
    else if (step.set) await ctx.page.clock.setSystemTime(new Date(step.set));
  },
  async wait(ctx, step) {
    await sleep((step.seconds ?? 1) * 1000);
    return { seconds: step.seconds ?? 1 };
  },
  async pause(ctx, step) {
    await sleep((step.seconds ?? 1) * 1000);
    return { seconds: step.seconds ?? 1, pause: true, why: step.why };
  },

  async waitFor(ctx, step) {
    const timeoutMs = (step.timeout ?? 15) * 1000;
    if (step.idle) {
      const ok = await settle(ctx.session, { quietMs: (step.quiet ?? 0.7) * 1000, timeoutMs });
      return { idle: true, ...(ok ? {} : notSettled(ctx.session)) };
    }
    if (step.url !== undefined) {
      const re = step.url instanceof RegExp ? step.url : new RegExp(String(step.url).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
      await ctx.page.waitForURL((u) => re.test(u.pathname + u.search), { timeout: timeoutMs });
      return { url: step.url };
    }
    if (step.gone) {
      await locatorFor(ctx.page, step.gone).waitFor({ state: 'hidden', timeout: timeoutMs });
      return { gone: describeTarget(step.gone) };
    }
    const t = step.target ?? (step.text !== undefined ? { text: step.text } : step.selector ? { selector: step.selector } : null);
    if (!t) throw new Error('waitFor precisa de target, text, selector, url, gone ou idle');
    const loc = locatorFor(ctx.page, t);
    try {
      await loc.waitFor({ state: 'visible', timeout: timeoutMs });
    } catch (e) {
      throw new Error(await explainMissing(loc, timeoutMs, e));
    }
    return { target: describeTarget(t) };
  },

  async mark(ctx, step) {
    const m = { name: step.name || `marca-${ctx.marks.length + 1}`, t: r3(ctx.T()), note: step.note };
    ctx.marks.push(m);
    return { name: m.name, note: step.note };
  },
};

// ------------------------------------------------------------------------------------------------
// Orquestracao
// ------------------------------------------------------------------------------------------------
function fmt(t) {
  return `${t.toFixed(2).padStart(7)}s`;
}

async function runSetup(ctx, steps) {
  for (const step of steps || []) {
    const fn = STEPS[step.do];
    if (!fn) throw new Error(`passo desconhecido no setup: ${step.do}`);
    await fn(ctx, step);
  }
}

/**
 * Confere o roteiro antes de abrir o navegador. Devolve { errors[], warnings[] } (erros impedem a gravacao).
 */
export function validateScript(script) {
  const errors = [];
  const warnings = [];
  const need = {
    click: ['target'], dblclick: ['target'], rightclick: ['target'], hover: ['target'], select: ['target', 'option'],
    goto: ['url'], press: ['key'], upload: ['target', 'file'], drag: ['target', 'to'], eval: ['js'], geo: ['lat', 'lng'],
  };
  const check = (list, where) => {
    let lastAt = -1;
    (list || []).forEach((st, i) => {
      const w = `${where}[${i}]`;
      if (!st || typeof st !== 'object') return errors.push(`${w}: passo precisa ser um objeto`);
      if (!STEPS[st.do]) return errors.push(`${w}: passo desconhecido "${st.do}" (validos: ${Object.keys(STEPS).join(', ')})`);
      for (const f of need[st.do] || []) if (st[f] === undefined) errors.push(`${w} (${st.do}): falta "${f}"`);
      if (st.do === 'type') {
        if (typeof st.text !== 'string') errors.push(`${w} (type): falta "text" (texto a digitar)`);
        if (!st.target && !st.noClick) warnings.push(`${w} (type): sem "target" digita no campo que ja estiver focado (use noClick: true para deixar explicito)`);
      }
      if (st.do === 'scroll' && st.by === undefined && !st.target) errors.push(`${w} (scroll): informe "by" (px) ou "target" (para revelar o alvo)`);
      if (st.do === 'waitFor' && !['idle', 'url', 'gone', 'target', 'text', 'selector'].some((k) => st[k] !== undefined)) errors.push(`${w} (waitFor): informe idle, text, selector, target, url ou gone`);
      if (st.target !== undefined && typeof st.target === 'object' && !['selector', 'text', 'role', 'placeholder', 'label', 'testId', 'title', 'alt'].some((k) => st.target[k] !== undefined)) errors.push(`${w}: target sem selector/text/role/placeholder/label/testId/title/alt`);
      if (st.at !== undefined) {
        if (typeof st.at !== 'number' || st.at < 0) errors.push(`${w}: "at" precisa ser um numero de segundos >= 0`);
        else {
          if (st.at < lastAt) warnings.push(`${w}: "at" ${st.at} vem antes do "at" ${lastAt} do passo anterior (vai sair atrasado)`);
          lastAt = Math.max(lastAt, st.at);
        }
      }
    });
  };
  if (!Array.isArray(script?.steps) || !script.steps.length) errors.push('roteiro sem "steps"');
  check(script?.steps, 'steps');
  check(script?.setup, 'setup');
  for (const u of script?.prewarm || []) if (typeof u !== 'string' || !u.startsWith('/')) errors.push(`prewarm: "${u}" precisa ser um caminho que comece com /`);
  if (script?.seedExtra !== undefined && !(Array.isArray(script.seedExtra) && script.seedExtra.every((f) => typeof f === 'string'))) errors.push('seedExtra precisa ser uma lista de nomes (ex.: ["t3/apos-cap02"])');

  // modo (fakebase | url), idioma e fuso do navegador
  let mode = null;
  let modeSource = null;
  try {
    ({ mode, source: modeSource } = resolveMode(script));
  } catch (e) {
    errors.push(e.message);
  }
  if (script?.locale !== undefined && !validLocale(script.locale)) errors.push(`locale ${JSON.stringify(script.locale)} invalido (ex.: "pt-BR", "en-US")`);
  if (script?.timezone !== undefined && !validTimezone(script.timezone)) errors.push(`timezone ${JSON.stringify(script.timezone)} invalido (nome IANA, ex.: "America/Sao_Paulo", "UTC")`);
  if (mode === 'url') for (const k of ['seedExtra', 'user', 'noReset']) if (script[k] !== undefined) warnings.push(`"${k}" so vale no modo fakebase: ignorado no modo url`);
  return { errors, warnings, mode, modeSource };
}

const validLocale = (v) => {
  try {
    return typeof v === 'string' && Intl.getCanonicalLocales(v).length === 1;
  } catch (e) {
    return false;
  }
};
const validTimezone = (v) => {
  try {
    return typeof v === 'string' && !!new Intl.DateTimeFormat('en', { timeZone: v });
  } catch (e) {
    return false;
  }
};

/**
 * @param {object} script  roteiro (ver README)
 * @param {object} opts    { outDir, name, headed, noEncode, keepFrames, noReset, cursorOverlay, preset, crf, verbose }
 */
export async function runScript(script, opts = {}) {
  const name = opts.name || script.name || 'gravacao';
  const lint = validateScript(script);
  for (const w of lint.warnings) console.log(`  aviso: ${w}`);
  if (lint.errors.length) throw new Error(`roteiro invalido:\n  - ${lint.errors.join('\n  - ')}`);
  const isUrl = lint.mode === 'url'; // modo url: o app de qualquer pessoa, por endereco (sem fakebase)
  if (isUrl && APP_ORIGIN) throw new Error('APP_ORIGIN so vale no modo fakebase (no modo url use APP_URL com o endereco do app)');
  // "$NOME" nos passos type: se faltar a variavel, para AQUI, antes de abrir o navegador (nunca no meio da gravacao)
  const missing = missingEnvVars(script);
  if (missing.length) {
    throw new Error(
      `faltam variaveis de ambiente do roteiro (passo type com "$NOME"):\n  - ${missing.map((m) => `${m.name} ${m.empty ? 'esta vazia' : 'nao esta definida'} (${m.where.join(', ')})`).join('\n  - ')}\n` +
        `  defina-as no ambiente antes de gravar (ex.: export ${missing[0].name}=...); o valor nunca e impresso nem gravado.`
    );
  }
  let appOrigin = null;
  if (isUrl) {
    try {
      appOrigin = new URL(APP_URL).origin; // so a origem: o endereco pode trazer usuario:senha
    } catch (e) {
      throw new Error('APP_URL nao e um endereco valido (ex.: APP_URL=http://127.0.0.1:3000)');
    }
  }
  const outDir = path.resolve(opts.outDir || script.outDir || '.');
  fs.mkdirSync(outDir, { recursive: true });
  const framesDir = path.join(outDir, '_frames');
  const debugDir = path.join(outDir, '_debug');
  const rng = makeRng(String(script.seed ?? name));
  const cursorOverlay = opts.cursorOverlay ?? script.cursorOverlay ?? false;
  const wall0 = Date.now();
  const log = (...a) => opts.verbose !== false && console.log(...a);

  if (isUrl) {
    log(`  modo url (${lint.modeSource}): ${appOrigin}`);
    if (!process.env.APP_URL) log('  aviso: APP_URL nao definido; usando o endereco de env.json (para outro app: APP_URL=http://... node rec/record.mjs ...)');
    log('  sem reset/seed, sessao anonima e rede sem desvio (nada do fakebase)');
  }

  if (APP_ORIGIN) log(`  APP_ORIGIN: o navegador abre o app em ${APP_ORIGIN} (servido pelo app local ${LOCAL_APP_URL}; nada sai para a rede)`);

  if (!isUrl && !(opts.noReset ?? script.noReset)) {
    await fetch(`${FAKE_URL}/__dev/reset`, { method: 'POST' }).catch(() => {
      throw new Error(`fakebase fora do ar em ${FAKE_URL} (rec/run.sh up)`);
    });
    // estado de partida do capitulo: seeds extras (rec/fakebase/seeds-extra/<nome>.json) por cima dos seeds normais
    if (Array.isArray(script.seedExtra) && script.seedExtra.length) {
      const r = await fetch(`${FAKE_URL}/__dev/seed`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ files: script.seedExtra }),
      });
      if (!r.ok) throw new Error(`seedExtra falhou (${r.status}): ${await r.text()}`);
      log(`  seeds extras aplicados: ${script.seedExtra.join(', ')}`);
    }
  }

  const session = await openSession({
    headed: opts.headed, email: script.user, storage: script.storage, cursorOverlay,
    anonymous: isUrl || !!script.anonymous, // modo url: sem login falso; "anonymous": true grava pagina publica sem sessao
    sameTab: !!script.sameTab, // "sameTab": true -> o que abriria outra aba abre nesta
    device: script.device, // "device": "phone" -> grava em tela de celular
    isolate: !isUrl, // modo url: a rede passa (o app e de outro lugar); fakebase: so localhost
    locale: script.locale, timezone: script.timezone, // padrao: pt-BR e America/Sao_Paulo
    ecotray: script.ecotray, // EcoTray falso: config, true/false; sem a opção, o do mundo (mundo.json "navegador.ecotray")
    dirImpressoes: path.join(outDir, `${name}.impressoes`), // o que o EcoTray falso "imprimiu" (PDF/PNG do app)
  });
  const { page, tel, diag } = session;
  const h = new Human(page, tel, rng, { pace: script.pace ?? 1, cps: script.cps ?? 11 });
  const marks = [];
  let t0Ms = null;
  const T = () => (t0Ms === null ? 0 : (Date.now() - t0Ms) / 1000);
  // spaNav: troca de rota por dentro do app (roteador da Dominex) so vale no fakebase; secrets: valores de "$NOME" ja usados
  const ctx = { page, session, tel, h, rng, script, T, marks, spaNav: !isUrl, secrets: new Map() };
  // rede de seguranca: se um valor de "$NOME" aparecer em texto vindo da pagina ou num erro (console, URL, mensagem), vira
  // "$NOME" antes de ir para o actions.json — tambem na forma de URL (%23, %3D...). Valores com menos de 4 caracteres
  // ficam de fora: estragariam textos comuns.
  const scrub = (s) => {
    let out = String(s);
    for (const [name, value] of ctx.secrets) {
      if (value.length < 4) continue;
      for (const v of new Set([value, encodeURIComponent(value)])) out = out.split(v).join(`$${name}`);
    }
    return out;
  };
  const actions = [];
  let cap = null;
  let capRes = null;
  let failure = null;
  let issues = null;

  try {
    // ---- preparo (nao vai para o video) ----
    for (const u of script.prewarm || []) {
      log(`  aquecendo ${u}${ctx.appLoaded && ctx.spaNav ? ' (navegacao interna)' : ''}`);
      if (ctx.appLoaded && ctx.spaNav) {
        await spaNavigate(page, u);
        await settle(session, { quietMs: 1200, timeoutMs: 60000 });
      } else {
        await page.goto(new URL(u, APP_URL).href, { waitUntil: 'load', timeout: 120000 });
        ctx.appLoaded = true;
        await settle(session, { quietMs: 1500, timeoutMs: 60000 });
      }
      await sleep(400);
    }
    await runSetup(ctx, script.setup);
    const start = script.start || { x: 900, y: 440 };
    await h.teleport(start.x, start.y);
    await sleep(300);

    // ---- grava ----
    diag.console.length = diag.pageErrors.length = diag.failed.length = diag.bad.length = 0;
    cap = await startCapture(page, framesDir, { width: VIEWPORT.width * SCALE, height: VIEWPORT.height * SCALE, quality: opts.quality ?? 92 });
    const first = await Promise.race([
      cap.firstFrame,
      sleep(2500).then(async () => {
        await page.evaluate(() => {
          document.documentElement.style.outline = '1px solid transparent';
          requestAnimationFrame(() => (document.documentElement.style.outline = ''));
        });
        return cap.firstFrame;
      }),
    ]);
    t0Ms = first;
    // posicao inicial do ponteiro em t=0 (e o cursor CSS sob ele)
    const kind0 = await page.evaluate(([x, y]) => {
      const el = document.elementFromPoint(x, y);
      const raw = (el ? getComputedStyle(el).cursor : 'auto').split(',').pop().trim();
      return raw === 'pointer' ? 'pointer' : raw === 'text' ? 'text' : 'arrow';
    }, [h.x, h.y]);
    tel.addExtra({ type: 'move', t: t0Ms, x: r1(h.x * SCALE), y: r1(h.y * SCALE), cursor: kind0, src: 'inicio' });

    const steps = script.steps || [];
    let i = 0;
    for (const step of steps) {
      const entry = { i, do: step.do };
      if (step.label) entry.label = step.label;
      if (step.note) entry.note = step.note;
      const fn = STEPS[step.do];
      if (!fn) throw new Error(`passo ${i}: "${step.do}" desconhecido`);
      if (step.at !== undefined) {
        entry.at = step.at;
        const wait = step.at - T();
        if (wait > 0) await sleep(wait * 1000);
      }
      entry.tStart = r3(T());
      if (step.at !== undefined && entry.tStart - step.at > 0.03) entry.lateBy = r3(entry.tStart - step.at);
      // passo condicional: `when` (executa so se o alvo ja estiver visivel) e `unless` (so se NAO estiver). Sem espera.
      // Serve para o mesmo roteiro valer em versoes do app diferentes (ex.: interruptor que ja vem ligado ou desligado).
      if (step.when !== undefined || step.unless !== undefined) {
        const seen = async (t) => (await locatorFor(page, t).count().catch(() => 0)) > 0;
        const run = (step.when === undefined || (await seen(step.when))) && (step.unless === undefined || !(await seen(step.unless)));
        if (!run) {
          entry.skipped = true;
          entry.ok = true;
          entry.tEnd = r3(T());
          actions.push(entry);
          log(`${fmt(entry.tStart)}  ${String(step.do).padEnd(8)} ${String(step.label ?? '').slice(0, 52).padEnd(52)} (pulado: condicao nao atendida)`);
          i++;
          continue;
        }
      }
      try {
        const out = await fn(ctx, step);
        Object.assign(entry, out);
        entry.ok = true;
      } catch (e) {
        entry.ok = false;
        entry.error = String(e?.message || e).split('\n')[0];
        if (ctx.secrets.size) entry.error = scrub(entry.error);
        fs.mkdirSync(debugDir, { recursive: true });
        await page.screenshot({ path: path.join(debugDir, `falha-${String(i).padStart(2, '0')}-${step.do}.png`), scale: 'css' }).catch(() => {});
        if (!step.optional) failure = entry;
      }
      entry.tEnd = r3(T());
      actions.push(entry);
      const what = step.target ? JSON.stringify(typeof step.target === 'string' ? step.target : step.target.text ?? step.target.name ?? step.target.placeholder ?? step.target.selector ?? step.target) : step.url ?? step.text ?? step.key ?? step.name ?? '';
      log(`${fmt(entry.tStart)}  ${String(step.do).padEnd(8)} ${String(what).slice(0, 52).padEnd(52)} ${entry.ok ? 'ok' : 'FALHOU: ' + entry.error}${entry.lateBy ? `  (atrasou ${entry.lateBy}s)` : ''}${entry.settled === false ? `  (rede nao assentou: ${entry.inflight} em voo, ${entry.quietMs} ms sem rede nova)` : ''}`);
      i++;
      if (failure) break;
    }
    if (!failure) await sleep((script.tail ?? 1.2) * 1000);
  } finally {
    const endMs = Date.now();
    if (cap) capRes = await cap.stop(endMs).catch((e) => (log('erro ao parar captura:', e.message), null));
    issues = {
      console: [...diag.console],
      pageErrors: [...diag.pageErrors],
      failed: [...diag.failed],
      bad: [...diag.bad],
    };
    await closeSession(session).catch(() => {});
  }

  if (ctx.secrets.size) {
    issues = {
      console: issues.console.map((c) => ({ ...c, text: scrub(c.text), url: scrub(c.url) })),
      pageErrors: issues.pageErrors.map(scrub),
      failed: issues.failed.map(scrub),
      bad: issues.bad.map(scrub),
    };
  }

  if (!capRes || !capRes.frames.length) throw new Error('nenhum quadro capturado');
  const endS = capRes.endS;

  // ---- telemetria ----
  const telem = tel.finalize({ t0Ms: capRes.t0Ms, endS });
  const telemetryFile = path.join(outDir, `${name}.telemetry.json`);
  const videoMeta = { width: VIEWPORT.width * SCALE, height: VIEWPORT.height * SCALE, fps: 30, durationS: r3(endS), dsf: SCALE, viewportCss: VIEWPORT };
  fs.writeFileSync(
    telemetryFile,
    JSON.stringify(
      {
        video: videoMeta,
        clock: 't = segundos desde o 1o quadro do video (mesmo relogio dos quadros e de actions.json)',
        units: 'x, y e rect em pixels do video (2560x1600); deltaY em px CSS da roda',
        cursorKinds: 'arrow | pointer | text (cursor CSS do elemento sob o ponteiro; cursorRaw traz o valor original quando diferente)',
        counts: telem.counts,
        samples: telem.samples,
      },
      null,
      0
    ).replace(/\},\{/g, '},\n{')
  );

  // ---- video ----
  const mp4 = path.join(outDir, `${name}.mp4`);
  let enc = null;
  let probe = null;
  let sheet = null;
  if (!opts.noEncode) {
    log(`  montando ${path.basename(mp4)} (${capRes.frames.length} quadros capturados em ${endS.toFixed(1)} s)...`);
    enc = await assemble({ frames: capRes.frames, endS, outFile: mp4, fps: 30, crf: opts.crf ?? 16, preset: opts.preset ?? 'veryfast' });
    probe = await probeVideo(mp4);
    sheet = path.join(outDir, `${name}.contact.jpg`);
    await contactSheet(mp4, sheet, { fps: 30, totalTicks: enc.ticks });
  }

  // ---- log de acoes ----
  const late = actions.filter((a) => a.lateBy);
  const gaps = capRes.frames.slice(1).map((f, k) => f.t - capRes.frames[k].t).sort((a, b) => a - b);
  const stats = {
    capturedFrames: capRes.frames.length,
    captureFps: r1(capRes.frames.length / Math.max(0.001, endS)),
    medianFrameGapMs: gaps.length ? r1(gaps[Math.floor(gaps.length / 2)] * 1000) : null,
    p90FrameGapMs: gaps.length ? r1(gaps[Math.floor(gaps.length * 0.9)] * 1000) : null,
    maxFrameGapMs: gaps.length ? r1(gaps[gaps.length - 1] * 1000) : null,
    videoDurationS: r3(endS),
    captureWallS: r3(endS), // captura em tempo real: 1 s de gravacao = 1 s de relogio
    encodeS: enc ? r1(enc.encodeS) : null,
    encodeVsRealtime: enc ? r1(enc.encodeS / endS) : null,
    totalWallS: r1((Date.now() - wall0) / 1000),
    pointerMoveSteps: h.moveSteps,
    staleRequestsDropped: diag.staleDropped || 0, // requisicoes perdidas pelo navegador que o `settle` precisou descartar (esperado: 0)
    // taxa de captura enquanto a tela esta mudando (lacunas <= 250 ms); a media geral inclui os trechos parados
    motionFps: (() => {
      const g = gaps.filter((x) => x <= 0.25);
      return g.length ? r1(1 / g[Math.floor(g.length / 2)]) : null;
    })(),
    // carimbo do quadro (relogio do Chrome) -> chegada no Node: mede carga da maquina, nao desalinhamento de relogio
    frameDeliveryLatencyMs: (() => {
      const d = capRes.frames.map((f) => f.recvMs - (capRes.t0Ms + f.t * 1000)).sort((a, b) => a - b);
      return d.length ? r1(d[Math.floor(d.length / 2)]) : null;
    })(),
    telemetry: { samples: telem.samples.length, byType: telem.counts, filledByRunner: telem.runnerFilled },
  };
  const actionsFile = path.join(outDir, `${name}.actions.json`);
  fs.writeFileSync(
    actionsFile,
    JSON.stringify(
      {
        script: script._file ? path.basename(script._file) : null,
        name,
        video: { ...videoMeta, file: path.basename(mp4), codec: probe ? `${probe.codec_name} ${probe.pix_fmt} ${probe.color_space}/${probe.color_range}` : null },
        clock: 't, tStart, tEnd, tAct, at, lateBy em segundos desde o 1o quadro do video; rect, point e optionRect em pixels do video (2560x1600)',
        t0EpochMs: Math.round(capRes.t0Ms),
        actions,
        marks,
        late: { count: late.length, maxS: late.length ? Math.max(...late.map((a) => a.lateBy)) : 0 },
        pageIssues: issues,
        stats,
      },
      null,
      2
    )
  );

  if (!opts.keepFrames) fs.rmSync(framesDir, { recursive: true, force: true });
  else fs.writeFileSync(path.join(framesDir, 'frames.json'), JSON.stringify(capRes.frames.map((f) => ({ file: path.basename(f.file), t: r3(f.t), bytes: f.bytes }))));
  const result = { ok: !failure, failure, files: { mp4: enc ? mp4 : null, actions: actionsFile, telemetry: telemetryFile, contact: sheet }, stats, probe };
  return result;
}

/** Carrega um roteiro .json ou .mjs (default = objeto ou funcao que devolve o objeto). */
export async function loadScript(file) {
  const abs = path.resolve(file);
  let script;
  if (abs.endsWith('.json')) script = JSON.parse(fs.readFileSync(abs, 'utf8'));
  else {
    const mod = await import(abs + '?t=' + Date.now());
    script = typeof mod.default === 'function' ? await mod.default() : mod.default;
  }
  script._file = abs;
  return script;
}
