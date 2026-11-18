// Caminhão poliguindaste (leva e busca a caçamba estacionária): o caminhão do kit sem a caçamba basculante, com dois trilhos
// na carroceria e os dois braços que giram na traseira, com as correntes.
// uso: const T = poliguindaste(CENA, { placa: 'RCV2E26' }); const k = cacambaEstacionaria(CENA, [0, 0, 0]);
//      posiciona(T, x, z, 1 | -1);            // -1 = de frente para -x
//      poseCacamba(T, k, s, dir);             // s 0 = caçamba no chão, atrás do caminhão; 1 = sobre os trilhos (o braço acompanha)
// Com a caçamba no chão (s 0) em xk, o caminhão fica em xk - dir * lxCarga(0). Sem caçamba: poseCacamba(T, null, s) só mexe o braço.
import { PI, cl, lerp, eio, mat, caixa, cil, malha, grupo } from '../motor.js';
import { caminhao, dirige } from './caminhao.js';
export const D_DESLIZE = 4.3, X_CARGA = -1.25, Y_TRILHO = 1.12, BRACO = 2.7, PIVO = [-3.35, 1.0];
export const lxCarga = s => lerp(X_CARGA - D_DESLIZE, X_CARGA, eio(cl(s)));
export function poliguindaste(pai, o = {}) {
  const T = caminhao(pai, { ...o, bau: 'nenhum', carga: 0 }), u = T.userData, c = u.corpo, aco = mat('#8F9BAA', { alt: 3, emi: .14 }), esc = mat('#2B323B', { bri: .12 }), amb = mat('#F2B63D', { emi: .36, alt: 3 });
  malha(caixa(5.0, .12, 2.3, .04), aco, [-1.2, .93, 0], c); for (const z of [-.62, .62]) malha(caixa(4.9, .1, .14, .03), esc, [-1.2, 1.04, z], c);
  malha(caixa(.12, 1.5, 2.2, .04), aco, [1.26, 1.7, 0], c);   // anteparo atrás da cabine
  for (const z of [-1.08, 1.08]) { malha(caixa(.5, .5, .16, .05), esc, [PIVO[0], PIVO[1], z], c); malha(caixa(.16, .5, .16, .04), esc, [-3.55, .5, z], c); malha(caixa(.3, .06, .3, .02), aco, [-3.55, .24, z], c); }
  const braco = grupo(c, [PIVO[0], PIVO[1], 0]);
  for (const z of [-1.08, 1.08]) { malha(caixa(.2, BRACO, .14, .05), amb, [0, BRACO / 2, z], braco); malha(cil(.09, .22, 14), esc, [0, 0, z], braco, [PI / 2, 0, 0]); }
  malha(cil(.07, 2.3, 12), esc, [0, BRACO, 0], braco, [PI / 2, 0, 0]);
  const correntes = [0, 1, 2, 3].map(() => malha(cil(.022, 1, 6), esc, [0, 0, 0], c)); u.braco = braco; u.correntes = correntes; u.dir = 1;
  poseCacamba(T, null, 1); return T;
}
export function posiciona(T, x, z, dir = 1) { dirige(T, x); T.position.z = z; T.rotation.y = dir < 0 ? PI : 0; T.userData.dir = dir; for (const r of T.userData.rodas) r.rotation.y = dir * x / .52; }
// caçamba k em relação ao caminhão; s de 0 (no chão, atrás) a 1 (sobre os trilhos). A caçamba sobe num arco, pendurada no braço.
export function poseCacamba(T, k, s, dir = T.userData.dir ?? 1) {
  const u = T.userData, e = eio(cl(s)), lx = lerp(X_CARGA - D_DESLIZE, X_CARGA, e), h = k?.userData.h ?? 1.1, y = lerp(0, Y_TRILHO, e) + .55 * Math.sin(PI * e) ** 1.2;
  // o braço aponta da dobradiça para um ponto acima do meio da caçamba
  const ax = lx - PIVO[0], ay = y + h + .95 - PIVO[1], ang = Math.atan2(-ax, ay); u.braco.rotation.z = ang;
  const tx = PIVO[0] - Math.sin(ang) * BRACO, ty = PIVO[1] + Math.cos(ang) * BRACO, c = k?.userData.c ?? 3.4, l = k?.userData.l ?? 1.7;
  u.correntes.forEach((m, i) => { const px = lx + (i < 2 ? -1 : 1) * c * .34, py = y + h - .22, pz = (i % 2 ? 1 : -1) * (l / 2 + .12), z0 = (i % 2 ? 1 : -1) * 1.0, dx = px - tx, dy = py - ty, dz = pz - z0, L = Math.hypot(dx, dy, dz);
    m.visible = !!k; m.position.set((tx + px) / 2, (ty + py) / 2, (z0 + pz) / 2); m.scale.set(1, L, 1); m.quaternion.setFromUnitVectors(m.up, m.position.clone().set(dx / L, dy / L, dz / L)); });
  if (k) { k.position.set(T.position.x + dir * lx * u.k, T.position.y + y * u.k, T.position.z); k.rotation.y = dir < 0 ? PI : 0; if (k.userData.sombra) k.userData.sombra.material.uniforms.uOp.value = .8 * (1 - e); }
}
