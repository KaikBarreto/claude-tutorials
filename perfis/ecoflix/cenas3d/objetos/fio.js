// Fio: um cilindro fino entre dois pontos do mundo que "cresce" de a até b (cordão que liga um documento a um objeto, trilho de
// uma rota). Uso: const f = fio(CENA, COR.verde, .025); a cada quadro: f.liga([x0,y0,z0], [x1,y1,z1], p) com p de 0 a 1
// (p = 0 esconde). Dá para ligar com ponta que se move (a, b mudam a cada quadro).
import { THREE, M } from '../kit3d.js';

const Y = new THREE.Vector3(0, 1, 0), _d = new THREE.Vector3();
export function fio(pai, cor, r = .025) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 8), M(cor)); m.castShadow = true; m.visible = false; pai.add(m);
  m.liga = (a, b, p = 1) => {
    _d.set(b[0] - a[0], b[1] - a[1], b[2] - a[2]); const L = _d.length() * p; m.visible = L > 1e-3; if (!m.visible) return;
    _d.normalize(); m.quaternion.setFromUnitVectors(Y, _d); m.scale.set(1, L, 1);
    m.position.set(a[0] + _d.x * L / 2, a[1] + _d.y * L / 2, a[2] + _d.z * L / 2);
  };
  return m;
}
