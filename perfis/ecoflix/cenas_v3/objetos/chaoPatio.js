// Chão do pátio: placa de concreto clara (topo em y 0) com as juntas e, se pedir, faixas âmbar tracejadas.
// uso: chaoPatio(CENA, [x, 0, z], { c: 22, l: 12, passo: 3, faixa: [-2, 2] });   faixa = lista de z das faixas
// Sem piso() por baixo ele já dá o chão; com piso(), fica como uma laje no meio dos pontos.
import { mat, caixa, malha, grupo, lote, poeInst } from '../motor.js';
export function chaoPatio(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 22, l = o.l ?? 12, e = o.passo ?? 3, g = grupo(pai, pos), jx = [], jz = [];
  malha(caixa(c, .14, l, .06), mat('#EDF1F3', { alt: .3, emi: .08, bri: .05 }), [0, -.07, 0], g).renderOrder = -3;
  for (let x = -c / 2 + e; x < c / 2 - .2; x += e) jx.push(x); for (let z = -l / 2 + e; z < l / 2 - .2; z += e) jz.push(z);
  const mj = mat('#D5DCE2', { emi: .14 }), a = lote(caixa(.05, .006, l - .16, .002), mj, jx.length, g), b = lote(caixa(c - .16, .006, .05, .002), mj, jz.length, g);
  jx.forEach((x, i) => poeInst(a, i, [x, .002, 0])); jz.forEach((z, i) => poeInst(b, i, [0, .002, z]));
  const F = []; for (const z of o.faixa ?? []) for (let x = -c / 2 + .8; x < c / 2 - 1.4; x += 2.2) F.push([x + .6, .004, z]);
  if (F.length) { const f = lote(caixa(1.2, .006, .13, .002), mat('#F2B63D', { emi: .5 }), F.length, g); F.forEach((p, i) => poeInst(f, i, p)); }
  g.userData = { c, l }; return g;
}
