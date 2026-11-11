// Motorista: figura de argila em pé (calça escura, camisa verde, cabeça e boné), de frente para +x, 1,75 m. O braço direito vem à
// frente para segurar uma folha: userData.mao = grupo na mão (ponto no pai: use mundo(g.userData.mao, [0,0,0])); userData.topo.
// Uso: const m = motorista(CENA, [x, 0, z]); m.rotation.y = PI / 2 vira o corpo para +z.
import { PI, THREE, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function motorista(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), mCal = M('#2F3640'), mCam = M(o.cor ?? '#3E8E64'), mPele = M('#D9A47E'), mCab = M('#2F3640'), s = o.s ?? 1;
  g.scale.setScalar(s);
  for (const z of [-.09, .09]) { poe(new THREE.CapsuleGeometry(.075, .62, 4, 10), mCal, g, [0, .45, z]); poe(rbox(.27, .08, .13, .03, 1), M(COR.pneu), g, [.04, .04, z]); }
  poe(new THREE.CapsuleGeometry(.2, .42, 5, 14), mCam, g, [0, 1.15, 0], [0, 0, 0], [.72, 1, 1.1]);
  poe(new THREE.CapsuleGeometry(.062, .5, 4, 10), mCam, g, [0, 1.1, -.27], [0, 0, 0]);
  const br = grupo(g, [0, 1.35, .24]); br.rotation.z = 1.25;
  poe(new THREE.CapsuleGeometry(.062, .46, 4, 10), mCam, br, [0, -.3, 0]);
  const mao = grupo(br, [0, -.62, 0]); poe(new THREE.SphereGeometry(.07, 12, 10), mPele, mao);
  poe(new THREE.CylinderGeometry(.05, .06, .08, 10), mPele, g, [0, 1.52, 0]);
  poe(new THREE.SphereGeometry(.15, 18, 14), mPele, g, [0, 1.66, 0]);
  poe(new THREE.SphereGeometry(.158, 18, 10, 0, PI * 2, 0, PI * .5), mCab, g, [-.01, 1.68, 0]);
  poe(rbox(.17, .025, .24, .01, 1), mCab, g, [.14, 1.67, 0]);
  g.userData.mao = mao; g.userData.topo = [0, 1.9 * s, 0]; mancha(g, .8, .7, .3); return g;
}
