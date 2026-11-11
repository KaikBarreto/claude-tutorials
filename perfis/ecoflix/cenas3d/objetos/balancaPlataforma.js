// balancaPlataforma(pai, p, o): balança de plataforma (a de pesar saco e fardo no chão, ligada por cabo ao computador): base baixa
// cinza com tampo, quatro pés, poste e cabeça do indicador com o visor aceso LISO (sem número: o número é o mostrador HTML preso
// a userData.topo com ancora()). Frente para +z, base em y 0. o: c (comprimento em x, 1.0), l (largura em z, .8).
// userData.sup = altura do tampo (onde a carga apoia), userData.topo = ponto acima da cabeça, userData.saida = onde o cabo sai.
// Uso (T05): const b = balancaPlataforma(CENA, [x, 0, z]); saco(CENA, [x, b.userData.sup, z]).
import { PI, THREE, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function balancaPlataforma(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 1.0, l = o.l ?? .8, px = c / 2 - .12, pz = -l / 2 + .1;
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) poe(new THREE.CylinderGeometry(.04, .045, .04, 12), M(COR.cinzaE), g, [sx * (c / 2 - .08), .02, sz * (l / 2 - .08)]);
  poe(rbox(c, .08, l, .03, 2), M('#8E98A3'), g, [0, .08, 0]);
  poe(rbox(c - .08, .024, l - .08, .012, 1), M(COR.cinzaC), g, [0, .132, 0]);
  const n = Math.floor((c - .3) / .12); for (let i = 0; i < n; i++) poe(rbox(.02, .006, l - .2, .003, 1), M('#A5AEB8'), g, [(i - (n - 1) / 2) * .12, .147, 0]);
  poe(rbox(.1, .035, .1, .02, 1), M('#9AA3AD'), g, [px, .17, pz]);
  poe(new THREE.CylinderGeometry(.028, .034, .9, 14), M('#B9C1C9'), g, [px, .6, pz]);
  const cab = grupo(g, [px, 1.1, pz + .02]); cab.rotation.x = .28;
  poe(rbox(.4, .22, .08, .035, 2), M(COR.escuro), cab); poe(rbox(.32, .12, .012, .006, 1), M('#2E7D57'), cab, [0, .02, .043]);
  for (const x of [-.12, 0, .12]) poe(new THREE.CylinderGeometry(.016, .016, .01, 10), M(COR.cinzaC), cab, [x, -.075, .043], [PI / 2, 0, 0]);
  g.userData.sup = .144; g.userData.topo = [px, 1.3, pz]; g.userData.saida = [px, .05, pz + .12];
  mancha(g, c + .9, l + .8, .26); return g;
}
