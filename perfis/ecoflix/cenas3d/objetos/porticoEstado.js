// Pórtico de divisa de estado: dois pilares e uma viga sobre a estrada (z de -l/2 a l/2), sem letra: a sigla (SP, RJ, MG) é
// um chip HTML preso a userData.topo com ancora(). Uso: porticoEstado(CENA, [x, 0, 0], { l: 2.6, h: 2.4 }).
import { PI, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function porticoEstado(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), l = o.l ?? 2.6, h = o.h ?? 2.4, mc = M(o.cor ?? '#9AA3AD');
  for (const s of [-1, 1]) { poe(rbox(.2, h, .2, .05, 1), mc, g, [0, h / 2, s * (l / 2 + .45)]); mancha(g, .8, .8, .2, [0, 0, s * (l / 2 + .45)]); }
  poe(rbox(.34, .5, l + 1.2, .06, 1), M(o.corViga ?? COR.verde), g, [0, h + .05, 0]);
  g.userData.topo = [0, h + .5, 0]; return g;
}
