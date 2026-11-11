// Esteira transportadora (correia escura, guias laterais, roletes nas pontas, pernas). Comprimento em x (c), largura em z (l),
// face de cima da correia a y = h. Para o ímã de separação. Uso: esteira(CENA, [x, 0, z], { c: 9, l: 1.2, h: .9 }); userData.topo = h.
import { PI, THREE, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function esteira(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 9, l = o.l ?? 1.2, h = o.h ?? .9, mB = M('#3A414A'), mG = M('#9AA3AD'), mE = M(COR.cinzaE), mR = M('#B9C1CA');
  poe(rbox(c - .2, .08, l - .22, .03, 1), mB, g, [0, h - .04, 0]);
  for (const s of [-1, 1]) poe(rbox(c, .26, .09, .03, 1), mG, g, [0, h - .1, s * (l / 2 - .045)]);
  for (let x = -c / 2 + .7; x < c / 2 - .5; x += .7) poe(rbox(.05, .014, l - .3, .006, 1), M('#2B3138'), g, [x, h + .004, 0]).castShadow = false;
  for (const s of [-1, 1]) poe(new THREE.CylinderGeometry(.15, .15, l - .16, 18), mR, g, [s * (c / 2 - .12), h - .12, 0], [PI / 2, 0, 0]);
  for (const x of [-c / 2 + .5, 0, c / 2 - .5]) for (const s of [-1, 1]) { poe(rbox(.1, h - .26, .1, .02, 1), mE, g, [x, (h - .26) / 2, s * (l / 2 - .05)]); }
  for (const x of [-c / 2 + .5, 0, c / 2 - .5]) poe(rbox(.1, .08, l, .02, 1), mE, g, [x, h - .3, 0]);
  g.userData.topo = h; mancha(g, c + 1, l + 1, .26); return g;
}
