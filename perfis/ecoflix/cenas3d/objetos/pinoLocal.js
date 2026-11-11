// Pino de local (gota virada para baixo, verde, com miolo branco): marca origem/destino. A ponta fica em p. Altura total ≈ 1 * s.
// Uso: const pn = pinoLocal(CENA, [x, 0, z]); flutua com pn.position.y = 0.1 * Math.sin(t * 2). userData.topo.
import { PI, THREE, grupo, poe, M, COR } from '../kit3d.js';

export function pinoLocal(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), s = o.s ?? 1, mc = M(o.cor ?? COR.verde);
  g.scale.setScalar(s);
  poe(new THREE.SphereGeometry(.3, 22, 16), mc, g, [0, .78, 0]);
  poe(new THREE.ConeGeometry(.24, .55, 20), mc, g, [0, .27, 0], [PI, 0, 0]);
  poe(new THREE.SphereGeometry(.11, 14, 10), M('#FFFFFF'), g, [0, .8, .22]);
  g.userData.topo = [0, 1.15 * s, 0]; return g;
}
