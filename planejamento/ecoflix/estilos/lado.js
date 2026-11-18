// Vista lateral da cena (caminhão carregado sobre a balança rodoviária, poste do visor) como lista de formas com um
// grupo cada. Os estilos 2D (flat, traço, papel, blueprint, vidro, gradiente) desenham AS MESMAS formas e só trocam o
// tratamento: est(forma) devolve os atributos SVG do grupo (texto), uma lista deles (várias passadas) ou null (não desenha).
import { sorteio, CORES_LATA } from './comum.js';
export const G = 682, X0 = 106, CH = G + 18;   // G: tampo da balança (onde as rodas pisam); X0: traseira do caminhão
export const BX = X0 + 356, BY = G - 73;   // canto de baixo/trás da cabine
export const POSTE = { x: 686, topo: G - 318 }, VISOR = { x: 700, y: G - 318 }, SELO = { x: X0 + 170, y: G - 222 };

export function poliR(pts, r) {   // polígono com cantos arredondados (r: número ou um por canto)
  const n = pts.length; let d = '';
  for (let i = 0; i < n; i++) { const p0 = pts[(i + n - 1) % n], p1 = pts[i], p2 = pts[(i + 1) % n];
    const v1 = [p0[0] - p1[0], p0[1] - p1[1]], v2 = [p2[0] - p1[0], p2[1] - p1[1]], l1 = Math.hypot(...v1), l2 = Math.hypot(...v2);
    const rr = Math.min(Array.isArray(r) ? r[i] : r, l1 / 2, l2 / 2);
    const a = [p1[0] + v1[0] / l1 * rr, p1[1] + v1[1] / l1 * rr], b = [p1[0] + v2[0] / l2 * rr, p1[1] + v2[1] / l2 * rr];
    d += `${i ? 'L' : 'M'}${a[0].toFixed(1)} ${a[1].toFixed(1)}Q${p1[0]} ${p1[1]} ${b[0].toFixed(1)} ${b[1].toFixed(1)}`; }
  return d + 'Z';
}
const R = (g, x, y, w, h, r = 0, x2) => ({ g, t: 'rect', x, y, w, h, r, ...x2 });
const C = (g, cx, cy, r, x2) => ({ g, t: 'circle', cx, cy, r, ...x2 });
const P = (g, d, x2) => ({ g, t: 'path', d, ...x2 });

// o.carga: { n (latas), esc (tamanho), ferro (peças) }; o.simples: sem miudezas (frisos, maçaneta, porta)
export function partes(o = {}) {
  const rnd = sorteio(o.semente ?? 7), ri = (a, b) => a + (b - a) * rnd(), L = [];
  const cg = { n: 120, esc: 1, ferro: 9, ...(o.carga || {}) };
  // balança: rampas, tampo, poste do visor
  L.push(R('poste', POSTE.x - 4, POSTE.topo, 8, CH - POSTE.topo, 3), R('posteBase', POSTE.x - 17, CH - 9, 34, 9, 3));
  L.push(P('rampa', `M44 ${CH}L98 ${G}L98 ${CH}Z`), P('rampa', `M684 ${CH}L630 ${G}L630 ${CH}Z`));
  L.push(R('deck', 94, G, 540, 18, 3), R('deckTopo', 94, G, 540, 5, 2.5));
  if (!o.simples) for (const x of [150, 364, 578]) L.push(R('celula', x - 14, G + 8, 28, 10, 2));
  // caminhão: chassi, tanque, para-choque
  L.push(R('chassi', X0 + 16, G - 67, 462, 21, 5), R('subcab', X0 + 362, G - 76, 126, 36, 5), R('tanque', X0 + 232, G - 52, 82, 27, 13),
    R('parachoque', X0 + 480, G - 54, 24, 26, 6), R('estrado', X0 + 12, G - 81, 318, 12, 3));
  // caçamba: tábua da frente, carga, lateral por cima
  L.push(R('bauFrente', X0 + 326, G - 180, 12, 106, 3));
  const xa = X0 + 20, xb = X0 + 320, xm = (xa + xb) / 2, hf = (xb - xa) / 2, yT = G - 152;
  const topo = x => yT - 6 - 50 * cg.esc ** .3 * (1 - ((x - xm) / hf) ** 4);
  const ferro = k => { const x = ri(xa + 30, xb - 30), y = topo(x) + ri(0, 22), a = ri(-34, 34);
    if (k % 3 === 0) { const w = ri(64, 96) * cg.esc ** .5, h = 9 * cg.esc ** .5; L.push(R('viga', x - w / 2, y - h / 2, w, h, 2, { rot: [a, x, y] })); }
    else if (k % 3 === 1) { const r = ri(9, 12) * cg.esc ** .5; L.push(C('tubo', x, y, r), C('tuboFuro', x, y, r * .55)); }
    else { const s = ri(17, 24) * cg.esc ** .5; L.push(P('chapa', poliR([[x - s, y + s * .6], [x - s * .3, y - s * .8], [x + s, y - s * .2], [x + s * .5, y + s * .7]], 2), { rot: [a, x, y] })); } };
  for (let k = 0; k < Math.ceil(cg.ferro / 2); k++) ferro(k);
  const latas = [];
  for (let i = 0; i < cg.n; i++) { const x = ri(xa, xb), t = topo(x), y = t + (yT + 10 - t) * rnd() ** 1.15 + 7 * cg.esc; latas.push([x, y, ri(0, 180), Math.floor(rnd() * CORES_LATA.length)]); }
  latas.sort((a, b) => a[1] - b[1]);
  const w = 14 * cg.esc, h = 22 * cg.esc;
  latas.forEach(([x, y, a, ci], i) => { L.push(R('lata', x - w / 2, y - h / 2, w, h, 3 * cg.esc, { rot: [a, x, y], ci }), R('lataFaixa', x - w / 2, y - h * .27, w, h * .54, 0, { rot: [a, x, y], ci }));
    if (i === Math.floor(cg.n * .45)) for (let k = Math.ceil(cg.ferro / 2); k < cg.ferro; k++) ferro(k); });
  L.push(R('bau', X0 + 3, G - 152, 332, 80, 5), R('bauBorda', X0, G - 157, 338, 10, 4));
  if (!o.simples) for (let i = 1; i < 5; i++) L.push(R('bauFriso', X0 + 3 + i * 332 / 5 - 3.5, G - 144, 7, 68, 2));
  // cabine (perfil com o para-brisa inclinado), janela, porta
  const cab = [[0, 0], [139, 0], [139, -70], [117, -119], [104, -128], [0, -128]].map(([x, y]) => [BX + x, BY + y]);
  L.push(P('cab', poliR(cab, [6, 8, 6, 8, 12, 12])));
  L.push(P('cabFaixa', poliR([[BX, BY], [BX + 139, BY], [BX + 139, BY - 30], [BX, BY - 30]], [6, 8, 0, 0])));
  L.push(P('janela', poliR([[58, -114], [103, -114], [122, -74], [58, -74]].map(([x, y]) => [BX + x, BY + y]), 6)));
  if (!o.simples) L.push(P('porta', `M${BX + 48} ${BY - 116}V${BY - 10}`, { linha: 1 }), R('macaneta', BX + 58, BY - 60, 16, 5, 2.5));
  L.push(R('farol', BX + 129, BY - 40, 10, 20, 3), R('espelho', BX + 126, BY - 104, 8, 30, 4));
  // rodas
  for (const x of [X0 + 75, X0 + 150, X0 + 424]) L.push(C('pneu', x, G - 34, 34), C('aro', x, G - 34, 18), C('cubo', x, G - 34, 6.5));
  return L;
}
export function forma(p, at) {
  const s = p.t === 'rect' ? `<rect x="${p.x.toFixed(1)}" y="${p.y.toFixed(1)}" width="${p.w.toFixed(1)}" height="${p.h.toFixed(1)}" rx="${p.r}" ${at}/>`
    : p.t === 'circle' ? `<circle cx="${p.cx.toFixed(1)}" cy="${p.cy.toFixed(1)}" r="${p.r.toFixed(1)}" ${at}/>` : `<path d="${p.d}" ${at}/>`;
  return p.rot ? `<g transform="rotate(${p.rot[0].toFixed(1)} ${p.rot[1].toFixed(1)} ${p.rot[2].toFixed(1)})">${s}</g>` : s;
}
export function svg(L, est, o = {}) {
  let s = '';
  for (const p of L) { const a = est(p); if (a == null) continue; for (const at of [].concat(a)) s += forma(p, at); }
  return `<svg id="sv" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 728 880" width="728" height="880"><defs>${o.defs || ''}</defs>${o.antes || ''}${s}${o.depois || ''}</svg>`;
}
