// Moeda e saldo: a moeda do kit (dourada, com o cifrão, desenho próprio) e o cartão de saldo, com a pilha de moedas que
// cai e o número que conta. Para dinheiro em conta, saldo do cliente, a receber, crédito do fornecedor.
// uso: const s = plano(htmlSaldo({ rot: 'Saldo em conta', sub: 'depois do pagamento', valor: 4354, moedas: 5 }), { pos, esc, clima: 'escuro' });
//      saldo(s.e, t, a, b, { de: 0, tConta });   ·   solta: plano(htmlMoeda({ px: 64 })) + moeda(p.e, t, a) (entra girando)
// o: w (340), fmt (padrão R$), cor ('' verde = positivo | 'v' negativo: o número fica vermelho), res (true: cartão de resultado).
import { vis, pr, eo, eo5, passa, golpe, lerp, estilo, PI } from '../motor.js';
import { base, pt, entra, reais as R0 } from './base.js';
const reais = v => (v < 0 ? '− ' : '') + R0(Math.abs(v));
const CSS = `
.d-mo{position:relative;border-radius:50%;background:radial-gradient(circle at 34% 28%,#FFE9A6 0%,#F7C95A 38%,#E3A02A 78%,#C98416 100%);box-shadow:inset 0 -3px 0 rgba(150,90,0,.35),inset 0 2px 0 rgba(255,255,255,.65),0 8px 16px -5px rgba(160,100,10,.55);
  display:flex;align-items:center;justify-content:center;font-weight:800;color:#9A6408;flex:none}
.d-mo:before{content:"";position:absolute;inset:11%;border-radius:50%;border:1.5px solid rgba(154,100,8,.45)}
.d-sal{padding:20px 22px;display:flex;align-items:center;gap:20px}.d-sal .pi{position:relative;width:64px;flex:none}.d-sal .pi .d-mo{position:absolute;left:0;height:22px!important;border-radius:50%/50%;font-size:0!important}
.d-sal .pi .d-mo:before{display:none}.d-sal .num{font-size:31px;margin-top:7px}.d-sal.v .num{background-image:linear-gradient(100deg,var(--vm),var(--vm));filter:none}`;
export const htmlMoeda = (o = {}) => { base(); estilo('d-mo', CSS); const px = o.px ?? 64; return `<div class="d-mo" style="width:${px}px;height:${px}px;font-size:${Math.round(px * .46)}px">${o.txt ?? '$'}</div>`; };
export function moeda(e, t, a, b = 1e9) { vis(e, t, a, b, { dy: -26, sc: 1 }); const p = pr(t, a, .7); e.style.rotate = ''; e.style.scale = `${Math.cos(PI * 3 * (1 - eo5(p))).toFixed(4)} 1`; }
export function htmlSaldo(o = {}) {
  base(); estilo('d-mo', CSS); const n = o.moedas ?? 5, fmt = o.fmt ?? reais;
  return `<div class="cartao d-sal ${o.res ? 'res' : ''} ${o.cor === 'v' ? 'v' : ''}" style="position:relative;width:${o.w ?? 340}px"><div class="pi" style="height:${22 + (n - 1) * 9}px">${[...Array(n)].map((_, i) => `<div class="d-mo" style="width:64px;bottom:${i * 9}px;margin-left:${[0, 3, -2, 2, -3, 1][i % 6]}px"></div>`).join('')}</div>
    <div><div class="d-t">${o.rot ?? ''}</div><div class="d-s">${o.sub ?? ''}</div><div class="num r" data-v="${typeof o.valor === 'number' ? o.valor : ''}">${typeof o.valor === 'number' ? fmt(o.valor) : o.valor ?? ''}</div></div>${o.res ? '<div class="onda"></div>' : ''}</div>`;
}
export function saldo(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 24, sc: .96 }); const fmt = o.fmt ?? reais, n = pt(e, '.num')[0], v = parseFloat(n.dataset.v), tc = o.tConta ?? a + .45;
  if (!isNaN(v)) { const s = fmt(lerp(o.de ?? 0, v, eo5(pr(t, tc, o.d ?? .9)))); if (n.textContent !== s) n.textContent = s; }
  pt(e, '.pi .d-mo').forEach((m, i) => { const ti = (o.tMoedas ?? a + .3) + i * .11, p = pr(t, ti, .34), q = pr(t, ti + .34, .3); m.style.opacity = eo(pr(t, ti, .1)).toFixed(3);
    m.style.transform = `translateY(${(-46 * (1 - p * p) - 3 * Math.abs(golpe(q, 1, 3))).toFixed(2)}px)`; });
}
