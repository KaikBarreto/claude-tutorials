// cedula(pai, p, o): cédula genérica de argila (retângulo verde-claro com a borda e o oval do meio mais escuros), sem número nem
// marca, deitada (face para +y), pivô no centro. o: cor (#9ED9B5), w (.16), d (.075). Para voar, mexa em position/rotation.
// Uso (T00): const n = cedula(CENA, [x, y, z]); a gaveta da registradora.js já vem com elas.
import { THREE, grupo, poe, rbox, M } from '../kit3d.js';

export function cedula(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), w = o.w ?? .16, d = o.d ?? .075;
  poe(rbox(w, .006, d, .003, 1), M(o.cor ?? '#9ED9B5'), g);
  poe(rbox(w * .9, .002, d * .8, .001, 1), M('#B7E4C7'), g, [0, .0035, 0]);
  poe(new THREE.CylinderGeometry(d * .26, d * .26, .002, 18), M('#7CC69B'), g, [0, .005, 0], [0, 0, 0], [1.3, 1, 1]);
  g.traverse(m => { if (m.isMesh) m.castShadow = false; });
  return g;
}
