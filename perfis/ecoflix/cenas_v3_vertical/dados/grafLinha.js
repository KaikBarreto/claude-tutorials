// Gráfico de linha simples (preço do material no tempo, saldo do caixa, estoque): a linha se desenha da esquerda para a
// direita, a área embaixo acende, e o último ponto ganha o valor.
// uso: const g = plano(htmlGrafLinha({ titulo: 'Preço do cobre', sub: 'R$ por kg', pontos: [41, 42.5, 42, 44, 46.2, 45.8, 48], rotulos: ['jun', 'jul', 'ago', 'set', 'out', 'nov'], valor: 'R$ 48,00' }), { pos, esc, clima: 'escuro' });
//      grafLinha(g.e, t, a, b, { d: 1.4 });   ·   o: w (420), h (170), selo (ícone), suave (true), min, max
import { selo, vis, pr, eo, eio, estilo, golpe } from '../motor.js';
import { base, pt, entra } from './base.js';
export function htmlGrafLinha(o = {}) {
  base(); estilo('d-lin', `
.d-lin{padding:20px 22px 16px}.d-lin .top{display:flex;align-items:center;gap:12px}.d-lin .top .num{margin-left:auto;font-size:26px}
.d-lin svg{display:block;margin-top:16px;overflow:visible}.d-lin .rs{display:flex;justify-content:space-between;margin-top:8px}.d-lin .rs span{font-weight:700;font-size:12.5px;color:var(--tx2)}`);
  const P = o.pontos ?? [], W = (o.w ?? 420) - 44, H = o.h ?? 170, mn = o.min ?? Math.min(...P), mx = o.max ?? Math.max(...P), am = (mx - mn) || 1;
  const X = i => 6 + i * (W - 12) / (P.length - 1), Y = v => H - 10 - (v - mn) / am * (H - 30), pts = P.map((v, i) => [X(i), Y(v)]);
  let d = `M${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`; for (let i = 1; i < pts.length; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], k = o.suave === false ? 0 : (x1 - x0) * .42; d += `C${(x0 + k).toFixed(1)} ${y0.toFixed(1)} ${(x1 - k).toFixed(1)} ${y1.toFixed(1)} ${x1.toFixed(1)} ${y1.toFixed(1)}`; }
  const id = 'gl' + Math.abs(P.reduce((s, v, i) => s + v * (i + 3) * 131, W) | 0), U = pts[pts.length - 1];
  return `<div class="cartao d-lin" style="position:relative;width:${o.w ?? 420}px">
    <div class="top">${o.selo ? selo(o.selo, o.cor ?? '', 44) : ''}<div><div class="d-t">${o.titulo ?? ''}</div><div class="d-s">${o.sub ?? ''}</div></div>${o.valor ? `<span class="num r">${o.valor}</span>` : ''}</div>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" fill="none"><defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#50D088" stop-opacity=".34"/><stop offset="1" stop-color="#50D088" stop-opacity="0"/></linearGradient>
      <clipPath id="${id}c"><rect class="cl" x="0" y="-10" width="0" height="${H + 20}"/></clipPath></defs>
      ${[0, 1, 2, 3].map(i => `<path d="M0 ${(H - 10 - i * (H - 30) / 3).toFixed(1)}H${W}" stroke="var(--ln)" stroke-width="1"/>`).join('')}
      <path d="${d}L${U[0].toFixed(1)} ${H}L${pts[0][0].toFixed(1)} ${H}Z" fill="url(#${id})" clip-path="url(#${id}c)"/>
      <path class="tr" d="${d}" stroke="var(--ac)" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <circle class="ha" cx="${U[0].toFixed(1)}" cy="${U[1].toFixed(1)}" r="13" fill="#50D088" opacity="0"/><circle class="po" cx="${U[0].toFixed(1)}" cy="${U[1].toFixed(1)}" r="6" fill="#fff" stroke="var(--ac)" stroke-width="3" opacity="0"/></svg>
    <div class="rs">${(o.rotulos ?? []).map(r => `<span>${r}</span>`).join('')}</div></div>`;
}
export function grafLinha(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 24, sc: .96 }); const d = o.d ?? 1.3, t0 = o.tLinha ?? a + .35, p = eio(pr(t, t0, d)), tr = pt(e, '.tr')[0], W = +pt(e, ':scope > svg')[0].getAttribute('width');
  tr.setAttribute('stroke-dashoffset', (1 - p).toFixed(4)); const len = tr._len ?? (tr._len = tr.getTotalLength()), q = tr.getPointAtLength(len * p); pt(e, '.cl')[0].setAttribute('width', (p >= 1 ? W + 10 : q.x).toFixed(1));
  const f = pr(t, t0 + d - .1, .6), k = eo(pr(t, t0 + d - .1, .25)); pt(e, '.po')[0].setAttribute('opacity', k.toFixed(3)); pt(e, '.po')[0].setAttribute('r', (6 * (1 + .5 * golpe(f, 1.1, 3.4))).toFixed(2));
  const ha = pt(e, '.ha')[0]; ha.setAttribute('opacity', (f > 0 && f < 1 ? .5 * (1 - f) : 0).toFixed(3)); ha.setAttribute('r', (8 + 22 * eo(f)).toFixed(1));
  for (const n of pt(e, '.top .num')) entra(n, t, t0 + d - .15, { dy: 6 }); pt(e, '.rs span').forEach((x, i, L) => { x.style.opacity = eo(pr(t, t0 + d * i / L.length, .3)).toFixed(3); });
}
