// Fluxo com setas entre cartões (o caminho do dado no sistema: Ticket → Nota → Estoque → Financeiro). Cada cartão entra no
// seu instante e a seta que chega nele se desenha antes, com um ponto de luz correndo.
// uso: const f = plano(htmlFluxoCartoes({ cartoes: [['scale', 'Ticket', 'peso líquido'], ['file-text', 'Nota', 'entrada'], ['package', 'Estoque', '+ 3.018 kg', 'res']] }), { pos, esc, clima: 'escuro' });
//      fluxoCartoes(f.e, t, a, b, { tempos: [t1, t2, t3] });   ·   pulsa: pulso(parte(f.e, 2), t, a)
// o: cw (largura do cartão, 190), vao (espaço da seta, 74), vertical. O 4º item do cartão: 'res' (resultado, verde) | 'a' (selo âmbar) | 'n' (neutro).
import { selo, vis, pr, eo, eio, estilo, PI } from '../motor.js';
import { base, pt, entra, quando } from './base.js';
export function htmlFluxoCartoes(o = {}) {
  base(); estilo('d-fx', `
.d-fx{position:relative;display:flex;align-items:center}.d-fx.v{flex-direction:column}
.d-fx .cartao{position:relative;padding:15px 16px;flex:none}.d-fx .cab{display:flex;align-items:center;gap:10px}.d-fx .d-t{font-size:17px}.d-fx .d-s{font-size:13px}
.d-fx svg{flex:none;overflow:visible}`);
  const C = o.cartoes ?? [], cw = o.cw ?? 190, vao = o.vao ?? 74, v = !!o.vertical;
  const seta = v ? `<svg width="40" height="${vao}" viewBox="0 0 40 ${vao}" fill="none" stroke-linecap="round" stroke-linejoin="round"><path class="sb" d="M20 8V${vao - 10}" stroke="var(--tr)" stroke-width="2.4"/><path class="st" d="M20 8V${vao - 10}" stroke="var(--ac)" stroke-width="3" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/><path class="sp" d="M12 ${vao - 18}L20 ${vao - 9}L28 ${vao - 18}" stroke="var(--ac)" stroke-width="3" opacity="0"/><circle class="sl" r="5" cx="20" cy="8" fill="#fff" opacity="0"/></svg>`
    : `<svg width="${vao}" height="40" viewBox="0 0 ${vao} 40" fill="none" stroke-linecap="round" stroke-linejoin="round"><path class="sb" d="M8 20H${vao - 10}" stroke="var(--tr)" stroke-width="2.4"/><path class="st" d="M8 20H${vao - 10}" stroke="var(--ac)" stroke-width="3" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/><path class="sp" d="M${vao - 18} 12L${vao - 9} 20L${vao - 18} 28" stroke="var(--ac)" stroke-width="3" opacity="0"/><circle class="sl" r="5" cx="8" cy="20" fill="#fff" opacity="0"/></svg>`;
  return `<div class="d-fx ${v ? 'v' : ''}" data-vao="${vao}">${C.map(([i, r, s, c], k) => `${k ? seta : ''}<div class="cartao ${c === 'res' ? 'res' : ''}" style="width:${cw}px"><div class="cab">${selo(i, c === 'res' ? '' : c ?? 'n', 40)}<div><div class="d-t">${r}</div><div class="d-s">${s ?? ''}</div></div></div></div>`).join('')}</div>`;
}
export const parte = (e, i) => pt(e, '.cartao')[i];
export function fluxoCartoes(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 0, sc: 1 }); const C = pt(e, '.cartao'), S = pt(e, ':scope > svg'), vao = +e.dataset.vao, v = e.classList.contains('v'), T = i => quando(o, a, i, .55, .1);
  C.forEach((c, i) => entra(c, t, T(i), { dy: 18, sc: .95, d: .5 }));
  S.forEach((s, i) => { const t0 = T(i + 1) - .42, p = eio(pr(t, t0, .4)), q = pr(t, t0, .45), l = s.querySelector('.sl'), x = 8 + (vao - 18) * eio(q);
    s.style.opacity = eo(pr(t, T(i) + .1, .3)).toFixed(3); s.querySelector('.st').setAttribute('stroke-dashoffset', (1 - p).toFixed(4)); s.querySelector('.sp').setAttribute('opacity', eo(pr(t, t0 + .3, .15)).toFixed(3));
    l.setAttribute(v ? 'cy' : 'cx', x.toFixed(1)); l.setAttribute('opacity', (q > 0 && q < 1 ? Math.sin(PI * q) ** .5 : 0).toFixed(3)); });
}
