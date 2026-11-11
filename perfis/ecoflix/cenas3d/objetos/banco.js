// banco(pai, p, o): prédio de banco genérico, sem nome nem marca: escada, quatro colunas, viga e frontão com um disco verde, e a
// parede do fundo com a porta. Frente para +z, base em y 0, centro em x/z, ~2,6 x 2,7 x 1,9 m. o.s = escala.
// userData.topo = ponto acima do frontão; userData.porta = ponto (local) na frente da porta, no chão.
// Uso (T00, a estação "Dinheiro na conta"): const bc = banco(CENA, [x, 0, z]);
import { PI, THREE, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function banco(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), b = grupo(g), mC = M('#C9D1DA'), mE = M('#7E8994'), mF = M('#5B636C');
  b.scale.setScalar(o.s ?? 1);
  poe(rbox(2.7, .14, 1.95, .04, 2), M('#AEB7C1'), b, [0, .07, 0]); poe(rbox(2.5, .14, 1.75, .04, 2), M('#B9C1CA'), b, [0, .21, -.04]);
  poe(rbox(2.3, .08, 1.55, .03, 1), mE, b, [0, .32, -.06]);
  poe(rbox(2.1, 1.75, .9, .04, 2), M('#DDE3E8'), b, [0, 1.2, -.42]);                                      // parede do fundo
  poe(rbox(.6, 1.1, .06, .03, 1), M('#4F5861'), b, [0, .92, .05]);                                         // porta
  for (const x of [-.9, -.3, .3, .9]) { poe(new THREE.CylinderGeometry(.11, .12, 1.7, 18), mC, b, [x, 1.21, .5]);
    poe(rbox(.3, .06, .3, .02, 1), mE, b, [x, .39, .5]); poe(rbox(.3, .06, .3, .02, 1), mE, b, [x, 2.09, .5]); }
  poe(rbox(2.4, .22, 1.55, .04, 2), mF, b, [0, 2.23, -.06]);                                               // viga
  const fr = new THREE.ExtrudeGeometry(new THREE.Shape([[-1.25, 0], [1.25, 0], [0, .62]].map(v => new THREE.Vector2(...v))),
    { depth: 1.45, bevelEnabled: true, bevelThickness: .03, bevelSize: .03, bevelSegments: 2, curveSegments: 1 });
  fr.translate(0, 0, -.78); poe(fr, mF, b, [0, 2.34, 0]);                                                   // frontão
  poe(new THREE.CylinderGeometry(.15, .15, .05, 28), M(COR.verde), b, [0, 2.58, .72], [PI / 2, 0, 0]);
  mancha(g, 3.4, 2.6, .28);
  g.userData.topo = [0, 3.15 * (o.s ?? 1), 0]; g.userData.porta = [0, 0, 1.1]; return g;
}
