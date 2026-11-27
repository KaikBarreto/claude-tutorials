// EcoFlix · kit de ilustrações v3: UM mundo 3D, DOIS climas (claro = mundo físico; escuro = mundo dos dados).
// A cena é um espaço com estações: objetos 3D (three.js, material de degradê do kit) e planos HTML (cartão, visor, chip)
// presos no mesmo espaço e vistos pela MESMA câmera. Passar de um conceito ao outro é mover a câmera. Ver LEIA.md.
// Página: <script type="module"> importa este arquivo e chama cena(monta). O render_cenas.cjs chama window.setup(dados)
// e window.R(t). Tudo é função pura de t (sem relógio, sem estado entre quadros). Sem rede.
import * as THREE from '../cenas3d/three.module.min.js';
export { THREE };

// ------------------------------------------------------------------ tempo e movimento (as curvas do MOTION_V2)
export const PI = Math.PI;
export const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, p) => a + (b - a) * p;
export const pr = (t, a, d = .45) => cl((t - a) / d);
export const eo = x => 1 - Math.pow(1 - cl(x), 3);
export const eio = x => { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
export const eo5 = x => 1 - Math.pow(1 - cl(x), 5);                      // entrada: arranca na hora, desacelera por muito tempo
export const ei = x => { x = cl(x); return x * x * x; };                 // saída: curta e acelerando
export const eio5 = x => { x = cl(x); return x < .5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2; };   // movimento com peso
export const eis = x => { x = cl(x); return x * x * x * (x * (x * 6 - 15) + 10); };                        // câmera: arranca e para sem tranco
export const passa = (x, k = 1.1) => { x = cl(x) - 1; return 1 + (k + 1) * x * x * x + k * x * x; };       // passa um pouco e volta
export function mola(x, z = .5) {   // resposta ao degrau de uma mola amortecida (analítica): 0 → 1
  x = cl(x); if (x >= 1) return 1; if (z >= 1) { const w = 9; return 1 - Math.exp(-w * x) * (1 + w * x); }
  const w = 7 / z, wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * x) * (Math.cos(wd * x) + z * w / wd * Math.sin(wd * x));
}
export const golpe = (x, n = 1.6, a = 4.2) => (x <= 0 || x >= 1) ? 0 : Math.exp(-a * x) * Math.sin(2 * PI * n * x) * (1 - x) * 1.55;   // bate e morre
export const escalona = (a, i, passo = .09) => a + i * passo;
let S = 0;
export const semente = s => { S = s | 0; };
export const rng = () => { S = S + 0x6D2B79F5 | 0; let t = Math.imul(S ^ S >>> 15, 1 | S); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
export const ri = (a, b) => lerp(a, b, rng());

// ------------------------------------------------------------------ ponte com a fala
let D = null;
const norm = w => w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%./-]+/g, '');
export function W(linha, palavra, n = 1, campo = 's') {   // instante da n-ésima "palavra" da linha (campo 'e' = fim)
  const alvo = norm(palavra); let k = 0;
  for (const w of D.words) if (w.linha === linha && norm(w.w).replace(/[.,:]$/, '') === alvo && ++k === n) return w[campo];
  k = 0; for (const w of D.words) if (w.linha === linha && norm(w.w).startsWith(alvo) && ++k >= n) return w[campo];
  console.warn('palavra não achada', linha, palavra); return L(linha);
}
export const L = i => (D.linhas.find(l => l.i === i) || { s: 0 }).s, LE = i => (D.linhas.find(l => l.i === i) || { e: D.dur }).e;

// ------------------------------------------------------------------ palco e os dois climas (CSS)
// Um sistema só: as mesmas classes (.cartao, .chip, .selo, .visor, .op, .num, .tit) leem as variáveis do clima do pai
// (.claro ou .escuro). Nada de backdrop-filter nem de blur por quadro: vidro = degradê translúcido + fio de luz + sombra.
const FT = new URL('../../../ferramentas/web/fonts/', import.meta.url).href;   // se não achar, o renderizador põe as da skill
const ff = (w, x) => `@font-face{font-family:M;font-weight:${w};src:url(${FT}montserrat-latin${x ? '-ext' : ''}-${w}-normal.woff2) format('woff2')${x ? ';unicode-range:U+0100-024F' : ''}}`;
// Largura do desenho: 1280 (16:10) ou a da janela quando ela é mais larga (16:9 = 1422x800; EcoFlix desde 19/11). A altura é sempre 800.
export const LARG = Math.round(globalThis.innerWidth || 504);   // VERTICAL: o desenho é a janela inteira (504x850 a 2x = painel 1008x1700 do 9:16)
export const ALT = Math.round(globalThis.innerHeight || 850);
const CSS = [500, 600, 700, 800].map(w => ff(w) + ff(w, 1)).join('') + `
:root{--v:#50D088;--ve:#2E7D57;--vc:#6CF0A8;--a:#F2B63D;--r1:12px;--r2:16px;--r3:22px;--rp:999px}
*{box-sizing:border-box;margin:0;padding:0;transition:none!important;animation:none!important}
html,body{width:${LARG}px;height:${ALT}px;overflow:hidden;background:#F4F7F6}
body{font-family:M,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
#st,#cu,#ce,#tr,#dc,#fr,#hud{position:absolute;left:0;top:0;width:${LARG}px;height:${ALT}px;overflow:hidden;isolation:isolate}
#gl{position:absolute;left:0;top:0;width:${LARG}px;height:${ALT}px}
#cu{background:linear-gradient(180deg,#F1F6F5 0%,#F6F9F8 58%,#FBFCFB 100%)}
#ce{opacity:0;background:radial-gradient(900px 620px at 50% 58%,rgba(80,208,136,.13),transparent 70%),radial-gradient(700px 520px at 100% 0%,rgba(80,208,136,.10),transparent 70%),
  radial-gradient(640px 520px at 0% 4%,rgba(90,150,255,.09),transparent 70%),linear-gradient(180deg,#17191A,#131415)}
#ce:after{content:"";position:absolute;inset:0;background:radial-gradient(1000px 640px at 50% 50%,transparent 55%,rgba(0,0,0,.42) 100%)}
.pl{position:absolute;left:0;top:0;transform-origin:0 0;backface-visibility:visible}
.ab{position:absolute}
.claro{--tx:#17191A;--tx2:#5F6E68;--cart:linear-gradient(165deg,#FFFFFF 0%,#F4F9F7 100%);--cb:1px solid rgba(255,255,255,.95);
  --cs:0 28px 54px -14px rgba(30,80,60,.26),0 6px 14px -4px rgba(30,80,60,.10),inset 0 1px 0 #fff;
  --res:linear-gradient(165deg,#F2FCF7 0%,#DDF6E8 100%);--resb:1.5px solid rgba(80,208,136,.75);
  --ress:0 30px 60px -14px rgba(47,178,113,.42),0 6px 14px -4px rgba(30,80,60,.10),inset 0 1px 0 #fff;
  --num:linear-gradient(100deg,#17191A,#17191A);--numr:linear-gradient(100deg,#178F57,#2FB271 55%,#50D088);--nsh:none;
  --chip:linear-gradient(100deg,#2FB271,#63D99B);--chipb:0 solid transparent;--chipt:#fff;--chips:0 12px 24px -6px rgba(47,178,113,.5),inset 0 1px 0 rgba(255,255,255,.45);
  --chn:linear-gradient(100deg,#39424A,#59646E);--chns:0 12px 24px -8px rgba(30,40,50,.42),inset 0 1px 0 rgba(255,255,255,.22);
  --op:linear-gradient(150deg,#FFFFFF,#EAF1EE);--opt:#3B4650;--ops:0 12px 22px -8px rgba(30,80,60,.34),inset 0 1px 0 #fff;--opb:1px solid #fff;
  --kick:#2E7D57;--h:linear-gradient(100deg,#17191A 35%,#2E7D57)}
.escuro{--tx:#F4F6F5;--tx2:rgba(255,255,255,.62);--cart:linear-gradient(160deg,rgba(255,255,255,.150) 0%,rgba(255,255,255,.045) 60%,rgba(255,255,255,.07) 100%);
  --cb:1px solid rgba(255,255,255,.20);--cs:0 30px 60px -12px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.26),inset 0 0 0 1px rgba(255,255,255,.03);
  --res:linear-gradient(160deg,rgba(80,208,136,.30) 0%,rgba(80,208,136,.09) 62%,rgba(80,208,136,.14) 100%);--resb:1px solid rgba(108,240,168,.62);
  --ress:0 30px 60px -12px rgba(0,0,0,.6),0 0 60px rgba(80,208,136,.26),inset 0 1px 0 rgba(255,255,255,.28);
  --num:linear-gradient(100deg,#F4F6F5,#F4F6F5);--numr:linear-gradient(100deg,#6CF0A8,#8CF5BE);--nsh:drop-shadow(0 0 14px rgba(80,208,136,.55));
  --chip:linear-gradient(160deg,rgba(80,208,136,.34),rgba(80,208,136,.14));--chipb:1px solid rgba(108,240,168,.6);--chipt:#D9FBE8;
  --chips:0 10px 26px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.25),0 0 26px rgba(80,208,136,.30);
  --chn:linear-gradient(160deg,rgba(255,255,255,.17),rgba(255,255,255,.06));--chns:0 10px 26px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.25);
  --op:linear-gradient(160deg,rgba(255,255,255,.20),rgba(255,255,255,.07));--opt:#F4F6F5;--ops:0 10px 22px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.28);--opb:1px solid rgba(255,255,255,.22);
  --kick:#6CF0A8;--h:linear-gradient(100deg,#FFFFFF 40%,#BFF5DA)}
.tit{position:absolute;left:0;top:0;width:${LARG}px;text-align:center}
.kick{font-weight:700;font-size:13px;letter-spacing:.3em;color:var(--kick);text-transform:uppercase;white-space:nowrap}
.h{display:inline-block;margin-top:8px;font-weight:800;font-size:34px;letter-spacing:-.02em;line-height:1.14;white-space:normal;max-width:${LARG - 56}px;padding:0 4px 3px;
  background:var(--h);-webkit-background-clip:text;background-clip:text;color:transparent}
.cartao{position:absolute;border-radius:var(--r3);background:var(--cart);border:var(--cb);box-shadow:var(--cs);color:var(--tx);padding:18px 22px}
.cartao.res{background:var(--res);border:var(--resb);box-shadow:var(--ress)}
.cartao .cab{display:flex;align-items:center;gap:11px;white-space:nowrap}
.cartao .rot{font-weight:800;font-size:19px;letter-spacing:-.005em;line-height:1.15}
.cartao .sub,.sub{font-weight:600;font-size:15px;line-height:1.25;color:var(--tx2);white-space:nowrap}
.num{display:inline-block;font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.02em;white-space:nowrap;line-height:1.1;padding-right:3px;
  background:var(--num);-webkit-background-clip:text;background-clip:text;color:transparent}
.res .num,.num.r{background-image:var(--numr);filter:var(--nsh)}
.selo{display:flex;align-items:center;justify-content:center;flex:none;width:42px;height:42px;border-radius:13px;color:#fff;
  background:linear-gradient(150deg,#63D99B,#2FB271);box-shadow:0 10px 18px -6px rgba(47,178,113,.6),inset 0 1px 0 rgba(255,255,255,.45)}
.selo.a{background:linear-gradient(150deg,#F7CB68,#E59A22);box-shadow:0 10px 18px -6px rgba(229,154,34,.6),inset 0 1px 0 rgba(255,255,255,.45)}
.selo.n{background:linear-gradient(150deg,#69747F,#39424A);box-shadow:0 10px 18px -6px rgba(30,40,50,.5),inset 0 1px 0 rgba(255,255,255,.25)}
.chip{position:absolute;display:inline-flex;align-items:center;gap:8px;height:38px;padding:0 17px 0 13px;border-radius:var(--rp);font-weight:800;font-size:17px;
  white-space:nowrap;color:var(--chipt);background:var(--chip);border:var(--chipb);box-shadow:var(--chips)}
.chip.n{background:var(--chn);box-shadow:var(--chns);color:#fff;border-color:rgba(255,255,255,.22)}
.op{position:absolute;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:28px;line-height:1;
  color:var(--opt);background:var(--op);border:var(--opb);box-shadow:var(--ops)}
/* o visor é um aparelho (tela de LED): é escuro nos dois climas. No claro é a única superfície escura: a porta dos dados */
.visor{position:absolute;width:262px;border-radius:20px;padding:15px 22px 17px;background:linear-gradient(170deg,#202423 0%,#131514 60%);
  box-shadow:0 30px 56px -14px rgba(16,30,24,.55),inset 0 1px 0 rgba(255,255,255,.16),inset 0 0 0 1px rgba(255,255,255,.06)}
.escuro .visor{background:linear-gradient(160deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.22);
  box-shadow:0 24px 50px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.28),0 0 44px rgba(80,208,136,.20)}
.visor .vl{position:relative;height:18px;font-weight:700;font-size:12.5px;letter-spacing:.2em;color:#A9E9C6;text-transform:uppercase}
.visor .vl span{position:absolute;left:0;top:0;white-space:nowrap}
.visor .vd{position:absolute;right:0;top:4px;width:9px;height:9px;border-radius:50%;background:var(--v);box-shadow:0 0 0 3px rgba(80,208,136,.22)}
.visor .vn{margin-top:7px;font-weight:800;font-size:43px;letter-spacing:-.02em;line-height:1.08;color:var(--vc);font-variant-numeric:tabular-nums;white-space:nowrap;
  text-shadow:0 0 18px rgba(80,208,136,.55)}
.ic{display:inline-flex;align-items:center;justify-content:center;flex:none}.ic svg{width:100%;height:100%}
.onda{position:absolute;inset:-2px;border-radius:calc(var(--r3) + 2px);border:2px solid var(--v);opacity:0;pointer-events:none}`;

export let ST = null, GL = null, TR = null, DC = null, FR = null, HUD = null, CE = null;
{ const s = document.createElement('style'); s.textContent = CSS; document.head.prepend(s);
  document.body.insertAdjacentHTML('afterbegin', '<div id="st"><div id="cu"></div><div id="ce"></div><div id="tr"></div><div id="dc"></div><canvas id="gl" width="'+LARG+'" height="'+ALT+'"></canvas><div id="fr"></div><div id="hud"></div></div>');
  const q = i => document.getElementById(i); ST = q('st'); GL = q('gl'); TR = q('tr'); DC = q('dc'); FR = q('fr'); HUD = q('hud'); CE = q('ce'); }

export function el(html, pai = HUD) { const d = document.createElement('div'); d.innerHTML = html.trim(); const f = d.firstElementChild; pai.appendChild(f); return f; }
export function ic(n, px) { return `<span class="ic" style="width:${px}px;height:${px}px">${(window.ICONS || {})[n] || ''}</span>`; }   // o nome tem de estar literal na PÁGINA da cena

// ------------------------------------------------------------------ rótulos: entrada, saída, foco, número
// vis: a opacidade chega antes da posição; quem entra por escala (sc < .9) passa um pouco e volta; saída curta
export function vis(e, t, a, b = 1e9, o = {}) {
  const din = o.din ?? .5, dout = o.dout ?? .4, dy = o.dy ?? 16, dx = o.dx ?? 0, sc = o.sc ?? .985;
  const x = pr(t, a, din * 1.3), p = eo5(x), po = eo(pr(t, a, din * .62)), y = pr(t, b, dout * .7), q = 1 - ei(y), op = Math.min(po, 1 - y * y);
  e.style.opacity = op.toFixed(4); e.style.visibility = op <= .001 ? 'hidden' : 'visible';
  const ps = sc < .9 ? passa(pr(t, a, din * 1.1), 1.6) : p, s = sc + (1 - sc) * ps - (1 - q) * (1 - sc) * .6;
  e.style.transform = `translate(${((1 - p) * dx).toFixed(2)}px,${((1 - p) * dy - (1 - q) * dy * .4).toFixed(2)}px) scale(${s.toFixed(4)})`;
  return op;
}
// foco: um assunto por momento. Fora de [a, b] o elemento recua (opacidade e saturação). Chamar DEPOIS do vis.
export function foco(e, t, a, b = 1e9, o = {}) {
  let k = Math.min(eo(pr(t, a, o.d ?? .4)), 1 - eo(pr(t, b, o.d ?? .4))); if (o.fora) k = 1 - k; const m = o.min ?? .45;
  e.style.opacity = ((+e.style.opacity || 0) * lerp(m, 1, k)).toFixed(4); e.style.filter = k > .995 ? '' : `saturate(${lerp(.4, 1, k).toFixed(3)})`; return k;
}
export function pulso(e, t, a, amp = .045, dur = .9) { const p = pr(t, a, dur); e.style.scale = (p > 0 && p < 1) ? (1 + amp * 1.25 * golpe(p, 1.1, 3.4)).toFixed(4) : ''; }
// onda: o contorno do cartão se solta, cresce e some (o resultado "bate")
export function ondaEm(r, t, a, d = 1.0) { const p = pr(t, a, d), q = eo5(p); r.style.opacity = (p > 0 && p < 1) ? (.9 * Math.pow(1 - p, 1.5)).toFixed(3) : 0; r.style.transform = `scale(${(1 + .11 * q).toFixed(4)},${(1 + .2 * q).toFixed(4)})`; }
const NF = new Intl.NumberFormat('pt-BR'), NF1 = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
export const kg = v => NF.format(Math.round(v)) + ' kg';
export const kgd = v => (Math.abs(v * 10 - Math.round(v) * 10) < .5 && Math.abs(v - Math.round(v)) < .05 ? NF.format(Math.round(v)) : NF1.format(Math.round(v * 10) / 10)) + ' kg';
export const kg1 = v => NF1.format(Math.round(v * 10) / 10) + ' kg';
const poe = (e, s) => { if (e.textContent !== s) e.textContent = s; };
export function conta(e, t, a, d, v0, v1, fmt = kg) { poe(e, fmt(lerp(v0, v1, eo5(pr(t, a, d * 1.15))))); }
// leitura de balança: passa do valor e volta (mola), de `passo` em `passo`; a luz do visor fica âmbar enquanto mexe
export function pesa(v, t, a, d, v0, v1, o = {}) {
  const x = pr(t, a, d), ps = o.passo ?? 10, val = lerp(v0, v1, mola(x, o.z ?? .74));
  poe(v.vn, (o.fmt || kg)(x <= 0 ? v0 : x >= 1 ? v1 : Math.round(val / ps) * ps));
  const m = x > 0 && x < .93; v.vd.style.background = m ? '#F2B63D' : '#50D088'; v.vd.style.boxShadow = m ? '0 0 0 3px rgba(242,182,61,.22)' : '0 0 0 3px rgba(80,208,136,.22)'; return x;
}

// ------------------------------------------------------------------ componentes (HTML; o clima vem da classe do plano)
export function titulo(kick, h, clima = 'claro') {   // título no quadro (HUD), fora do espaço: nada passa por cima dele
  return el(`<div class="tit ${clima}"><div class="kick">${kick}</div><div class="h">${h}</div></div>`);
}
// título grande no meio que sobe para o topo quando o desenho entra; a chamada chega 90 ms antes, com as letras fechando
export function posTitulo(e, t, a, sobe, sai = 1e9, o = {}) {
  vis(e, t, a, sai, { dy: 14 }); const p = eio5(pr(t, sobe - .05, .85)), y0 = o.y0 ?? ALT / 2 - 80, y1 = o.y1 ?? 38;
  e.style.top = lerp(y0, y1, p).toFixed(2) + 'px'; e.style.scale = lerp(o.s0 ?? 1.12, 1, p).toFixed(4);
  const k = e.firstElementChild, h = k.nextElementSibling, pk = eo5(pr(t, a, .9)), ph = eo5(pr(t, a + .09, .75));
  k.style.letterSpacing = lerp(.42, .3, pk).toFixed(4) + 'em'; h.style.transform = `translateY(${((1 - ph) * 10).toFixed(2)}px)`; h.style.opacity = eo(pr(t, a + .09, .4)).toFixed(3);
}
export const selo = (icone, cls = '', px = 42) => `<div class="selo ${cls}" style="width:${px}px;height:${px}px;border-radius:${Math.round(px * .31)}px">${ic(icone, Math.round(px * .56))}</div>`;
export const htmlChip = (txt, cls = '') => `<div class="chip ${cls}" style="position:relative">${txt}</div>`;
// cartão de número: selo com ícone + rótulo + legenda + número. o.res = resultado (verde); o.w/o.h; o.fn = corpo do número
export function htmlCartao(icone, rot, sub, valor, o = {}) {
  return `<div class="cartao ${o.res ? 'res' : ''}" style="position:relative;width:${o.w ?? 300}px;height:${o.h ?? 132}px">
    <div class="cab">${selo(icone, o.cls ?? (o.res ? '' : 'n'), o.selo ?? 42)}<div><div class="rot">${rot}</div><div class="sub">${sub}</div></div></div>
    <div class="num" style="margin-top:${o.mt ?? 12}px;font-size:${o.fn ?? 36}px">${valor}</div>${o.res ? '<div class="onda"></div>' : ''}</div>`;
}
export const htmlOp = s => `<div class="op" style="position:relative">${s}</div>`;
export const htmlVisor = (rots, w = 262) => `<div class="visor" style="position:relative;width:${w}px"><div class="vl">${[].concat(rots).map((r, i) => `<span style="opacity:${i ? 0 : 1}">${r}</span>`).join('')}<i class="vd"></i></div><div class="vn">0 kg</div></div>`;
export function ligaVisor(e) {   // e.troca(t, a, i): no instante a, o rótulo i-1 sobe e some e o rótulo i sobe e entra (chamar em ordem)
  e.vn = e.querySelector('.vn'); e.vs = [...e.querySelectorAll('.vl span')]; e.vd = e.querySelector('.vd');
  e.troca = (t, a, i = 1) => { if (t < a - .02) return; const p = eo5(pr(t, a, .5)), q = eo(pr(t, a, .22)), s0 = e.vs[i - 1], s1 = e.vs[i];
    s0.style.opacity = (1 - q).toFixed(3); s1.style.opacity = eo(pr(t, a + .08, .3)).toFixed(3);
    s0.style.transform = `translateY(${(-7 * q).toFixed(2)}px)`; s1.style.transform = `translateY(${(7 * (1 - p)).toFixed(2)}px)`; };
  e.zera = () => e.vs.forEach((s, i) => { s.style.opacity = i ? 0 : 1; s.style.transform = ''; });
  return e;
}
// fluxo: traço SVG num plano, que se desenha de a até a+d e por onde corre um ponto de luz (de la até la+ld)
export function htmlFluxo(w, h, caminhos, o = {}) {
  const c = o.cor ?? 'var(--vc)';
  return `<svg class="fluxo" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="overflow:visible;display:block" fill="none" stroke-linecap="round" stroke-linejoin="round">
    ${caminhos.map(d => `<g><path class="fb" d="${d}" stroke="${o.base ?? 'rgba(255,255,255,.16)'}" stroke-width="${o.lw ?? 2}"/><path class="ft" d="${d}" stroke="${c}" stroke-width="${(o.lw ?? 2) + .6}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <circle class="fp" r="${o.rp ?? 5}" fill="${o.ponto ?? '#fff'}" opacity="0"/><circle class="fh" r="${(o.rp ?? 5) * 2.6}" fill="${c}" opacity="0"/></g>`).join('')}</svg>`;
}
export function fluxo(svg, i, t, a, d, o = {}) {   // i = qual caminho; o.luz = [inicio, duração] do ponto que corre; o.fica = o traço aceso depois
  const g = svg.children[i], ft = g.querySelector('.ft'), fp = g.querySelector('.fp'), fh = g.querySelector('.fh'), p = eio(pr(t, a, d));
  ft.setAttribute('stroke-dashoffset', (1 - p).toFixed(4)); ft.setAttribute('opacity', (o.fica ?? .55).toFixed(3));
  const [la, ld] = o.luz || [a, d], q = pr(t, la, ld), on = q > 0 && q < 1;
  if (on) { const len = g._len ?? (g._len = ft.getTotalLength()), pt = ft.getPointAtLength(len * eio(q)), k = Math.sin(PI * q) ** .5;
    for (const c of [fp, fh]) { c.setAttribute('cx', pt.x.toFixed(2)); c.setAttribute('cy', pt.y.toFixed(2)); }
    fp.setAttribute('opacity', k.toFixed(3)); fh.setAttribute('opacity', (k * .32).toFixed(3)); }
  else { fp.setAttribute('opacity', 0); fh.setAttribute('opacity', 0); }
}

// ------------------------------------------------------------------ 3D: palco, material de degradê (dois climas), câmera
export let RD = null, CENA = null, CAM = null;
const OPC = { fov: 26, inercia: .34, respira: 1, semente: 20261118, pr: 1.5 };
export const U = { uClima: { value: 0 }, uNevoa: { value: new THREE.Vector4(1, 1, 1, 0) } };   // uniformes de todos os materiais
function base() {
  if (!RD) {
    RD = new THREE.WebGLRenderer({ canvas: GL, antialias: true, alpha: true, preserveDrawingBuffer: true });
    RD.setPixelRatio(Math.min(window.devicePixelRatio || 1, OPC.pr)); RD.setSize(LARG, ALT, false); RD.setClearColor(0x000000, 0);
    RD.outputColorSpace = THREE.LinearSRGBColorSpace;   // as cores do material já são as da tela (hex da marca sem conversão)
  }
  CENA = new THREE.Scene(); CAM = new THREE.PerspectiveCamera(OPC.fov, LARG / ALT, .2, 400);
  PLANOS.length = 0; TR.innerHTML = ''; DC.innerHTML = ''; DC.style.clipPath = DC._cp = ''; FR.innerHTML = ''; HUD.innerHTML = ''; MC.clear();
}
const hex = c => { const n = parseInt(c.slice(1), 16); return new THREE.Vector3((n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255); };
const VS = `varying vec3 vN; varying vec3 vW; varying vec3 vC;
void main(){ vec4 p = vec4(position, 1.0); vec3 n = normal; vC = vec3(1.0);
#ifdef USE_INSTANCING
  p = instanceMatrix * p; n = mat3(instanceMatrix) * n;
#endif
#ifdef USE_INSTANCING_COLOR
  vC = instanceColor;
#endif
  vec4 w = modelMatrix * p; vW = w.xyz; vN = normalize(mat3(modelMatrix) * n); gl_Position = projectionMatrix * viewMatrix * w; }`;
// Material do kit. Claro: degradê macio (luz de cima-esquerda em meia sombra fria, topo mais claro, brilho de borda branco,
// escuro de contato perto do chão). Escuro: corpo quase preto com fio de luz na borda (fresnel) e emissivo (uEmi).
const FS = `uniform vec3 uCor; uniform float uClima, uEmi, uEmiC, uAlt, uOp, uBri; uniform vec4 uNevoa; varying vec3 vN; varying vec3 vW; varying vec3 vC;
void main(){ vec3 N = normalize(vN); if (!gl_FrontFacing) N = -N; vec3 V = normalize(cameraPosition - vW); vec3 b = uCor * vC;
  float dl = smoothstep(.10, .96, dot(N, normalize(vec3(-.40, .80, .46))) * .5 + .5);
  float fr = pow(1.0 - clamp(dot(N, V), 0.0, 1.0), 3.0), alt = smoothstep(0.0, uAlt, vW.y);
  vec3 a = mix(b * vec3(.62, .70, .78) + vec3(.015, .03, .04), mix(b, vec3(1.0), .15), dl);
  a *= mix(.86, 1.05, alt); a += fr * uBri; a += b * uEmiC;
  vec3 e = b * (.09 + .10 * max(N.y, 0.0) + .13 * alt * alt) + vec3(.028, .036, .040);
  e += mix(vec3(.70, 1.0, .85), b, .35) * (fr * 1.15 + pow(1.0 - abs(N.y), 6.0) * .05); e += b * uEmi * mix(.62, 1.12, alt);
  vec3 c = mix(a, e, uClima); c = mix(c, uNevoa.rgb, uNevoa.a * smoothstep(14.0, 70.0, length(cameraPosition - vW)));
  gl_FragColor = vec4(c, uOp); }`;
const MC = new Map();
// mat('#50D088', { emi: brilho próprio no clima escuro, emiC: no claro, alt: altura do degradê (m), bri: brilho de borda, op })
export function mat(cor, o = {}) {
  const k = cor + JSON.stringify(o); if (MC.has(k) && !o.novo) return MC.get(k);
  const m = new THREE.ShaderMaterial({ vertexShader: VS, fragmentShader: FS, side: o.ds ? THREE.DoubleSide : THREE.FrontSide, transparent: (o.op ?? 1) < 1 || !!o.transp,
    uniforms: { uCor: { value: hex(cor) }, uClima: U.uClima, uNevoa: U.uNevoa, uEmi: { value: o.emi ?? 0 }, uEmiC: { value: o.emiC ?? 0 }, uAlt: { value: o.alt ?? 3 },
      uOp: { value: o.op ?? 1 }, uBri: { value: o.bri ?? .2 } } });
  MC.set(k, m); return m;
}
// formas: caixa de cantos redondos, cilindro, perfil extrudado (polígono com cantos redondos, extrudado em z)
export function caixa(w, h, d, r = .06) {
  r = Math.min(r, w / 2 - .001, h / 2 - .001, d / 2 - .001); const s = new THREE.Shape(), x = w / 2 - r, y = h / 2 - r;
  s.absarc(x, y, r, 0, PI / 2); s.absarc(-x, y, r, PI / 2, PI); s.absarc(-x, -y, r, PI, 1.5 * PI); s.absarc(x, -y, r, 1.5 * PI, 2 * PI);
  const g = new THREE.ExtrudeGeometry(s, { depth: d - 2 * r, bevelEnabled: true, bevelThickness: r, bevelSize: r, bevelOffset: -r, bevelSegments: 3, curveSegments: 5 });
  g.translate(0, 0, -(d - 2 * r) / 2); return g;
}
export function perfil(pts, r, prof, bisel = .05) {
  const n = pts.length, s = new THREE.Shape();
  for (let i = 0; i < n; i++) { const p0 = pts[(i + n - 1) % n], p1 = pts[i], p2 = pts[(i + 1) % n];
    const v1 = [p0[0] - p1[0], p0[1] - p1[1]], v2 = [p2[0] - p1[0], p2[1] - p1[1]], l1 = Math.hypot(...v1), l2 = Math.hypot(...v2);
    const rr = Math.min(Array.isArray(r) ? r[i] : r, l1 / 2, l2 / 2), a = [p1[0] + v1[0] / l1 * rr, p1[1] + v1[1] / l1 * rr], b = [p1[0] + v2[0] / l2 * rr, p1[1] + v2[1] / l2 * rr];
    if (i) s.lineTo(a[0], a[1]); else s.moveTo(a[0], a[1]); s.quadraticCurveTo(p1[0], p1[1], b[0], b[1]); }
  s.closePath();
  const g = new THREE.ExtrudeGeometry(s, { depth: prof - 2 * bisel, bevelEnabled: bisel > 0, bevelThickness: bisel, bevelSize: bisel, bevelOffset: -bisel, bevelSegments: 3, curveSegments: 6 });
  g.translate(0, 0, -(prof - 2 * bisel) / 2); return g;
}
export const cil = (r, h, seg = 28, r2 = r) => new THREE.CylinderGeometry(r2, r, h, seg);
export function malha(geo, m, pos = [0, 0, 0], pai = null, rot = null) { const o = new THREE.Mesh(geo, m); o.position.set(...pos); if (rot) o.rotation.set(...rot); if (pai) pai.add(o); return o; }
export function grupo(pai = CENA, pos = [0, 0, 0]) { const g = new THREE.Group(); g.position.set(...pos); pai.add(g); return g; }
// mancha no chão: sombra macia no claro (verde-escura), reflexo de luz no escuro. Sem mapa de sombra.
const FSM = `uniform float uClima, uOp; uniform vec3 uCorE; varying vec2 vU;
void main(){ float r = length(vU - .5) * 2.0, k = pow(smoothstep(1.0, 0.0, r), 1.7);
  vec4 c = mix(vec4(.08, .26, .18, .50 * k), vec4(uCorE, .36 * k), uClima); gl_FragColor = vec4(c.rgb, c.a * uOp); }`;
export function mancha(w, d, pos, o = {}) {
  const m = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, vertexShader: 'varying vec2 vU; void main(){ vU = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: FSM, uniforms: { uClima: U.uClima, uOp: { value: o.op ?? 1 }, uCorE: { value: hex(o.cor ?? '#50D088') } } });
  const q = malha(new THREE.PlaneGeometry(w, d), m, [pos[0], (pos[1] ?? 0) + .012, pos[2]], o.pai ?? CENA, [-PI / 2, 0, 0]); q.renderOrder = -5; return q;
}
// piso: disco grande que some nas bordas. Claro: branco com pontos miúdos (dá leitura ao movimento da câmera);
// escuro: malha de linhas verdes. o.r = raio, o.passo = distância dos pontos (m)
const FSP = `uniform float uClima, uR, uPasso, uOp; uniform vec2 uC; varying vec3 vW;
void main(){ vec2 p = vW.xz; float r = length(p - uC) / uR, borda = smoothstep(1.0, .25, r);
  vec2 g = abs(fract(p / uPasso - .5) - .5) * uPasso; float fw = fwidth(p.x) + fwidth(p.y);
  float ponto = 1.0 - smoothstep(.045, .045 + fw, length(g));
  float linha = 1.0 - smoothstep(.010, .010 + fw * .8, min(g.x, g.y));
  vec4 a = vec4(mix(vec3(1.0), vec3(.60, .72, .68), ponto * .55), (.70 + .30 * ponto) * borda);
  vec4 e = vec4(.42, .94, .66, (linha * .028 + ponto * .36 + .02) * borda * borda);
  vec4 c = mix(a, e, uClima); gl_FragColor = vec4(c.rgb, c.a * uOp); }`;
export function piso(o = {}) {
  const r = o.r ?? 26, m = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, vertexShader: 'varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader: FSP, uniforms: { uClima: U.uClima, uR: { value: r }, uPasso: { value: o.passo ?? 1.3 }, uOp: { value: 1 }, uC: { value: new THREE.Vector2(o.x ?? 0, o.z ?? 0) } } });
  const q = malha(new THREE.PlaneGeometry(2 * r, 2 * r), m, [o.x ?? 0, 0, o.z ?? 0], CENA, [-PI / 2, 0, 0]); q.renderOrder = -10; return q;
}
// anel no chão (destaque): cresce de a por d s e some
export function anel(r, pos, cor = '#50D088') {
  const m = new THREE.MeshBasicMaterial({ color: cor, transparent: true, opacity: 0, depthWrite: false });
  const q = malha(new THREE.RingGeometry(r - .07, r, 72), m, [pos[0], .03, pos[2]], CENA, [-PI / 2, 0, 0]); q.renderOrder = -4; return q;
}
export function destaque(an, t, a, d = 1.1) { const p = pr(t, a, d); an.material.opacity = (p > 0 && p < 1) ? .85 * Math.pow(1 - p, 1.4) : 0; an.scale.setScalar(.55 + .75 * eo5(p)); }

// ------------------------------------------------------------------ câmera: chaves, inércia de operador, estações
// Chave: [t, pose, curva]. pose = { x, y, z (para onde olha), d (distância; negativa = já atravessou o alvo), az, el
// (radianos), rol, oy (px: sobe o desenho), fov }. curva: 'eis' (padrão: arranca e para sem tranco), 'eio5', 'lin' ou função.
// O 4º item é opcional: { reta: true } leva a câmera em LINHA RETA até a pose (mergulho, travessia de um plano);
// { mira: curva } faz o olhar chegar antes do corpo (a câmera acha o alvo e depois vai).
let CK = [[0, { x: 0, y: 0, z: 0, d: 12, az: 0, el: .3 }]];
const PD = { x: 0, y: 0, z: 0, d: 12, az: 0, el: 0, rol: 0, oy: 0, fov: 26 };
export const camera = ck => { CK = ck.map(([t, p, c, o]) => [t, { ...PD, fov: OPC.fov, ...p }, c, o || {}]); };
const CURVA = { lin: x => x, eio, eio5, eis, eo5, eo };
const livre = k => { const ce = Math.cos(k.el); return { px: k.x + k.d * Math.sin(k.az) * ce, py: k.y + k.d * Math.sin(k.el), pz: k.z + k.d * Math.cos(k.az) * ce, az: k.az, el: k.el, rol: k.rol, oy: k.oy, fov: k.fov }; };
export const posCam = k => { const l = livre({ ...PD, ...k }); return [l.px, l.py, l.pz]; };   // onde a câmera fica numa pose
function poseBruta(t) {
  if (t > CK[0][0]) for (let i = 1; i < CK.length; i++) {
    const [t1, p1, c, o] = CK[i], [t0, p0] = CK[i - 1];
    if (t <= t1) { const q0 = (t - t0) / (t1 - t0), q = (typeof c === 'function' ? c : CURVA[c || 'eis'])(q0), k = {};
      if (o.reta) { const A = livre(p0), B = livre(p1), qm = o.mira ? o.mira(q0) : q; for (const n in A) k[n] = lerp(A[n], B[n], n[0] === 'p' ? q : qm); return k; }
      for (const n in p0) k[n] = lerp(p0[n], p1[n], q); return livre(k); }
  }
  return livre(t <= CK[0][0] ? CK[0][1] : CK[CK.length - 1][1]);
}
// curva de mergulho para um trecho { reta: true } que atravessa um plano: a distância até o plano cai em razão constante
// (o plano dobra de tamanho no quadro a cada tanto de tempo, sem dar tranco perto dele), com começo e fim macios.
// z0 = distância da câmera ao plano na saída; zf = na chegada (negativa = já do outro lado); c = folga (m) além de zf
export function mergulho(z0, zf, c = .5, o = {}) {
  const a = o.a ?? .2, b = o.b ?? .32, v = 1 / (1 - a / 2 - b / 2), k = c - zf;   // velocidade em trapézio: acelera em a, freia em b
  const s = u => u < a ? v * u * u / (2 * a) : u > 1 - b ? 1 - v * (1 - u) * (1 - u) / (2 * b) : v * (u - a / 2);
  return u => { u = cl(u); const z = Math.pow(z0 + k, 1 - s(u)) * Math.pow(zf + k, s(u)) - k; return (z0 - z) / (z0 - zf); };
}
// operador humano: média em sino das chaves (±inercia s) + respiração de milésimos de radiano. Função só de t.
export function pose(t) {
  const w = OPC.inercia; let k = {};
  if (w > 0 && CK.length > 1) { let s = 0;
    for (let i = -4; i <= 4; i++) { const g = 1 + Math.cos(PI * i / 5), p = poseBruta(t + i / 4 * w); s += g; for (const c in p) k[c] = (k[c] ?? 0) + g * p[c]; }
    for (const c in k) k[c] /= s; } else k = { ...poseBruta(t) };
  const r = OPC.respira; if (r) { k.az += r * (.0030 * Math.sin(t * .83 + 1.3) + .0014 * Math.sin(t * 1.9 + .4)); k.el += r * .0019 * Math.sin(t * .67 + 2.1); }
  return k;
}
export let POSE = null;
export const olho = () => [CAM.position.x, CAM.position.y, CAM.position.z];   // onde a câmera está neste quadro
function aplicaCam(k) {
  POSE = k; CAM.fov = k.fov; CAM.position.set(k.px, k.py, k.pz);
  CAM.rotation.set(-k.el, k.az, k.rol, 'YXZ'); CAM.setViewOffset(LARG, ALT, 0, k.oy, LARG, ALT); CAM.updateProjectionMatrix(); CAM.updateMatrixWorld(); CAM.matrixWorldInverse.copy(CAM.matrixWorld).invert();
}
const _v = new THREE.Vector3(), _v4 = new THREE.Vector4();
export function tela(p) { _v.set(p[0], p[1], p[2]).project(CAM); return [(_v.x + 1) * LARG / 2, (1 - _v.y) * ALT / 2]; }   // mundo → px
export function ancora(e, p, ax = .5, ay = 1, dx = 0, dy = 0) {   // prende um rótulo do HUD a um ponto do mundo
  if (e._w == null) { e._w = e.offsetWidth; e._h = e.offsetHeight; } const [x, y] = tela(p);
  e.style.left = (x - e._w * ax + dx).toFixed(1) + 'px'; e.style.top = (y - e._h * ay + dy).toFixed(1) + 'px';
}
// referencial: um "lugar" do espaço (posição + giro em y). Planos e poses de câmera podem ser dados dentro dele.
export function lugar(pos, az = 0, elv = 0) {
  const m = new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(-elv, az, 0, 'YXZ')).setPosition(pos[0], pos[1], pos[2]);
  const inv = m.clone().invert();
  return { m, az, el: elv, pos, local(q) { _v.set(q[0], q[1], q[2]).applyMatrix4(inv); return [_v.x, _v.y, _v.z]; }, p(q) { _v.set(q[0], q[1], q[2]).applyMatrix4(m); return [_v.x, _v.y, _v.z]; },
    pose(k) { const [x, y, z] = this.p([k.x ?? 0, k.y ?? 0, k.z ?? 0]); return { ...k, x, y, z, az: (k.az ?? 0) + az, el: (k.el ?? 0) + elv }; } };
}
// lugar cujo eixo z aponta de `alvo` para `olho`: o que estiver nele fica de frente para quem vem de `olho`
export function lugarDeFrente(alvo, olho) {
  const d = [olho[0] - alvo[0], olho[1] - alvo[1], olho[2] - alvo[2]], n = Math.hypot(...d);
  return lugar(alvo, Math.atan2(d[0], d[2]), Math.asin(d[1] / n));
}
// pose que enquadra um plano de frente: o plano ocupa `folga` da altura do quadro (1 = encosta em cima e embaixo)
export function enquadra(p, folga = .6, o = {}) {
  const h = p.h * p.esc, d = h / folga / (2 * Math.tan((o.fov ?? OPC.fov) * PI / 360)), c = p.centro();
  return { x: c[0], y: c[1], z: c[2], d, az: p.azMundo(), el: -p.rot[0] + (p.em ? p.em.el : 0), ...o };
}

// ------------------------------------------------------------------ planos HTML no espaço (a mesma câmera do 3D)
// plano(html, { pos, rot [rx, ry, rz], esc (metros por px), anc [ax, ay] (ponto do plano que fica em pos), clima, tras
// (atrás do 3D), em (lugar) }). Devolve p: p.e = o elemento (use vis/foco/pulso nele), p.pos e p.rot mexem por quadro,
// p.op = opacidade do plano inteiro, p.w/p.h px. Papéis (ver "Acabamento" no LEIA.md): tras = fundo macio (mancha, brilho,
// pontos); tras + deco = traço decorativo (anel, linha): fica numa camada que o motor RECORTA atrás de todo cartão de
// vidro, então nunca cruza conteúdo; deco sozinho = enfeite na frente (poeira de luz), fora da verificação; sobre = plano
// posto de propósito em cima de outro (selo na quina de um cartão); sangra = pode ser cortado pela borda do quadro.
const PLANOS = [];
const _m = new THREE.Matrix4(), _m2 = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _s = new THREE.Vector3(), _p = new THREE.Vector3();
export function plano(html, o = {}) {
  const pl = document.createElement('div'); pl.className = 'pl ' + (o.clima ?? 'claro'); pl.innerHTML = html.trim(); (o.tras ? (o.deco ? DC : TR) : FR).appendChild(pl); cabe(pl);
  const p = { pl, e: pl.firstElementChild, pos: [...(o.pos ?? [0, 0, 0])], rot: [...(o.rot ?? [0, 0, 0])], esc: o.esc ?? .011, anc: o.anc ?? [.5, .5], em: o.em ?? null, op: 1, z: o.z ?? 0,
    w: 0, h: 0, prof: 0, escTela: 0, tras: !!o.tras, deco: !!o.deco, sobre: !!o.sobre, sangra: !!o.sangra, M: new Float64Array(16), MW: new Float64Array(16), on: false, cx: null,
    mede() { this.w = pl.offsetWidth; this.h = pl.offsetHeight; return this; },
    ret() { const x0 = this.pos[0] - this.anc[0] * this.w * this.esc, y1 = this.pos[1] + this.anc[1] * this.h * this.esc; return [x0, y1 - this.h * this.esc, x0 + this.w * this.esc, y1]; },   // [x0, y0, x1, y1] em metros, no lugar do plano (plano sem giro)
    centro() { const m = matrizPlano(this); _v.set(this.w / 2, this.h / 2, 0).applyMatrix4(m); return [_v.x, _v.y, _v.z]; },
    ponto(u, v) { const m = matrizPlano(this); _v.set(u, v, 0).applyMatrix4(m); return [_v.x, _v.y, _v.z]; },   // px do plano → mundo
    azMundo() { return this.rot[1] + (this.em ? this.em.az : 0); },
    dist() { const c = this.centro(); return Math.hypot(c[0] - CAM.position.x, c[1] - CAM.position.y, c[2] - CAM.position.z); } };
  PLANOS.push(p); p.mede(); if (!p.tras && !p.deco) p.cx = contornos(pl); return p;
}
function matrizPlano(p) {
  _e.set(p.rot[0], p.rot[1], p.rot[2], 'YXZ'); _q.setFromEuler(_e); _p.set(p.pos[0], p.pos[1], p.pos[2]); _s.set(p.esc, -p.esc, p.esc);
  _m.compose(_p, _q, _s); _m2.makeTranslation(-p.anc[0] * p.w, -p.anc[1] * p.h, 0); _m.multiply(_m2); if (p.em) _m.premultiply(p.em.m); return _m;
}
const _pv = new THREE.Matrix4(), _c = new THREE.Matrix4();
function projeta() {
  _pv.multiplyMatrices(CAM.projectionMatrix, CAM.matrixWorldInverse);
  const f = ALT / 2 / Math.tan(CAM.fov * PI / 360);
  for (const p of PLANOS) {
    p.on = false; if (p.op <= .002) { p.pl.style.display = 'none'; continue; }
    _c.multiplyMatrices(_pv, matrizPlano(p)); const m = _c.elements; p.MW.set(_m.elements);   // colunas: u, v, z, t → linhas x, y, z, w do recorte
    // algum canto atrás (ou colado) da câmera: não desenha (quem atravessa a câmera some antes, por p.op)
    let wmin = 1e9, wc = 0; for (const [u, v] of [[0, 0], [p.w, 0], [0, p.h], [p.w, p.h]]) { const w = m[3] * u + m[7] * v + m[15]; wmin = Math.min(wmin, w); wc += w / 4; }
    if (wmin < .35) { p.pl.style.display = 'none'; continue; }
    const X = i => LARG / 2 * (m[i] + m[i + 3]), Y = i => ALT / 2 * (m[i + 3] - m[i + 1]);
    p.pl.style.display = ''; p.prof = wc; p.escTela = p.esc * f / wc; p.M.set(m); p.on = true;
    p.pl.style.transform = `matrix3d(${X(0)},${Y(0)},0,${m[3]},${X(4)},${Y(4)},0,${m[7]},0,0,1,0,${X(12)},${Y(12)},0,${m[15]})`;
    p.pl.style.opacity = p.op >= .999 ? '' : p.op.toFixed(4); p.pl.style.zIndex = String(Math.round(200000 - wc * 400 + p.z));
  }
  if (DC.childElementCount) furos();
}

// ------------------------------------------------------------------ clima do quadro e a cena
// clima(k): 0 = claro (dia), 1 = escuro (dados). Troca o fundo do quadro e o material do 3D. A troca acontece só numa
// passagem de câmera (quando um plano escuro cobre o quadro inteiro, ninguém vê a troca).
export function clima(k) { U.uClima.value = k; CE.style.opacity = k.toFixed(4); }
let RENDER = null;
export function cena(monta, o = {}) {
  window.setup = d => { D = d; Object.assign(OPC, o); base(); semente(OPC.semente); clima(0); GL.style.opacity = ''; camera([[0, PD]]); aplicaCam(pose(0)); RENDER = monta(d); quadro(0); return true; };
  window.R = t => { document.getElementById('aud')?.remove(); quadro(t); return true; };
  window.auditar = (t, op) => auditar(t, op);   // verificação de acabamento do quadro (ver "Acabamento" no LEIA.md e auditar.cjs)
}
function quadro(t) { aplicaCam(pose(t)); RENDER(t); projeta(); RD.render(CENA, CAM); }

// ------------------------------------------------------------------ biblioteca de objetos (objetos/*.js e dados/*.js)
// Só acréscimos: nada acima mudou. Formas a mais, lotes de peças iguais, material com desenho e CSS de componente.
export const pega = a => a[Math.floor(rng() * a.length)];
export const torno = (pts, seg = 28) => new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), seg);   // perfil [raio, y] de baixo para cima
export const esfera = (r, e = [1, 1, 1], seg = 20) => { const g = new THREE.SphereGeometry(r, seg, Math.max(8, Math.round(seg * .7))); g.scale(e[0], e[1], e[2]); return g; };
export const capsula = (r, h, seg = 12) => new THREE.CapsuleGeometry(r, h, 5, seg);
export const toro = (R, r, seg = 36, arco = 2 * PI) => new THREE.TorusGeometry(R, r, 8, seg, arco);
export function tubo(pts, r = .02, seg = 48) {   // tubo por uma curva suave que passa pelos pontos; g.userData.curva.getPoint(u)
  const c = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(p[0], p[1], p[2]))), g = new THREE.TubeGeometry(c, seg, r, 8, false); g.userData.curva = c; return g;
}
export function mundo(o, p = [0, 0, 0]) { o.updateWorldMatrix(true, false); _v.set(p[0], p[1], p[2]); o.localToWorld(_v); return [_v.x, _v.y, _v.z]; }   // ponto local → mundo
// lote: N peças iguais numa chamada de desenho (InstancedMesh). poeInst põe a peça i; a cor é a da tela (hex sem conversão)
const _lm = new THREE.Matrix4(), _lq = new THREE.Quaternion(), _le = new THREE.Euler(), _lp = new THREE.Vector3(), _ls = new THREE.Vector3(), _lc = new THREE.Color();
export function lote(geo, m, n, pai) { const im = new THREE.InstancedMesh(geo, m, n); im.frustumCulled = false; if (pai) pai.add(im); return im; }
export function poeInst(im, i, pos, rot = [0, 0, 0], esc = 1, cor = null) {
  _le.set(rot[0], rot[1], rot[2]); _lq.setFromEuler(_le); _lp.set(pos[0], pos[1], pos[2]); if (Array.isArray(esc)) _ls.set(esc[0], esc[1], esc[2]); else _ls.set(esc, esc, esc);
  im.setMatrixAt(i, _lm.compose(_lp, _lq, _ls)); im.instanceMatrix.needsUpdate = true;
  if (cor) { const h = parseInt(cor.slice(1), 16); im.setColorAt(i, _lc.setRGB((h >> 16 & 255) / 255, (h >> 8 & 255) / 255, (h & 255) / 255, THREE.LinearSRGBColorSpace)); im.instanceColor.needsUpdate = true; }
}
// pintura: material com um desenho de canvas (placa, visor de aparelho, cupom, letreiro). desenha(ctx, w, h) pinta; no clima
// escuro o desenho fica com o.emi do brilho (papel .5; tela de aparelho 1). m.userData.refaz(f) redesenha; uUV = recorte.
export function pintura(w, h, desenha, o = {}) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const ctx = cv.getContext('2d'), tx = new THREE.CanvasTexture(cv); tx.anisotropy = 8;
  const m = new THREE.ShaderMaterial({ side: o.ds ? THREE.DoubleSide : THREE.FrontSide, transparent: !!o.transp,
    vertexShader: 'uniform vec4 uUV; varying vec2 vU; void main(){ vU = uv * uUV.zw + uUV.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform sampler2D uMapa; uniform float uClima, uEmi, uEmiC; varying vec2 vU; void main(){ vec4 c = texture2D(uMapa, vU); gl_FragColor = vec4(mix(c.rgb * uEmiC, c.rgb * uEmi, uClima), c.a); }',
    uniforms: { uMapa: { value: tx }, uClima: U.uClima, uEmi: { value: o.emi ?? .5 }, uEmiC: { value: o.emiC ?? 1 }, uUV: { value: new THREE.Vector4(0, 0, 1, 1) } } });
  m.userData = { ctx, cv, refaz(f = desenha) { ctx.clearRect(0, 0, w, h); f(ctx, w, h); tx.needsUpdate = true; } }; m.userData.refaz(); return m;
}
// estilo: CSS de um componente, posto uma vez só (cada arquivo de dados/ traz o seu; lê as variáveis do clima do plano)
export function estilo(id, css) { if (document.getElementById('es-' + id)) return; const s = document.createElement('style'); s.id = 'es-' + id; s.textContent = css; document.head.appendChild(s); }

// ------------------------------------------------------------------ acabamento: o texto cabe, o enfeite fica atrás, o quadro é verificado
// Mínimos (px do desenho, a 1280x800): respiro do texto até a borda do cartão, margem até a borda do quadro, folga do
// título, respiro entre seta e cartão e entre caixas, velocidade (px/s) abaixo da qual um elemento conta como parado, e a
// faixa do "quase alinhado" (diferença maior que a tolerância e menor que o que seria um degrau de propósito).
export const RESP = { texto: 10, textoV: 2, borda: 40, titulo: 10, seta: 8, caixas: 8, parado: 40, alinha: [1.5, 6] };
const SEL = '.cartao,.chip,.visor,.op,.papel,.d-mo,.bo,[data-caixa]';   // o que é "caixa de conteúdo" num plano (data-caixa marca uma caixa própria da cena)
function* textosDe(c) {   // os textos que pertencem à caixa c (não os de uma caixa dentro dela), com o retângulo de cada um
  const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT), rg = document.createRange(), cx = c.matches(SEL) ? c : null; let n;
  while ((n = w.nextNode())) { if (!/\S/.test(n.nodeValue) || n.parentElement.closest(SEL) !== cx) continue; rg.selectNodeContents(n); const r = rg.getBoundingClientRect(); if (r.width > 0) yield { n, r }; }
}
// cabe: todo .cartao mede o próprio texto e cresce até sobrar o respiro mínimo à direita (texto nunca estoura nem encosta
// na borda). O plano() chama sozinho; chame de novo se trocar o texto de um cartão por outro mais comprido.
export function cabe(raiz) {
  for (const c of raiz.querySelectorAll('.cartao')) for (let k = 0; k < 3; k++) {
    const r = c.getBoundingClientRect(); if (!r.width) break;
    const lim = r.right - Math.max(parseFloat(getComputedStyle(c).paddingRight) || 0, RESP.texto); let mx = -1e9;
    for (const q of textosDe(c)) mx = Math.max(mx, q.r.right);
    if (mx <= lim + .5) break; const w0 = [c.style.width, c.style.minWidth]; c.style.width = c.style.minWidth = Math.ceil(r.width + mx - lim) + 'px';
    let m2 = -1e9; for (const q of textosDe(c)) m2 = Math.max(m2, q.r.right);   // texto preso à direita anda junto com a borda: crescer não resolve, desfaz
    if (m2 - mx > mx - lim - 1) { [c.style.width, c.style.minWidth] = w0; break; }
  }
}
function contornos(pl) {   // contorno (px do plano, cantos redondos) de cada caixa de conteúdo; medido na criação, sem transformação
  const o = pl.getBoundingClientRect(), L = [];
  for (const e of pl.querySelectorAll(SEL)) { if (e.parentElement.closest(SEL)) continue; const r = e.getBoundingClientRect(); if (!r.width) continue;
    const x = r.left - o.left, y = r.top - o.top, w = r.width, h = r.height, rr = Math.min(parseFloat(getComputedStyle(e).borderTopLeftRadius) || 0, w / 2, h / 2), c = [];
    for (const [cx, cy, a0] of [[x + w - rr, y + rr, -PI / 2], [x + w - rr, y + h - rr, 0], [x + rr, y + h - rr, PI / 2], [x + rr, y + rr, PI]]) for (let i = 0; i <= 3; i++) c.push([cx + rr * Math.cos(a0 + i * PI / 6), cy + rr * Math.sin(a0 + i * PI / 6)]);
    L.push({ e, c }); }
  return L;
}
const naTela = (m, u, v) => { const w = m[3] * u + m[7] * v + m[15]; return [LARG / 2 * ((m[0] * u + m[4] * v + m[12]) / w + 1), ALT / 2 * (1 - (m[1] * u + m[5] * v + m[13]) / w)]; };   // px do plano → px do quadro
function opInline(e, fim) { let k = 1; for (; e && e !== fim; e = e.parentElement) { const s = e.style; if (s.visibility === 'hidden' || s.display === 'none') return 0; if (s.opacity !== '') k *= +s.opacity; } return k; }
// furos: a camada dos traços decorativos (plano tras + deco) é recortada onde há caixa de vidro: o anel passa ATRÁS do cartão
function furos() {
  let d = ''; const visto = new Set();
  for (const p of PLANOS) { if (!p.on || !p.cx || p.op < .2 || !p.pl.classList.contains('escuro')) continue;
    for (const { e, c } of p.cx) { if (opInline(e, p.pl) * p.op < .2) continue; let s = '', k = '';
      c.forEach(([u, v], i) => { const [x, y] = naTela(p.M, u, v); s += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); if (i % 8 === 0) k += Math.round(x / 6) + ',' + Math.round(y / 6) + ';'; });
      if (!visto.has(k)) { visto.add(k); d += s + 'Z'; } } }   // dois cartões no mesmo lugar (troca por fusão) = um furo só
  const cp = d ? `path(evenodd,"M0 0H${LARG}V${ALT}H0Z${d}")` : ''; if (DC._cp !== cp) DC.style.clipPath = DC._cp = cp;
}
// enquadraRet: pose de frente que põe um retângulo do lugar (metros: [x0, y0, x1, y1]; use p.ret() e uneRet) INTEIRO na área
// útil do quadro. o: margem (px dos lados e de baixo; padrão 64 = os 40 da regra + folga para a deriva), topo (px livres
// para o título; padrão 150), max (teto de px por metro, para não fechar demais), z, az, el (do olhar, dentro do lugar).
export function enquadraRet(lg, ret, o = {}) {
  const mg = o.margem ?? 64, topo = o.topo ?? 150, chao = ALT - (o.base ?? mg), f = ALT / 2 / Math.tan((o.fov ?? OPC.fov) * PI / 360);
  const s = Math.min((LARG - 2 * mg) / (ret[2] - ret[0]), (chao - topo) / (ret[3] - ret[1]), o.max ?? 1e9);
  const k = { x: (ret[0] + ret[2]) / 2, y: (ret[1] + ret[3]) / 2 + ((topo + chao) / 2 - ALT / 2) / s, z: o.z ?? 0, d: f / s, az: o.az ?? 0, el: o.el ?? 0 };
  return lg ? lg.pose(k) : k;
}
export const uneRet = (...r) => [Math.min(...r.map(a => a[0])), Math.min(...r.map(a => a[1])), Math.max(...r.map(a => a[2])), Math.max(...r.map(a => a[3]))];

// auditar(t): a verificação automática do quadro. Devolve a lista de problemas [{ tipo, chave, msg, ret [x0, y0, x1, y1] }]:
//   texto     texto maior que a caixa (cartão, chip, visor, papel) ou a menos do respiro mínimo da borda dela
//   borda     caixa ou traço cortado pela borda do quadro, ou a menos de 40 px dela, estando PARADO (câmera parada ou fim de
//             movimento; o que cruza a borda em trânsito, a mais de 40 px/s, passa). plano(..., { sangra: true }) libera
//   titulo    caixa ou traço em cima do título (ou a menos de 10 px dele)
//   respiro   seta colada no cartão ou com respiro diferente nas duas pontas; fio que nem encosta nem afasta; caixas coladas
//   sobreposicao  duas caixas uma em cima da outra (plano(..., { sobre: true }) libera o selo posto de propósito na quina)
//   alinhamento   caixas vizinhas (planos paralelos do mesmo lugar) quase alinhadas: topo, meio ou base fora por 1,5 a 6 px
// Mede no desenho (px do plano, sem a perspectiva) e projeta com a câmera do quadro. o.marca: desenha os problemas no quadro.
function aoQuad(p, q) {   // distância (px do quadro) de um ponto ao quadrilátero de uma caixa na tela; 0 se está dentro
  let d = 1e9, sn = 0, den = true;
  for (let i = 0; i < 4; i++) { const a = q[i], b = q[(i + 1) % 4], vx = b[0] - a[0], vy = b[1] - a[1], wx = p[0] - a[0], wy = p[1] - a[1], cr = vx * wy - vy * wx;
    if (cr) { if (sn && Math.sign(cr) !== sn) den = false; sn = sn || Math.sign(cr); }
    const u = cl((wx * vx + wy * vy) / (vx * vx + vy * vy || 1)); d = Math.min(d, Math.hypot(wx - u * vx, wy - u * vy)); }
  return den ? 0 : d;
}
function opReal(e, fim) { let k = 1; for (; e; e = e.parentElement) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden') return 0; k *= +s.opacity; if (e === fim) break; } return k; }
const nomeDe = e => (e.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 34) || e.className || e.tagName;
function coleta(leve) {
  const A = PLANOS.filter(p => p.on && !p.tras && !p.deco && p.op > .12), tf = A.map(p => p.pl.style.transform), B = [], Ln = [], Tx = [];
  A.forEach(p => { p.pl.style.transform = 'none'; });
  for (const [p, raiz] of [...A.map(p => [p, p.pl]), [null, HUD]]) {
    const o = p ? raiz.getBoundingClientRect() : { left: 0, top: 0 }, rel = r => [r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top];
    let els = [...raiz.querySelectorAll(SEL)].filter(e => !e.closest('.tit'));
    if (p && !els.length && p.e && p.e.tagName !== 'svg' && /\S/.test(p.e.textContent)) els = [p.e];
    if (!p) els.push(...[...HUD.children].filter(e => !e.matches('.tit,' + SEL) && /\S/.test(e.textContent)));
    for (const e of els) { const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue; const op = opReal(e, raiz); if (op < .12) continue;
      const b = { e, p, op, l: rel(r), nome: nomeDe(e), impl: !e.matches(SEL), filho: !!e.parentElement.closest(SEL), k: p ? p.escTela : 1, pulsa: !!(e.style.scale || (p && p.e.style.scale)) }; B.push(b);   // pulsa = no meio de um pulso(): o respiro não é medido
      if (!b.impl && !leve) for (const { n, r: q } of textosDe(e)) if (opReal(n.parentElement, e) >= .05) Tx.push({ b, txt: n.nodeValue.replace(/\s+/g, ' ').trim().slice(0, 30), l: rel(q) }); }
    for (const sv of raiz.querySelectorAll('svg.seta,svg.fluxo')) { const op = opReal(sv, raiz); if (op < .12) continue;
      const r = sv.getBoundingClientRect(), vb = sv.viewBox.baseVal, kx = vb.width ? r.width / vb.width : 1, ky = vb.height ? r.height / vb.height : 1, seta = sv.classList.contains('seta');
      const loc = q => [r.left - o.left + (q.x - vb.x) * kx, r.top - o.top + (q.y - vb.y) * ky];
      for (const ph of sv.querySelectorAll(seta ? '.sb' : '.fb')) { const n = ph.getTotalLength(); if (!(n > 0)) continue; const a = loc(ph.getPointAtLength(0)); let z = loc(ph.getPointAtLength(n));
        const sp = seta && sv.querySelector('.sp'); if (sp) { const m = sp.getTotalLength(); let fd = Math.hypot(z[0] - a[0], z[1] - a[1]); for (const u of [0, .25, .5, .75, 1]) { const q = loc(sp.getPointAtLength(m * u)), dd = Math.hypot(q[0] - a[0], q[1] - a[1]); if (dd > fd) { fd = dd; z = q; } } }
        Ln.push({ e: ph, p, op, seta, a, z, hw: (parseFloat(ph.getAttribute('stroke-width')) || 2) / 2, k: p ? p.escTela : 1, nome: seta ? 'seta' : 'fio' }); } }
  }
  A.forEach((p, i) => { p.pl.style.transform = tf[i]; });
  const T = (p, u, v) => p ? naTela(p.M, u, v) : [u, v];
  for (const b of B) { const q = [[b.l[0], b.l[1]], [b.l[2], b.l[1]], [b.l[2], b.l[3]], [b.l[0], b.l[3]]].map(([u, v]) => T(b.p, u, v)), xs = q.map(a => a[0]), ys = q.map(a => a[1]);
    b.q = q; b.s = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; b.c = [(b.s[0] + b.s[2]) / 2, (b.s[1] + b.s[3]) / 2]; }
  for (const l of Ln) { l.sa = T(l.p, ...l.a); l.sz = T(l.p, ...l.z); l.s = [Math.min(l.sa[0], l.sz[0]), Math.min(l.sa[1], l.sz[1]), Math.max(l.sa[0], l.sz[0]), Math.max(l.sa[1], l.sz[1])]; l.c = [(l.s[0] + l.s[2]) / 2, (l.s[1] + l.s[3]) / 2]; }
  return { B, Ln, Tx };
}
export function auditar(t, o = {}) {
  const R = RESP, dt = .3, P = [], visto = new Set();
  const add = (tipo, chave, msg, s) => { chave = tipo + ': ' + chave; if (visto.has(chave)) return; visto.add(chave); P.push({ tipo, chave, msg, ret: s.map(v => Math.round(v)) }); };
  // parado = quase não anda na tela de t - 0,3 a t + 0,3 s (câmera parada, deriva lenta ou fim de movimento seguido de pausa)
  const onde = u => { quadro(u); const a = coleta(true), m = new Map(); for (const b of [...a.B, ...a.Ln]) m.set(b.e, b.c); return m; }, antes = onde(t - dt), depois = onde(t + dt);
  quadro(t); const { B, Ln, Tx } = coleta(), f1 = v => (Math.round(v * 10) / 10).toString().replace('.', ',');
  for (const b of [...B, ...Ln]) b.parado = [antes, depois].every(m => { const a = m.get(b.e); return !!a && Math.hypot(b.c[0] - a[0], b.c[1] - a[1]) / dt <= R.parado; });
  // 1 · texto na caixa
  for (const x of Tx) { const b = x.b.l, q = x.l, h = Math.max(b[0] + R.texto - q[0], q[2] - (b[2] - R.texto)), v = Math.max(b[1] + R.textoV - q[1], q[3] - (b[3] - R.textoV));
    if (Math.max(h, v) > .75) add('texto', x.b.nome + ' | ' + x.txt, `o texto "${x.txt}" ${h > v ? (h > R.texto ? 'estoura a largura' : 'encosta na borda') : 'estoura a altura'} de "${x.b.nome}" (faltam ${f1(Math.max(h, v))} px para o respiro de ${h > v ? R.texto : R.textoV} px)`, x.b.s); }
  // 2 · borda do quadro (só o que está parado)
  const livre = s => s[2] <= 0 || s[3] <= 0 || s[0] >= LARG || s[1] >= ALT, falta = s => Math.max(R.borda - s[0], R.borda - s[1], s[2] - (LARG - R.borda), s[3] - (ALT - R.borda));
  for (const b of [...B, ...Ln]) { if (b.filho || !b.parado || (b.p && b.p.sangra) || livre(b.s)) continue; const m = falta(b.s); if (m <= .75) continue;
    const lado = m === R.borda - b.s[0] ? 'esquerda' : m === R.borda - b.s[1] ? 'de cima' : m === b.s[2] - (LARG - R.borda) ? 'direita' : 'de baixo';
    add('borda', b.nome + (b.seta != null ? ' @' + Math.round(b.c[0] / 40) + ',' + Math.round(b.c[1] / 40) : ''), `"${b.nome}" ${m > R.borda ? `cortado pela borda ${lado} do quadro (${f1(m - R.borda)} px para fora)` : `a ${f1(R.borda - m)} px da borda ${lado} (mínimo ${R.borda})`}`, b.s); }
  // 3 · título
  const rg = document.createRange();
  for (const tt of HUD.querySelectorAll('.tit')) { if (opReal(tt, HUD) < .3) continue;
    for (const pt of tt.children) { if (opReal(pt, tt) < .3) continue; rg.selectNodeContents(pt); const r = rg.getBoundingClientRect(), g = R.titulo;
      for (const b of [...B, ...Ln]) if (!b.filho && b.op >= .3 && b.s[0] < r.right + g && b.s[2] > r.left - g && b.s[1] < r.bottom + g && b.s[3] > r.top - g)
        add('titulo', b.nome, `"${b.nome}" em cima do título "${nomeDe(tt)}" (ou a menos de ${g} px dele)`, b.s); } }
  // 4 · respiro: seta e fio contra a caixa mais próxima de cada ponta; caixas entre si
  const Bv = B.filter(b => !b.filho && b.op >= .3);
  for (const l of Ln) { if (!l.parado) continue;
    const g = [l.sa, l.sz].map(q => { let m = 1e9, bb = null; for (const b of Bv) { const d = aoQuad(q, b.q); if (d < m) { m = d; bb = b; } } return [Math.max(0, m / l.k - l.hw), bb]; });
    if (g.some(([, b]) => b && (!b.parado || b.pulsa))) continue;
    const chave = l.nome + ' ' + g.map(([, b]) => b ? b.nome : '').join(' > '), perto = g.filter(([d, b]) => b && d < 30 && (l.seta || d > .75));
    for (const [d, b] of perto) if (d < R.seta - .5) add('respiro', chave + ' | ' + b.nome, `${l.nome} ${l.seta ? 'colada em' : 'nem encostado nem afastado de'} "${b.nome}": respiro de ${f1(d)} px (mínimo ${R.seta}${l.seta ? '' : ', ou encostar'})`, l.s);
    if (perto.length === 2 && Math.abs(perto[0][0] - perto[1][0]) > (l.seta ? 2 : 3)) add('respiro', chave + ' | desigual', `${l.nome} com respiro desigual: ${f1(perto[0][0])} px de "${perto[0][1].nome}" e ${f1(perto[1][0])} px de "${perto[1][1].nome}"`, l.s); }
  const Bp = Bv.filter(b => b.op >= .5 && b.parado && !b.pulsa), sobre = b => b.p && b.p.sobre;
  for (let i = 0; i < Bp.length; i++) for (let j = i + 1; j < Bp.length; j++) { const a = Bp[i], b = Bp[j]; if (a.e.contains(b.e) || b.e.contains(a.e) || sobre(a) || sobre(b)) continue;
    const ix = Math.min(a.s[2], b.s[2]) - Math.max(a.s[0], b.s[0]), iy = Math.min(a.s[3], b.s[3]) - Math.max(a.s[1], b.s[1]), k = Math.min(a.k, b.k), u = [Math.min(a.s[0], b.s[0]), Math.min(a.s[1], b.s[1]), Math.max(a.s[2], b.s[2]), Math.max(a.s[3], b.s[3])];
    if (ix > 1.5 && iy > 1.5) { const ar = q => (q.s[2] - q.s[0]) * (q.s[3] - q.s[1]); if (ix * iy / (ar(a) + ar(b) - ix * iy) < .8) add('sobreposicao', a.nome + ' | ' + b.nome, `"${a.nome}" e "${b.nome}" sobrepostos (${f1(Math.min(ix, iy) / k)} px)`, u); }
    else { const gp = iy > 1.5 ? -ix : ix > 1.5 ? -iy : 1e9; if (gp / k < R.caixas - .5) add('respiro', a.nome + ' | ' + b.nome, `"${a.nome}" e "${b.nome}" colados: ${f1(Math.max(0, gp / k))} px (mínimo ${R.caixas})`, u); }
    // 5 · alinhamento: só entre planos paralelos do mesmo lugar, na mesma profundidade e vizinhos (mede no espaço, não na tela)
    if (!a.p || !b.p || a.p.em !== b.p.em || a.p.rot.some((v, n) => Math.abs(v - b.p.rot[n]) > 1e-6)) continue;
    const no = q => { const m = q.p.MW, c = [[q.l[0], q.l[1]], [q.l[2], q.l[1]], [q.l[2], q.l[3]], [q.l[0], q.l[3]]].map(([u2, v2]) => { const w = [m[0] * u2 + m[4] * v2 + m[12], m[1] * u2 + m[5] * v2 + m[13], m[2] * u2 + m[6] * v2 + m[14]]; return q.p.em ? q.p.em.local(w) : w; });
      return [Math.min(...c.map(w => w[0])), Math.min(...c.map(w => w[1])), Math.max(...c.map(w => w[0])), Math.max(...c.map(w => w[1])), c[0][2]]; };
    const ra = no(a), rb = no(b), px = Math.max(a.p.esc, b.p.esc), [lo, hi] = R.alinha; if (Math.abs(ra[4] - rb[4]) > .7) continue;
    for (const [i0, i1, eixo] of [[1, 3, 'na horizontal'], [0, 2, 'na vertical']]) { const j0 = 1 - i0, j1 = j0 + 2, vao = Math.max(ra[j0], rb[j0]) - Math.min(ra[j1], rb[j1]);   // vizinhos nesse eixo: não se cruzam no outro e estão perto
      if (vao < 0 || vao / px > 320) continue; const ov = Math.min(ra[i1], rb[i1]) - Math.max(ra[i0], rb[i0]); if (ov < .5 * Math.min(ra[i1] - ra[i0], rb[i1] - rb[i0])) continue;
      const ta = ra[i1] - ra[i0], tb = rb[i1] - rb[i0], meio = Math.abs(ra[i0] + ra[i1] - rb[i0] - rb[i1]) / 2;   // bordas só se comparam entre caixas de tamanho parecido; o meio, sempre
      const dd = (Math.min(ta, tb) / Math.max(ta, tb) > .6 ? Math.min(Math.abs(ra[i0] - rb[i0]), Math.abs(ra[i1] - rb[i1]), meio) : meio) / px;
      if (dd > lo && dd < hi) add('alinhamento', a.nome + ' | ' + b.nome, `"${a.nome}" e "${b.nome}" quase alinhados ${eixo}: fora por ${f1(dd)} px`, u); } }
  if (o.marca) { document.getElementById('aud')?.remove(); const d = el('<div id="aud" style="position:absolute;left:0;top:0;width:' + LARG + 'px;height:' + ALT + 'px;z-index:9"></div>', ST);
    for (const q of P) d.insertAdjacentHTML('beforeend', `<div style="position:absolute;left:${q.ret[0]}px;top:${q.ret[1]}px;width:${q.ret[2] - q.ret[0]}px;height:${q.ret[3] - q.ret[1]}px;outline:2px solid #FF3B5C;outline-offset:2px"><span style="position:absolute;left:-2px;top:-19px;font:700 11px M,sans-serif;color:#fff;background:#FF3B5C;padding:1px 6px;border-radius:3px;white-space:nowrap">${q.tipo}</span></div>`); }
  return P;
}
