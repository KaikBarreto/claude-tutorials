// cancela(pai, p, o): cancela de pátio (caixa-base cinza e braço listrado âmbar e branco). O braço fecha ao longo de +z (atravessa a
// pista) e sobe até a vertical. o: l (comprimento do braço, 3.0). ergue(g, a): a de 0 (fechada) a 1 (aberta, vertical).
// Origem no pé da base. userData.topo (ponto acima da base).
// Uso (T16): const cn = cancela(CENA, [x, 0, -1.6]); ergue(cn, eio(pr(t, tMer, .7)));
import { PI, THREE, grupo, poe, rbox, M, COR, mancha, cl } from '../kit3d.js';

export function cancela(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), l = o.l ?? 3.0, pv = grupo(g, [0, 1.0, .08]);
  poe(rbox(.34, 1.1, .34, .07, 2), M('#9AA3AD'), g, [0, .55, 0]); poe(rbox(.38, .1, .38, .04, 1), M(COR.cinzaE), g, [0, 1.12, 0]);
  poe(new THREE.CylinderGeometry(.09, .09, .36, 16), M(COR.cinzaE), pv, [0, 0, 0], [0, 0, PI / 2]);
  const n = 6, sg = (l - .2) / n; for (let i = 0; i < n; i++) poe(rbox(.07, .1, sg, .02, 1), M(i % 2 ? '#F7F8F9' : COR.ambar), pv, [0, 0, .2 + sg * (i + .5)]);
  poe(rbox(.08, .08, .08, .02, 1), M('#C8553D'), pv, [0, 0, l]);
  g.userData.pv = pv; g.userData.topo = [0, 1.3, 0]; mancha(g, 1, 1, .26); ergue(g, 0); return g;
}
export function ergue(g, a) { g.userData.pv.rotation.x = -cl(a) * (PI / 2 - .04); }
