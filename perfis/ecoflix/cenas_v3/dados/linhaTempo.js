// Linha do tempo: etapas em sequência num trilho (o caminho de um ticket, de uma nota, de um pagamento). O trilho acende
// até a etapa atual; cada etapa tem o selo com ícone, o nome e a legenda (data, hora, quem fez).
// uso: const l = plano(htmlLinhaTempo({ etapas: [['scale', 'Pesagem', '08:12'], ['file-text', 'Nota', '08:20'], ['banknote', 'Pagamento', '08:31']] }), { pos, esc, clima: 'escuro' });
//      linhaTempo(l.e, t, a, b, { tempos: [t1, t2, t3] });   // cada etapa acende no seu instante (sem tempos: uma a cada .5 s)
// o: w (largura total, 640), vertical (true: de cima para baixo, com o texto à direita), pendente (índice a partir do qual fica apagada).
import { selo, vis, pr, eo, eio, passa, lerp, estilo } from '../motor.js';
import { base, pt, entra, quando } from './base.js';
// Acabamento: cada etapa tem a largura do texto mais comprido (nunca menos que a do layout pedido): os nomes não se
// encostam (16 px no mínimo entre eles) e o trilho liga os selos de centro a centro. Com textos curtos, sai como antes.
export function htmlLinhaTempo(o = {}) {
  base(); estilo('d-lt', `
.d-lt{position:relative;display:grid;width:max-content}.d-lt .tr,.d-lt .tf{position:absolute;border-radius:3px}.d-lt .tr{background:var(--tr)}.d-lt .tf{background:linear-gradient(90deg,#2FB271,#6CF0A8);box-shadow:0 0 14px rgba(80,208,136,.5);transform-origin:0 0}
.d-lt.v .tf{background:linear-gradient(180deg,#2FB271,#6CF0A8)}
.d-lt .et{position:relative;display:flex;flex-direction:column;align-items:center;gap:9px;text-align:center}.d-lt.v .et{flex-direction:row;text-align:left;gap:14px;align-self:start;height:46px}
.d-lt .et .ap{position:absolute;left:50%;top:0;width:46px;height:46px;margin-left:-23px;border-radius:14px;background:var(--fx);border:1.5px dashed var(--tr)}.d-lt.v .et .ap{left:0;margin-left:0}
.d-lt .et .selo{position:relative}.d-lt .et .d-t{font-size:16.5px}.d-lt .et .d-s{font-size:13px}`);
  const E = o.etapas ?? [], n = E.length, v = !!o.vertical, W = o.w ?? (v ? 300 : 640), P = v ? (o.passo ?? 84) : (W - 150) / Math.max(1, n - 1), H = v ? (n - 1) * P + 46 : 104;
  const col = Math.max(60, Math.min(150, P - 16)), vao = n > 1 ? P - col : 0, pad = (150 - col) / 2;   // horizontal: n colunas iguais; com texto curto, os centros ficam em 75 + k * P (como antes)
  const lado = `calc(${pad}px + (100% - ${2 * pad + (n - 1) * vao}px) / ${2 * n})`, trilho = v ? `left:20px;top:23px;width:6px;height:${(n - 1) * P}px` : `left:${lado};right:${lado};top:20px;height:6px`;
  return `<div class="d-lt ${v ? 'v' : ''}" style="${v ? `min-width:${W}px;grid-template-rows:${n > 1 ? `repeat(${n - 1},${P}px) ` : ''}46px` : `min-height:${H}px;padding:0 ${pad}px;grid-template-columns:repeat(${n},minmax(${col}px,1fr));column-gap:${vao}px`}" data-p="${P}" data-n="${n}">
    <div class="tr" style="${trilho}"></div><div class="tf" style="${trilho}"></div>
    ${E.map(([i, r, s, c]) => `<div class="et"><i class="ap"></i>${selo(i, c ?? '', 46)}<div class="tx"><div class="d-t">${r}</div><div class="d-s">${s ?? ''}</div></div></div>`).join('')}</div>`;
}
export function linhaTempo(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 18 }); const n = +e.dataset.n, v = e.classList.contains('v'), E = pt(e, '.et'), T = i => quando(o, a, i, .5, .35); let f = 0;
  E.forEach((x, i) => { const ti = T(i), s = x.querySelector('.selo'), tx = x.querySelector('.tx'), on = i < (o.pendente ?? 99);
    x.style.opacity = eo(pr(t, a + .1 + i * .06, .3)).toFixed(3); const p = on ? pr(t, ti, .5) : 0; s.style.transform = `scale(${(p <= 0 ? 0 : passa(p, 1.7)).toFixed(4)})`; s.style.opacity = eo(pr(t, ti, .15)).toFixed(3) * (on ? 1 : 0);
    tx.style.opacity = lerp(.45, 1, on ? eo(pr(t, ti, .3)) : 0).toFixed(3);
    if (on && i > 0) f = Math.max(f, i - 1 + eio(pr(t, T(i) - .45, .45))); });
  pt(e, '.tf')[0].style.transform = v ? `scaleY(${(f / Math.max(1, n - 1)).toFixed(4)})` : `scaleX(${(f / Math.max(1, n - 1)).toFixed(4)})`;
}
