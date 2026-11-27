// Fio: cilindro fino entre dois pontos que "cresce" de a até b (o cordão que liga um documento a um objeto, o trilho de uma rota).
// uso: const f = fio(CENA, '#50D088', .03); a cada quadro: f.liga([x0, y0, z0], [x1, y1, z1], p)   // p de 0 a 1 (0 esconde)
// As pontas podem se mover (a e b mudam a cada quadro). No clima escuro o fio é aceso.
import { mat, cil, malha, THREE } from '../motor.js';
const _a = new THREE.Vector3(), _d = new THREE.Vector3(), _y = new THREE.Vector3(0, 1, 0);
export function fio(pai, cor = '#50D088', r = .025) {
  const m = malha(cil(r, 1, 10), mat(cor, { emi: 1.1, emiC: .1, bri: .1 }), [0, 0, 0], pai); m.visible = false;
  m.liga = (a, b, p = 1) => { p = Math.min(1, Math.max(0, p)); m.visible = p > .001; if (!m.visible) return; _a.set(a[0], a[1], a[2]); _d.set(b[0] - a[0], b[1] - a[1], b[2] - a[2]); const L = _d.length() * p; if (L < 1e-5) { m.visible = false; return; }
    _d.normalize(); m.position.copy(_a).addScaledVector(_d, L / 2); m.scale.set(1, L, 1); m.quaternion.setFromUnitVectors(_y, _d); };
  return m;
}
