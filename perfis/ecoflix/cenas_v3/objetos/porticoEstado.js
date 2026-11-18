// Pórtico de divisa de estado sobre a estrada: dois pilares e uma viga com a faixa verde, sem letra (a sigla SP, RJ, MG é um chip
// preso a userData.topo). A estrada passa ao longo de x; o pórtico atravessa em z.
// uso: porticoEstado(CENA, [x, 0, 0], { l: 7, h: 5.2 });  userData: topo, viga (meio da viga)
import { mat, caixa, malha, grupo, mancha } from '../motor.js';
export function porticoEstado(pai, pos = [0, 0, 0], o = {}) {
  const l = o.l ?? 7, h = o.h ?? 5.2, g = grupo(pai, pos), con = mat('#E3E8EC', { alt: h, emi: .11 }), cz = mat('#AEB9C5', { alt: h, emi: .14 });
  mancha(2.4, l + 3.4, [0, 0, 0], { pai: g, op: .6 });
  for (const s of [-1, 1]) { malha(caixa(.6, h, .6, .08), con, [0, h / 2, s * (l / 2 + .6)], g); malha(caixa(.8, .16, .8, .05), cz, [0, .08, s * (l / 2 + .6)], g); }
  malha(caixa(.7, .8, l + 2.2, .1), con, [0, h + .1, 0], g); malha(caixa(.74, .2, l + 2.24, .06), mat('#50D088', { emi: .6, alt: h + 1 }), [0, h - .2, 0], g);
  g.userData = { topo: [0, h + 1.1, 0], viga: [0, h + .1, 0] }; return g;
}
