// Caminhão poliguindaste (leva e busca caçamba estacionária): o caminhão do kit sem a caçamba basculante, com dois trilhos de
// aço na carroceria e o braço do gancho no fundo. Uso (a caçamba é de objetos/cacambaEstacionaria.js, c 3,4 · l 1,7 · h 1,1):
//   const T = poliguindaste(CENA, [0, 0, z], { cor: COR.verde }); posiciona(T, x, z, 1 | -1);   // -1 = de frente para -x
//   poseCacamba(T, k, s, x, z, dir)  // s 0 = no chão (atrás do caminhão, encostada), 1 = sobre os trilhos; também mexe no braço
// k.userData.c = comprimento da caçamba (ler de lá). Com a caçamba no chão e s 0, o x do caminhão é x_caçamba + dir·5,0 (s 1: dir·1,2).
import { PI, THREE, lerp, cl, eo, poe, rbox, M, COR } from '../kit3d.js';
import { caminhao } from '../kit3d.js';

export const D_DESLIZE = 3.8, X_CARGA = -1.2, Y_TRILHO = 1.03;
export function poliguindaste(pai, p, o = {}) {
  const g = caminhao(pai, p, { ...o, bau: 'grade', hb: .05, carga: undefined }), u = g.userData, c = o.c ?? 6.6, x0 = -c / 2 + .04, cb = u.bau.cb;
  u.cacamba.visible = false; const mE = M(COR.cinzaE), mG = M('#9AA3AD');
  for (const s of [-1, 1]) poe(rbox(cb, .1, .16, .03, 1), mG, g, [x0 + cb / 2, Y_TRILHO - .05, s * .5]);
  poe(rbox(.3, .34, 1.4, .05, 1), mE, g, [x0 + .1, Y_TRILHO + .1, 0]);   // cavalete do braço
  u.pivo = [x0 + .2, Y_TRILHO + .25];
  u.braco = poe(new THREE.CylinderGeometry(.06, .06, 1, 10), M(COR.aco), g); u.braco.visible = false;
  u.gancho = poe(new THREE.TorusGeometry(.13, .035, 8, 16, PI * 1.5), M(COR.aco), g); u.gancho.visible = false;
  u.rodasR = u.R; return g;
}
export function posiciona(g, x, z, dir = 1) {
  g.position.set(x, 0, z); g.rotation.y = dir > 0 ? 0 : PI; g.userData.rodas.forEach(r => { r.rotation.z = -dir * x / g.userData.R; });
}
// põe a caçamba k (grupo no mundo) em relação ao caminhão g; s de 0 (no chão, encostada) a 1 (sobre os trilhos)
export function poseCacamba(g, k, s, dir = 1) {
  const u = g.userData, c = k.userData.c ?? 3.4, h = k.userData.boca ?? 1.1, e = eo(cl(s));
  const lx = lerp(X_CARGA - D_DESLIZE, X_CARGA, e), ly = Y_TRILHO * Math.pow(e, 1.4), th = .26 * Math.sin(PI * e) * (1 - .3 * e);
  k.position.set(g.position.x + dir * lx, ly, g.position.z); k.rotation.set(0, dir > 0 ? 0 : PI, th);
  // braço: do cavalete até a argola da frente da caçamba (no sistema do caminhão)
  const hx = lx + (c / 2 - .1) * Math.cos(th) - (h * .75) * Math.sin(th), hy = ly + (c / 2 - .1) * Math.sin(th) + (h * .75) * Math.cos(th) + .0;
  const [px, py] = u.pivo, dx = hx - px, dy = hy - py, L = Math.hypot(dx, dy), vis = s < .985;
  u.braco.visible = u.gancho.visible = vis;
  u.braco.position.set((px + hx) / 2, (py + hy) / 2, 0); u.braco.scale.set(1, L, 1); u.braco.rotation.z = -Math.atan2(dx, dy);
  u.gancho.position.set(hx, hy, 0); u.gancho.rotation.z = th;
}
