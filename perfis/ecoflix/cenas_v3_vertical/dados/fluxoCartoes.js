// Fluxo com setas entre cartões (o caminho do dado no sistema: Ticket → Nota → Estoque → Financeiro). Cada cartão entra no
// seu instante e a seta que chega nele se desenha antes, com um ponto de luz correndo.
// uso: const f = plano(htmlFluxoCartoes({ cartoes: [['scale', 'Ticket', 'peso líquido'], ['file-text', 'Nota', 'entrada'], ['package', 'Estoque', '+ 3.018 kg', 'res']] }), { pos, esc, clima: 'escuro' });
//      fluxoCartoes(f.e, t, a, b, { tempos: [t1, t2, t3] });   ·   pulsa: pulso(parte(f.e, 2), t, a)
// o: cw (largura MÍNIMA do cartão, 190), vao (espaço da seta, 74; mínimo 44), respiro (entre a seta e os cartões, 12), vertical.
// O 4º item do cartão: 'res' (resultado, verde) | 'a' (selo âmbar) | 'n' (neutro).
// Acabamento: os cartões têm todos a MESMA largura, a do texto mais comprido (nunca menor que cw): texto não estoura. A seta
// fica no eixo dos cartões, com o mesmo respiro nas duas pontas. Para alinhar duas fileiras em colunas, dê às duas um cw
// que caiba o texto mais comprido das duas (o auditar acusa se não couber). A largura real é p.w; cartão i: parte(e, i).
import { selo, vis, pr, eo, eio, estilo, PI } from '../motor.js';
import { base, pt, entra, quando } from './base.js';
export function htmlFluxoCartoes(o = {}) {
  base(); estilo('d-fx', `
.d-fx{position:relative;display:grid;align-items:center;width:max-content}.d-fx.v{justify-items:stretch}
.d-fx .cartao{position:relative;padding:15px 16px;white-space:nowrap}.d-fx .cab{display:flex;align-items:center;gap:10px}.d-fx .d-t{font-size:17px}.d-fx .d-s{font-size:13px}
.d-fx svg{overflow:visible;display:block;justify-self:center}`);
  const C = o.cartoes ?? [], cw = o.cw ?? 190, vao = Math.max(44, o.vao ?? 74), r = Math.min(o.respiro ?? 12, vao / 2 - 10), v = !!o.vertical, p0 = r + 1.5, p1 = vao - r - 1.5;   // a ponta redonda do traço (1,5) conta no respiro
  const d = (a, b) => v ? `M20 ${a}V${b}` : `M${a} 20H${b}`, ponta = v ? `M12 ${p1 - 9}L20 ${p1}L28 ${p1 - 9}` : `M${p1 - 9} 12L${p1} 20L${p1 - 9} 28`;
  const seta = `<svg class="seta" width="${v ? 40 : vao}" height="${v ? vao : 40}" viewBox="0 0 ${v ? 40 : vao} ${v ? vao : 40}" fill="none" stroke-linecap="round" stroke-linejoin="round"><path class="sb" d="${d(p0, p1 - 1.5)}" stroke="var(--tr)" stroke-width="2.4"/><path class="st" d="${d(p0, p1 - 1.5)}" stroke="var(--ac)" stroke-width="3" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/><path class="sp" d="${ponta}" stroke="var(--ac)" stroke-width="3" opacity="0"/><circle class="sl" r="5" ${v ? `cx="20" cy="${p0}"` : `cx="${p0}" cy="20"`} fill="#fff" opacity="0"/></svg>`;
  const trilhas = C.map((_, k) => `${k ? vao + 'px ' : ''}${v ? 'auto' : `minmax(${cw}px,1fr)`}`).join('');
  return `<div class="d-fx ${v ? 'v' : ''}" data-vao="${vao}" data-r="${p0}" style="${v ? `grid-template-rows:${trilhas};min-width:${cw}px` : `grid-template-columns:${trilhas}`}">${C.map(([i, r, s, c], k) => `${k ? seta : ''}<div class="cartao ${c === 'res' ? 'res' : ''}"><div class="cab">${selo(i, c === 'res' ? '' : c ?? 'n', 40)}<div><div class="d-t">${r}</div><div class="d-s">${s ?? ''}</div></div></div></div>`).join('')}</div>`;
}
export const parte = (e, i) => pt(e, '.cartao')[i], seta = (e, i) => pt(e, ':scope > svg')[i];   // seta(e, i) = a que chega no cartão i + 1
export function fluxoCartoes(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 0, sc: 1 }); const C = pt(e, '.cartao'), S = pt(e, ':scope > svg'), vao = +e.dataset.vao, v = e.classList.contains('v'), T = i => quando(o, a, i, .55, .1);
  C.forEach((c, i) => entra(c, t, T(i), { dy: 18, sc: .95, d: .5 }));
  S.forEach((s, i) => { const t0 = T(i + 1) - .42, p = eio(pr(t, t0, .4)), q = pr(t, t0, .45), l = s.querySelector('.sl'), r0 = +(e.dataset.r ?? 8), x = r0 + (vao - 2 * r0) * eio(q);
    s.style.opacity = eo(pr(t, Math.max(T(i) + .1, t0 - .18), .3)).toFixed(3);   /* a seta só aparece quando vai se desenhar: não fica apontando para o vazio */ s.querySelector('.st').setAttribute('stroke-dashoffset', (1 - p).toFixed(4)); s.querySelector('.sp').setAttribute('opacity', eo(pr(t, t0 + .3, .15)).toFixed(3));
    l.setAttribute(v ? 'cy' : 'cx', x.toFixed(1)); l.setAttribute('opacity', (q > 0 && q < 1 ? Math.sin(PI * q) ** .5 : 0).toFixed(3)); });
}
