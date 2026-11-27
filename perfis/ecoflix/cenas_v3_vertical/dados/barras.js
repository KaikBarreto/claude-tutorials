// Gráfico de barras simples (compras por material, vendas por mês, margem por cliente): título, barras que crescem do chão
// com o valor em cima, uma em destaque (verde cheio) e as outras em tom neutro.
// uso: const g = plano(htmlBarras({ titulo: 'Compras por material', sub: 'toneladas no mês', dados: [['Latinha', 42], ['PET', 28], ['Cobre', 9]], destaque: 0 }), { pos, esc, clima: 'escuro' });
//      barras(g.e, t, a, b, { tempos });   ·   o: w (420), h (altura das barras, 170), fmt (v => texto), max, selo (ícone)
import { selo, vis, pr, eo, eo5, passa, lerp, estilo } from '../motor.js';
import { base, pt, entra, quando } from './base.js';
export function htmlBarras(o = {}) {
  base(); estilo('d-bar', `
.d-bar{padding:20px 22px 16px}.d-bar .top{display:flex;align-items:center;gap:12px}
.d-bar .ar{position:relative;display:flex;align-items:flex-end;gap:14px;margin-top:34px;border-bottom:1.5px solid var(--tr);background:repeating-linear-gradient(0deg,transparent 0 41.5px,var(--ln) 41.5px 42.5px)}
.d-bar .b{position:relative;flex:1;min-width:0;border-radius:9px 9px 0 0;background:linear-gradient(180deg,var(--tr),var(--fx));transform-origin:50% 100%}
.d-bar .b.dq{background:linear-gradient(180deg,#63D99B,#2FB271);box-shadow:0 0 26px rgba(80,208,136,.35)}
.d-bar .b .d-n{position:absolute;left:50%;top:-23px;translate:-50% 0;font-size:14.5px;color:var(--tx2)}.d-bar .b.dq .d-n{color:var(--ac)}
.d-bar .rs{display:flex;gap:14px;margin-top:8px}.d-bar .rs span{flex:1;min-width:0;text-align:center;font-weight:700;font-size:12.5px;color:var(--tx2);white-space:nowrap}`);
  const D = o.dados ?? [], mx = o.max ?? Math.max(...D.map(d => d[1])), h = o.h ?? 170, fmt = o.fmt ?? (v => String(Math.round(v)));
  return `<div class="cartao d-bar" style="position:relative;width:${o.w ?? 420}px">
    <div class="top">${o.selo ? selo(o.selo, o.cor ?? '', 44) : ''}<div><div class="d-t">${o.titulo ?? ''}</div><div class="d-s">${o.sub ?? ''}</div></div></div>
    <div class="ar" style="height:${h}px">${D.map(([r, v], i) => `<div class="b ${i === o.destaque ? 'dq' : ''}" style="height:${(h * v / mx).toFixed(1)}px" data-v="${v}"><span class="d-n">${fmt(v)}</span></div>`).join('')}</div>
    <div class="rs">${D.map(([r]) => `<span>${r}</span>`).join('')}</div></div>`;
}
export function barras(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 24, sc: .96 }); const fmt = o.fmt ?? (v => String(Math.round(v))), R = pt(e, '.rs span');
  pt(e, '.b').forEach((x, i) => { const ti = quando(o, a, i, .1, .35), p = pr(t, ti, .7), n = x.firstElementChild, v = +x.dataset.v;
    x.style.transform = `scaleY(${Math.max(.001, passa(p, .7)).toFixed(4)})`; n.style.transform = `scaleY(${(1 / Math.max(.05, passa(p, .7))).toFixed(4)})`; n.style.opacity = eo(pr(t, ti + .2, .3)).toFixed(3);
    const s = fmt(lerp(0, v, eo5(p))); if (n.textContent !== s) n.textContent = s; R[i].style.opacity = eo(pr(t, ti, .3)).toFixed(3); });
}
