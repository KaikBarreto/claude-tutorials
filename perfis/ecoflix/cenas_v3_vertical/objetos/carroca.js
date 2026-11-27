// Carroça de mão do catador: caixa âmbar, duas rodas de raio, varais de madeira. Frente (os varais) em +x.
// uso: const c = carroca(CENA, [x, 0, z], { carga: 'papelao' }); puxa(c, x) anda e gira as rodas
// userData: rodas, R, fundo (y do fundo da caixa), dentro, topo, lotes.
import { PI, mat, caixa, cil, toro, malha, grupo, mancha } from '../motor.js';
import { pecas, pontosMonte } from './monte.js';
export function carroca(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), amb = mat(o.cor ?? '#F2B63D', { alt: 1.2, emi: .28, bri: .22 }), ambE = mat('#D99A2B', { alt: 1.2, emi: .28 }), pau = mat('#A9764A', { alt: 1, emi: .14 }), esc = mat('#2B323B', { bri: .12 }), R = .42, rodas = [];
  mancha(3.4, 2.3, [.3, 0, .1], { pai: g, op: .75 });
  for (const z of [-.72, .72]) { const r = grupo(g, [0, R, z]); rodas.push(r);
    malha(toro(R - .07, .07, 34), esc, [0, 0, 0], r); malha(cil(.09, .12, 16), mat('#50D088', { emi: .55 }), [0, 0, 0], r, [PI / 2, 0, 0]);
    for (let k = 0; k < 4; k++) malha(caixa(2 * R - .16, .035, .035, .012), mat('#C9D1DA', { emi: .14 }), [0, 0, 0], r, [0, 0, k * PI / 4]); }
  malha(cil(.035, 1.44, 10), esc, [0, R, 0], g, [PI / 2, 0, 0]); for (const z of [-.44, .44]) malha(caixa(.12, .22, .06, .02), esc, [0, R + .1, z], g);
  malha(caixa(1.9, .07, 1.2, .025), ambE, [0, .62, 0], g);
  for (const x of [-.92, .92]) malha(caixa(.07, .5, 1.2, .025), amb, [x, .87, 0], g); for (const z of [-.57, .57]) malha(caixa(1.9, .5, .07, .025), amb, [0, .87, z], g);
  for (const z of [-.42, .42]) malha(cil(.034, 1.4, 10), pau, [1.6, .76, z], g, [0, 0, PI / 2 - .03]); malha(cil(.036, 1.0, 10), pau, [2.28, .78, 0], g, [PI / 2, 0, 0]);
  g.userData = { rodas, R, fundo: .66, dentro: [0, .66, 0], topo: [0, 1.9, 0] };
  if (o.carga) g.userData.lotes = pecas(g, o.carga, pontosMonte(o.n ?? 30, .78, .44, .62, .74), { s: o.sp ?? .78 });
  return g;
}
export function puxa(c, x) { c.position.x = x; for (const r of c.userData.rodas) r.rotation.z = -x / c.userData.R; }
