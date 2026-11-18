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
const CSS = [500, 600, 700, 800].map(w => ff(w) + ff(w, 1)).join('') + `
:root{--v:#50D088;--ve:#2E7D57;--vc:#6CF0A8;--a:#F2B63D;--r1:12px;--r2:16px;--r3:22px;--rp:999px}
*{box-sizing:border-box;margin:0;padding:0;transition:none!important;animation:none!important}
html,body{width:1280px;height:800px;overflow:hidden;background:#F4F7F6}
body{font-family:M,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
#st,#cu,#ce,#tr,#fr,#hud{position:absolute;left:0;top:0;width:1280px;height:800px;overflow:hidden;isolation:isolate}
#gl{position:absolute;left:0;top:0;width:1280px;height:800px}
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
.tit{position:absolute;left:0;top:0;width:1280px;text-align:center}
.kick{font-weight:700;font-size:14px;letter-spacing:.3em;color:var(--kick);text-transform:uppercase;white-space:nowrap}
.h{display:inline-block;margin-top:10px;font-weight:800;font-size:46px;letter-spacing:-.02em;line-height:1.14;white-space:nowrap;padding:0 4px 3px;
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

export let ST = null, GL = null, TR = null, FR = null, HUD = null, CE = null;
{ const s = document.createElement('style'); s.textContent = CSS; document.head.prepend(s);
  document.body.insertAdjacentHTML('afterbegin', '<div id="st"><div id="cu"></div><div id="ce"></div><div id="tr"></div><canvas id="gl" width="1280" height="800"></canvas><div id="fr"></div><div id="hud"></div></div>');
  const q = i => document.getElementById(i); ST = q('st'); GL = q('gl'); TR = q('tr'); FR = q('fr'); HUD = q('hud'); CE = q('ce'); }

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
  vis(e, t, a, sai, { dy: 14 }); const p = eio5(pr(t, sobe - .05, .85)), y0 = o.y0 ?? 318, y1 = o.y1 ?? 44;
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
    RD.setPixelRatio(Math.min(window.devicePixelRatio || 1, OPC.pr)); RD.setSize(1280, 800, false); RD.setClearColor(0x000000, 0);
    RD.outputColorSpace = THREE.LinearSRGBColorSpace;   // as cores do material já são as da tela (hex da marca sem conversão)
  }
  CENA = new THREE.Scene(); CAM = new THREE.PerspectiveCamera(OPC.fov, 1280 / 800, .2, 400);
  PLANOS.length = 0; TR.innerHTML = ''; FR.innerHTML = ''; HUD.innerHTML = ''; MC.clear();
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
  CAM.rotation.set(-k.el, k.az, k.rol, 'YXZ'); CAM.setViewOffset(1280, 800, 0, k.oy, 1280, 800); CAM.updateProjectionMatrix(); CAM.updateMatrixWorld(); CAM.matrixWorldInverse.copy(CAM.matrixWorld).invert();
}
const _v = new THREE.Vector3(), _v4 = new THREE.Vector4();
export function tela(p) { _v.set(p[0], p[1], p[2]).project(CAM); return [(_v.x + 1) * 640, (1 - _v.y) * 400]; }   // mundo → px
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
// p.op = opacidade do plano inteiro, p.w/p.h px.
const PLANOS = [];
const _m = new THREE.Matrix4(), _m2 = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _s = new THREE.Vector3(), _p = new THREE.Vector3();
export function plano(html, o = {}) {
  const pl = document.createElement('div'); pl.className = 'pl ' + (o.clima ?? 'claro'); pl.innerHTML = html.trim(); (o.tras ? TR : FR).appendChild(pl);
  const p = { pl, e: pl.firstElementChild, pos: [...(o.pos ?? [0, 0, 0])], rot: [...(o.rot ?? [0, 0, 0])], esc: o.esc ?? .011, anc: o.anc ?? [.5, .5], em: o.em ?? null, op: 1, z: o.z ?? 0,
    w: 0, h: 0, prof: 0, escTela: 0,
    mede() { this.w = pl.offsetWidth; this.h = pl.offsetHeight; return this; },
    centro() { const m = matrizPlano(this); _v.set(this.w / 2, this.h / 2, 0).applyMatrix4(m); return [_v.x, _v.y, _v.z]; },
    ponto(u, v) { const m = matrizPlano(this); _v.set(u, v, 0).applyMatrix4(m); return [_v.x, _v.y, _v.z]; },   // px do plano → mundo
    azMundo() { return this.rot[1] + (this.em ? this.em.az : 0); },
    dist() { const c = this.centro(); return Math.hypot(c[0] - CAM.position.x, c[1] - CAM.position.y, c[2] - CAM.position.z); } };
  PLANOS.push(p); return p.mede();
}
function matrizPlano(p) {
  _e.set(p.rot[0], p.rot[1], p.rot[2], 'YXZ'); _q.setFromEuler(_e); _p.set(p.pos[0], p.pos[1], p.pos[2]); _s.set(p.esc, -p.esc, p.esc);
  _m.compose(_p, _q, _s); _m2.makeTranslation(-p.anc[0] * p.w, -p.anc[1] * p.h, 0); _m.multiply(_m2); if (p.em) _m.premultiply(p.em.m); return _m;
}
const _pv = new THREE.Matrix4(), _c = new THREE.Matrix4();
function projeta() {
  _pv.multiplyMatrices(CAM.projectionMatrix, CAM.matrixWorldInverse);
  const f = 400 / Math.tan(CAM.fov * PI / 360);
  for (const p of PLANOS) {
    if (p.op <= .002) { p.pl.style.display = 'none'; continue; }
    _c.multiplyMatrices(_pv, matrizPlano(p)); const m = _c.elements;   // colunas: u, v, z, t → linhas x, y, z, w do recorte
    // algum canto atrás (ou colado) da câmera: não desenha (quem atravessa a câmera some antes, por p.op)
    let wmin = 1e9, wc = 0; for (const [u, v] of [[0, 0], [p.w, 0], [0, p.h], [p.w, p.h]]) { const w = m[3] * u + m[7] * v + m[15]; wmin = Math.min(wmin, w); wc += w / 4; }
    if (wmin < .35) { p.pl.style.display = 'none'; continue; }
    const X = i => 640 * (m[i] + m[i + 3]), Y = i => 400 * (m[i + 3] - m[i + 1]);
    p.pl.style.display = ''; p.prof = wc; p.escTela = p.esc * f / wc;
    p.pl.style.transform = `matrix3d(${X(0)},${Y(0)},0,${m[3]},${X(4)},${Y(4)},0,${m[7]},0,0,1,0,${X(12)},${Y(12)},0,${m[15]})`;
    p.pl.style.opacity = p.op >= .999 ? '' : p.op.toFixed(4); p.pl.style.zIndex = String(Math.round(200000 - wc * 400 + p.z));
  }
}

// ------------------------------------------------------------------ clima do quadro e a cena
// clima(k): 0 = claro (dia), 1 = escuro (dados). Troca o fundo do quadro e o material do 3D. A troca acontece só numa
// passagem de câmera (quando um plano escuro cobre o quadro inteiro, ninguém vê a troca).
export function clima(k) { U.uClima.value = k; CE.style.opacity = k.toFixed(4); }
let RENDER = null;
export function cena(monta, o = {}) {
  window.setup = d => { D = d; Object.assign(OPC, o); base(); semente(OPC.semente); clima(0); GL.style.opacity = ''; camera([[0, PD]]); aplicaCam(pose(0)); RENDER = monta(d); quadro(0); return true; };
  window.R = t => { quadro(t); return true; };
}
function quadro(t) { aplicaCam(pose(t)); RENDER(t); projeta(); RD.render(CENA, CAM); }
