// Balão de conversa (o assistente Cato responde, o usuário pergunta): bolha com a ponta, o selo de quem fala (ícone genérico,
// SEM logo) e o nome. O texto entra palavra por palavra depois dos três pontinhos de "pensando".
// uso: const p = plano(htmlBalao({ lado: 'e', icone: 'sparkles', nome: 'Cato', texto: 'Hoje entraram 3.018 kg de latinha.' }), { pos, esc, clima: 'escuro' });
//      balao(p.e, t, a, b, { pensa: .6, d: 1.2 });   // pensa = tempo dos pontinhos; d = tempo para o texto todo aparecer
// o: lado ('e' = assistente, bolha de vidro à esquerda | 'd' = usuário, bolha verde à direita), w (largura máx. do texto, 330), nome, icone.
import { selo, vis, pr, eo, cl, estilo, PI } from '../motor.js';
import { base, pt } from './base.js';
export function htmlBalao(o = {}) {
  base(); estilo('d-bal', `
.d-bal{position:relative;display:flex;align-items:flex-end;gap:12px}.d-bal.d{flex-direction:row-reverse}
.d-bal .bo{position:relative;padding:14px 18px 15px;border-radius:22px 22px 22px 7px;background:var(--cart);border:var(--cb);box-shadow:var(--cs);transform-origin:0 100%}
.d-bal.d .bo{border-radius:22px 22px 7px 22px;background:linear-gradient(150deg,#63D99B,#2FB271);border:1px solid rgba(255,255,255,.35);box-shadow:0 18px 36px -10px rgba(47,178,113,.55),inset 0 1px 0 rgba(255,255,255,.4);transform-origin:100% 100%}
.d-bal .nm{font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ac);margin-bottom:5px}.d-bal.d .nm{color:rgba(255,255,255,.85)}
.d-bal .tx{font-weight:600;font-size:17px;line-height:1.38;color:var(--tx)}.d-bal.d .tx{color:#fff}.d-bal .tx b{font-weight:800;color:var(--ac)}.d-bal.d .tx b{color:#fff}
.d-bal .pp{position:absolute;left:18px;bottom:17px;display:flex;gap:6px}.d-bal .pp i{width:9px;height:9px;border-radius:50%;background:var(--mut)}.d-bal.d .pp i{background:rgba(255,255,255,.8)}
.d-bal .selo{border-radius:50%!important}`);
  const pal = String(o.texto ?? '').split(/\s+/).map(w => `<span class="pw">${w}</span>`).join(' ');
  return `<div class="d-bal ${o.lado === 'd' ? 'd' : ''}">${selo(o.icone ?? '', o.lado === 'd' ? 'n' : '', 44)}<div class="bo" style="max-width:${(o.w ?? 330) + 38}px">${o.nome ? `<div class="nm">${o.nome}</div>` : ''}<div class="tx">${pal}</div><div class="pp"><i></i><i></i><i></i></div></div></div>`;
}
export function balao(e, t, a, b = 1e9, o = {}) {
  const pensa = o.pensa ?? .55, d = o.d ?? 1.1, t1 = a + .25 + pensa, P = pt(e, '.pw'), bo = pt(e, '.bo')[0], sl = pt(e, '.selo')[0];
  vis(e, t, a, b, { dy: 0, sc: 1 }); const p = pr(t, a + .08, .5); bo.style.transform = `scale(${(p <= 0 ? .6 : .6 + .4 * (1 - Math.pow(1 - p, 3)) + .05 * Math.sin(PI * p) * (1 - p)).toFixed(4)})`; bo.style.opacity = eo(pr(t, a + .08, .2)).toFixed(3);
  sl.style.transform = `scale(${eo(pr(t, a, .35)).toFixed(4)})`;
  P.forEach((w, i) => { w.style.opacity = eo(pr(t, t1 + d * i / P.length, .22)).toFixed(3); });
  const k = cl(1 - (t - t1 + .12) / .12) * eo(pr(t, a + .25, .2)); pt(e, '.pp i').forEach((x, i) => { x.style.opacity = (k * (.45 + .55 * Math.max(0, Math.sin((t - a) * 9 - i * .9)))).toFixed(3); x.style.transform = `translateY(${(-3 * Math.max(0, Math.sin((t - a) * 9 - i * .9))).toFixed(2)}px)`; });
}
