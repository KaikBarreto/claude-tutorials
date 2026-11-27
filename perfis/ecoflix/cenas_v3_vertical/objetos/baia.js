// Baia de estoque do pátio: três muretas de concreto (fundo e laterais), aberta para +z, com a borda de cima marcada.
// uso: const b = baia(CENA, [x, 0, z], { c: 4, l: 3, h: 1.5 }); monte(b, [0, 0, -.2], { tipo: 'cobre', r: 1.4, mancha: false });
// userData: dentro (centro do chão), topo (acima do meio do fundo: o chip do material vai ali), c, l, h.
import { mat, caixa, malha, grupo, mancha } from '../motor.js';
export function baia(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 4, l = o.l ?? 3, h = o.h ?? 1.5, e = o.e ?? .26, g = grupo(pai, pos), m = mat('#E3E8EC', { alt: h, emi: .11 }), b = mat(o.cor ?? '#AEB9C5', { alt: h + .5, emi: .14 });
  mancha(c + 2.6, l + 2.4, [0, 0, .1], { pai: g, op: .7 });
  malha(caixa(c + 2 * e, h, e, .05), m, [0, h / 2, -l / 2 - e / 2], g); malha(caixa(c + 2 * e + .04, .09, e + .04, .03), b, [0, h, -l / 2 - e / 2], g);
  for (const s of [-1, 1]) { malha(caixa(e, h, l, .05), m, [s * (c / 2 + e / 2), h / 2, 0], g); malha(caixa(e + .04, .09, l + .02, .03), b, [s * (c / 2 + e / 2), h, 0], g); }
  g.userData = { c, l, h, dentro: [0, 0, 0], topo: [0, h + .7, -l / 2] }; return g;
}
