// cabo(pai, pontos, o): cabo (tubo de argila) por uma curva suave que passa pelos pontos [[x,y,z], ...] (no pai).
// o: r (raio, .012), cor (padrão grafite), seg (trechos, 48). userData.curva = THREE.CatmullRomCurve3 (getPoint(u) dá um ponto
// para o que "viaja" pelo cabo). caboAte(m, p) desenha o cabo até p (0 a 1), como se ele esticasse da origem ao destino.
// Uso (T05): const usb = cabo(CENA, [[0,.05,0],[1,.02,.4],[2,.05,.5]], { r: .02 }); caboAte(usb, eio(pr(t, a, .6)));
import { THREE, M, COR, cl } from '../kit3d.js';

export function cabo(pai, pts, o = {}) {
  const curva = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p)), false, 'catmullrom', .5);
  const geo = new THREE.TubeGeometry(curva, o.seg ?? 48, o.r ?? .012, 8, false);
  const m = new THREE.Mesh(geo, M(o.cor ?? COR.cinzaE)); m.castShadow = true; pai.add(m);
  m.userData.curva = curva; m.userData.n = geo.index.count; return m;
}
export function caboAte(m, p) {
  p = cl(p); m.visible = p > .002; m.geometry.setDrawRange(0, Math.floor(m.userData.n * p / 48) * 48);
}
