// Kit v3 · os fundos em profundidade dos dois climas (os mesmos da cena aprovada da T08), prontos e já no acabamento certo:
// tudo o que é enfeite fica ATRÁS do conteúdo. Manchas, brilhos, pontos e poeira são planos `tras` (macios: podem aparecer
// através do vidro); os anéis são traço, então vão como `tras + deco`: o motor os recorta atrás de todo cartão de vidro.
// uso (claro):  ceuClaro();                                     // disco claro atrás do assunto + manchas de cor
// uso (escuro): const E = mundoEscuro(EIXO, ZD, EE);            // E(html, x, y, z, o) = plano escuro no lugar EIXO (metros), em z = ZD + z
//               E.fundo(cx, cy);                                // pontos, brilhos, anéis e poeira, centrados em (cx, cy) do desenho
//               for (const p of E.lista) p.op = dentro;         // E.lista = todos os planos escuros (para a troca de clima)
// FOCAL = distância focal em px no fov 26: escala na tela de um plano = esc * FOCAL / distância.
import { PI, ri, plano, ALT } from './motor.js';
export const FOCAL = ALT / 2 / Math.tan(13 * PI / 180);
export const BOLA = (cor, w) => `<div style="width:${w}px;height:${w}px;border-radius:50%;background:radial-gradient(circle,${cor} 0%,${cor.replace(/[\d.]+\)$/, '0)')} 68%)"></div>`;
export function ceuClaro(o = {}) {   // o.em = lugar (para outra frente), o.halo = posição do disco claro
  const P = (h, pos, esc) => plano(h, { em: o.em ?? null, pos, esc, tras: true });
  return [P('<div style="width:1500px;height:1500px;border-radius:50%;background:radial-gradient(circle at 42% 36%,#fff 0%,#fff 38%,rgba(232,247,239,.9) 62%,rgba(221,243,231,0) 71%)"></div>', o.halo ?? [1.2, 3.4, -14], .0135),
    P(BOLA('rgba(189,239,212,.95)', 1300), [-34, 10, -70], .05), P(BOLA('rgba(207,228,255,.95)', 1200), [34, 20, -80], .05), P(BOLA('rgba(252,231,184,.8)', 1100), [30, -8, -60], .05), P(BOLA('rgba(211,245,227,.9)', 900), [-22, -9, -50], .05)];
}
export function mundoEscuro(EIXO, ZD, EE = .0112) {
  const L = [], E = (html, x, y, z = 0, o = {}) => { const p = plano(html, { em: EIXO, pos: [x, y, ZD + z], esc: EE, clima: 'escuro', ...o }); L.push(p); return p; };
  E.lista = L;
  E.fundo = (cx, cy, o = {}) => {
    E('<div style="width:3200px;height:2000px;background-image:radial-gradient(rgba(255,255,255,.13) 1.5px,transparent 2.2px);background-size:40px 40px;-webkit-mask-image:radial-gradient(1500px 900px at 50% 50%,#000 20%,transparent 78%)"></div>', cx, cy, -16, { esc: .03, tras: true });
    E(BOLA('rgba(80,208,136,.20)', 620), cx, cy - 1.5, -5, { esc: .04, tras: true }); E(BOLA('rgba(90,150,255,.14)', 560), cx - 13, cy + 8, -12, { esc: .04, tras: true }); E(BOLA('rgba(80,208,136,.13)', 520), cx + 12, cy + 5, -10, { esc: .04, tras: true });
    if (o.aneis !== false) E(`<svg width="1400" height="1400" viewBox="-700 -700 1400 1400" fill="none" stroke="rgba(108,240,168,.17)" stroke-width="1.6"><circle r="330"/><circle r="470" stroke-dasharray="4 12"/><circle r="640" opacity=".55"/></svg>`, cx, cy - 1.5, -3, { esc: .017, tras: true, deco: true });
    for (let i = 0; i < 12; i++) { const w = Math.round(ri(26, 84));   // poeira de luz ATRÁS dos cartões, em várias distâncias (paralaxe: dá a medida do movimento)
      E(`<div style="width:${w}px;height:${w}px;border-radius:50%;background:radial-gradient(circle,rgba(140,245,190,${ri(.08, .2).toFixed(2)}) 0%,rgba(140,245,190,0) 70%)"></div>`, cx + ri(-11, 11), cy + ri(-6, 5), -ri(.8, 7), { esc: .014, tras: true }); }
  };
  return E;
}
