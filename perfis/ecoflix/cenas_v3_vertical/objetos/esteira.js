// Esteira transportadora: correia escura com travessas (andam com corre), guias laterais, roletes nas pontas e pernas.
// uso: const e = esteira(CENA, [x, 0, z], { c: 9, l: 1.2, h: .9 }); corre(e, dist);   // dist em metros (ex.: 1.2 * t)
// Comprimento em x; a face de cima da correia fica em userData.topo (y). O material vai por cima: pecas(e, 'misto', pontos).
import { mat, caixa, cil, malha, grupo, mancha, lote, poeInst, PI } from '../motor.js';
export function esteira(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 9, l = o.l ?? 1.2, h = o.h ?? .9, g = grupo(pai, pos), esc = mat('#39424A', { alt: 1.2, bri: .1, emi: .28 }), aco = mat('#AEB9C5', { alt: 1.2, emi: .14 }), vd = mat('#50D088', { alt: 1.2, emi: .5 });
  mancha(c + 2, l + 1.8, [0, 0, .1], { pai: g, op: .75 });
  malha(caixa(c, .12, l, .055), esc, [0, h - .06, 0], g);
  for (const x of [-c / 2, c / 2]) malha(cil(.085, l + .06, 18), aco, [x, h - .06, 0], g, [PI / 2, 0, 0]);
  for (const z of [-1, 1]) { malha(caixa(c + .1, .16, .06, .025), vd, [0, h + .03, z * (l / 2 + .04)], g); malha(caixa(c - .3, .08, .05, .02), aco, [0, h - .2, z * (l / 2 + .02)], g); }
  const n = Math.max(2, Math.round(c / 3)); for (let i = 0; i < n; i++) for (const z of [-1, 1]) { const x = -c / 2 + .6 + i * (c - 1.2) / (n - 1); malha(caixa(.1, h - .16, .1, .03), aco, [x, (h - .16) / 2, z * (l / 2 - .04)], g); malha(caixa(.26, .04, .2, .015), esc, [x, .02, z * (l / 2 - .04)], g); }
  const passo = .6, nt = Math.floor((c - .3) / passo), tr = lote(caixa(.05, .016, l - .16, .006), mat('#59646F', { emi: .32 }), nt, g);
  g.userData = { c, l, h, topo: h, tr, nt, passo }; corre(g, 0); return g;
}
export function corre(g, d) { const u = g.userData, L = u.nt * u.passo; for (let i = 0; i < u.nt; i++) poeInst(u.tr, i, [(((i * u.passo + d) % L) + L) % L - L / 2 + u.passo / 2, u.h + .004, 0]); }
