// Estrada: faixa de asfalto cinza com acostamento claro e linha central tracejada, ao longo de x (c) e z (l); topo em y .03.
// Uso: estrada(CENA, [cx, 0, 0], { c: 30, l: 2.6 }). Para marcar a divisa de um estado, use porticoEstado em cima dela.
import { PI, grupo, poe, rbox, M, COR } from '../kit3d.js';

export function estrada(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 30, l = o.l ?? 2.6;
  poe(rbox(c, .06, l + .5, .03, 1), M('#C5CCD4'), g, [0, .0, 0]).castShadow = false;
  poe(rbox(c, .06, l, .03, 1), M('#6B7580'), g, [0, .015, 0]).castShadow = false;
  for (let x = -c / 2 + .8; x < c / 2 - 1; x += 1.9) poe(rbox(.9, .006, .09, .003, 1), M('#F4F6F8'), g, [x + .45, .05, 0]).castShadow = false;
  for (const s of [-1, 1]) poe(rbox(c - .2, .006, .05, .002, 1), M(COR.ambar), g, [0, .05, s * (l / 2 - .12)]).castShadow = false;
  return g;
}
