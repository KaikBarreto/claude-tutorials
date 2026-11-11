// fundicao(pai, p, o): fundição genérica (galpão baixo cinza-azulado, forno em cúpula, portão escuro com brilho âmbar e chaminé
// com faixa âmbar), sem nome nem marca: o nome é um chip HTML preso a userData.topo com ancora(). Frente para +z, base em y 0.
// o: c (6), l (4), h (2.4). Uso (T16): fundicao(CENA, [x, 0, z], { c: 6 }).
import { PI, THREE, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function fundicao(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 6, l = o.l ?? 4, h = o.h ?? 2.4, mP = M('#D3DAE1'), mT = M('#7A8794');
  poe(rbox(c, h, l, .06, 2), mP, g, [0, h / 2, 0]);
  poe(rbox(c + .3, .2, l + .3, .05, 1), mT, g, [0, h + .1, 0]);
  poe(rbox(c * .36, h * .74, .1, .05, 1), M(COR.cinzaE), g, [-c * .12, h * .37, l / 2 + .01]);
  poe(rbox(c * .26, h * .5, .05, .04, 1), M('#F2B63D', { r: .55 }), g, [-c * .12, h * .3, l / 2 + .06]);
  poe(new THREE.SphereGeometry(1.15, 24, 14, 0, PI * 2, 0, PI / 2), M('#98A3AE'), g, [c * .3, h, -l * .05], [0, 0, 0], [1, .8, 1]);
  poe(new THREE.CylinderGeometry(.18, .18, .6, 14), M(COR.cinzaE), g, [c * .3, h + .8, -l * .05 + .9], [PI / 2, 0, 0]);
  const ch = c * .36; poe(new THREE.CylinderGeometry(.3, .42, 3.4, 20), mT, g, [-c / 2 + .8, h + 1.7, -l * .1]);
  poe(new THREE.CylinderGeometry(.43, .43, .34, 20), M(COR.ambar), g, [-c / 2 + .8, h + 2.9, -l * .1]);
  poe(new THREE.CylinderGeometry(.34, .34, .18, 20), M(COR.cinzaE), g, [-c / 2 + .8, h + 3.45, -l * .1]);
  g.userData.topo = [0, h + .5, l / 2]; mancha(g, c + 1.6, l + 1.4, .3); return g;
}
