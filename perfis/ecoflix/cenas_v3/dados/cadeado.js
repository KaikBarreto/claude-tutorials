// Cadeado e permissão: o cadeado (desenho próprio do kit) que abre, e o cartão de permissões de um papel (linhas com chave
// ligada ou trancada). Para "quem pode ver o quê", "liberado pelo administrador", "acesso bloqueado".
// uso: const c = plano(htmlCadeado({ px: 150 }), { pos, esc, clima: 'escuro' }); cadeado(c.e, t, a, b, { abre: tAbre });   // sem abre: fica fechado
//      const p = plano(htmlPermissao({ icone: 'user', papel: 'Operador de balança', sub: '3 de 5 liberadas', itens: [['Pesar', true], ['Ver preços', false]] }), { ... });
//      permissao(p.e, t, a, b, { tempos, liga: [[1, tLibera]] });   // liga: a linha i passa de trancada a liberada no instante dado
import { selo, vis, pr, eo, eio, golpe, passa, lerp, estilo } from '../motor.js';
import { base, pt, entra, quando } from './base.js';
const CSS = `
.d-cad{position:relative}.d-cad .cp{position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 50% 45%,var(--fx2),transparent 70%)}
.d-cad svg{position:absolute;inset:0;overflow:visible}.d-cad .aro{transform-origin:66.5% 47%}
.d-per{padding:18px 20px 12px}.d-per .top{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.d-per .ln{display:flex;align-items:center;justify-content:space-between;height:46px;border-top:1px solid var(--ln)}.d-per .ln .d-v{font-size:15.5px}
.d-per .ch{position:relative;width:46px;height:26px;border-radius:13px;background:var(--tr);flex:none}.d-per .ch .on{position:absolute;inset:0;border-radius:13px;background:linear-gradient(100deg,#2FB271,#63D99B);box-shadow:0 0 16px rgba(80,208,136,.4);opacity:0}
.d-per .ch .bt{position:absolute;left:3px;top:3px;width:20px;height:20px;border-radius:50%;background:#fff;box-shadow:0 2px 5px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;color:#7B8794}`;
export function htmlCadeado(o = {}) {
  base(); estilo('d-cad', CSS); const px = o.px ?? 150;
  return `<div class="d-cad" style="width:${px}px;height:${px}px"><div class="cp"></div><svg viewBox="0 0 120 120" fill="none">
    <defs><linearGradient id="cdA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#63D99B"/><stop offset="1" stop-color="#2FB271"/></linearGradient><linearGradient id="cdB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7CB68"/><stop offset="1" stop-color="#E59A22"/></linearGradient></defs>
    <g class="tudo"><path class="aro" d="M43 56V40a17 17 0 0 1 34 0v16" stroke="var(--tx2)" stroke-width="9" stroke-linecap="round"/>
    <rect class="cb" x="30" y="53" width="60" height="46" rx="13" fill="url(#cdB)"/><rect class="ca" x="30" y="53" width="60" height="46" rx="13" fill="url(#cdA)" opacity="0"/>
    <rect x="30.5" y="53.5" width="59" height="45" rx="12.5" stroke="rgba(255,255,255,.45)"/><circle cx="60" cy="72" r="6.5" fill="#fff"/><rect x="57" y="74" width="6" height="13" rx="3" fill="#fff"/></g></svg></div>`;
}
export function cadeado(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 0, sc: .7 }); const ab = o.abre ?? 1e9, p = pr(t, ab, .5), q = eio(p);
  pt(e, '.aro')[0].style.transform = `translateY(${(-7 * q).toFixed(2)}px) rotate(${(-38 * passa(p, 1.2) * (p > 0 ? 1 : 0)).toFixed(2)}deg)`; pt(e, '.ca')[0].setAttribute('opacity', eo(pr(t, ab + .12, .3)).toFixed(3));
  pt(e, '.tudo')[0].style.transform = `rotate(${(5 * golpe(pr(t, ab - .02, .5), 2.2, 4)).toFixed(2)}deg)`; pt(e, '.tudo')[0].style.transformOrigin = '50% 60%';
}
export function htmlPermissao(o = {}) {
  base(); estilo('d-cad', CSS);
  return `<div class="cartao d-per" style="position:relative;width:${o.w ?? 340}px"><div class="top">${selo(o.icone ?? '', o.cor ?? '', 44)}<div><div class="d-t">${o.papel ?? ''}</div><div class="d-s">${o.sub ?? ''}</div></div></div>
    ${(o.itens ?? []).map(([r, on]) => `<div class="ln" data-on="${on ? 1 : 0}"><span class="d-v">${r}</span><div class="ch"><i class="on"></i><i class="bt"><svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M4 5.5V4a2 2 0 0 1 4 0v1.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><rect x="2.6" y="5.3" width="6.8" height="5" rx="1.5" fill="currentColor"/></svg></i></div></div>`).join('')}</div>`;
}
export function permissao(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 24, sc: .96 }); const liga = new Map(o.liga ?? []);
  pt(e, '.ln').forEach((x, i) => { const ti = quando(o, a, i, .12, .3); entra(x, t, ti, { dx: -12, dy: 0 }); const on = x.dataset.on === '1', tl = liga.get(i) ?? (on ? ti + .2 : 1e9), k = eio(pr(t, tl, .32));
    x.querySelector('.on').style.opacity = k.toFixed(3); const bt = x.querySelector('.bt'); bt.style.transform = `translateX(${(20 * k).toFixed(2)}px)`; bt.firstElementChild.style.opacity = (1 - k).toFixed(3); x.firstElementChild.style.opacity = lerp(.55, 1, k).toFixed(3); });
}
