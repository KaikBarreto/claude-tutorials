// Ímã de separação (ferradura de aço com as pontas claras) pendurado num carrinho sobre um trilho; e o trilho. Origem do ímã
// = centro do arco; as pontas ficam em x = ±R, com a base a y = -0,66 (userData.ponta = [R, -0,66]); userData.topo = y do carrinho.
// campo(g, a): anéis verdes de atração nas pontas (a de 0 a 1). Uso: const im = ima(CENA, [x, y, z]); trilho(CENA, -3.5, 8.5, 3.7, 0).
// O ímã anda em x e o trilho passa por cima (o carrinho é do ímã). Sem marca; cores da paleta do kit.
import { PI, THREE, grupo, poe, rbox, M, COR } from '../kit3d.js';

export function ima(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), R = o.R ?? .5, e = .16, mC = M('#4F5861'), mP = M('#D3DAE1'), mE = M(COR.cinzaE), H = o.H ?? .55;
  poe(new THREE.TorusGeometry(R, e, 12, 28, PI), mC, g);
  for (const s of [-1, 1]) { poe(rbox(2 * e, .5, 2 * e, .04, 1), mC, g, [s * R, -.25, 0]); poe(rbox(2 * e + .02, .16, 2 * e + .02, .03, 1), mP, g, [s * R, -.58, 0]); }
  const yt = R + e + H;
  poe(new THREE.CylinderGeometry(.04, .04, H + .05, 10), M(COR.aco), g, [0, R + e + H / 2, 0]);
  poe(rbox(.7, .2, .5, .05, 1), mE, g, [0, yt + .08, 0]);
  const rods = [];
  for (const s of [-1, 1]) for (const [y, r] of [[-.4, R * .54], [-.6, R * .62]]) { const t = new THREE.Mesh(new THREE.TorusGeometry(r, .018, 6, 36), new THREE.MeshBasicMaterial({ color: 0x50D088, transparent: true, opacity: 0, depthWrite: false }));
    t.position.set(s * R, y, 0); t.rotation.x = PI / 2; t.renderOrder = 3; g.add(t); rods.push(t); }
  g.userData.ponta = [R, -.66]; g.userData.topo = yt + .18; g.userData.campo = rods; return g;
}
export function campo(g, a) { for (const t of g.userData.campo) { t.material.opacity = .85 * a; t.visible = a > .01; t.scale.setScalar(.85 + .15 * a); } }
// trilho: duas vigas ao longo de x de x0 a x1, a altura y (face de baixo), z; dois postes até o chão
export function trilho(pai, x0, x1, y, z = 0) {
  const g = grupo(pai, [0, 0, z]), m = M('#9AA3AD'), mE = M(COR.cinzaE);
  for (const s of [-1, 1]) poe(rbox(x1 - x0, .12, .1, .03, 1), m, g, [(x0 + x1) / 2, y + .06, s * .3]);
  for (const x of [x0, x1]) { poe(rbox(.12, y, .12, .03, 1), mE, g, [x, y / 2, 0]); poe(rbox(.16, .12, .8, .03, 1), mE, g, [x, y + .06, 0]); poe(rbox(.5, .06, .5, .02, 1), mE, g, [x, .03, 0]); }
  return g;
}
