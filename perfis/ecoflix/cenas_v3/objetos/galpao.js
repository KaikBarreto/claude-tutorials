// Galpão genérico (paredes claras, telhado de duas águas, porta de enrolar e uma placa âmbar lisa), sem nome nem marca.
// uso: galpao(CENA, [x, 0, z], { c: 12, l: 8, h: 4.5 });   como ícone de estação, menor: g.scale.setScalar(.4)
// Frente para +z. o: porta (true), cor (paredes), telhado (cor). userData: topo (acima do cume), porta (ponto no chão, à frente), placa.
import { mat, caixa, perfil, malha, grupo, mancha } from '../motor.js';
export function galpao(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 12, l = o.l ?? 8, h = o.h ?? 4.5, hc = h + c * .16, g = grupo(pai, pos), A = { alt: hc, emi: .11 }, par = mat(o.cor ?? '#EEF2F5', A), tel = mat(o.telhado ?? '#8F9BAA', { ...A, emi: .22 }), esc = mat('#56626F', { ...A, emi: .24 });
  mancha(c + 5, l + 4.5, [0, 0, .2], { pai: g, op: .75 });
  malha(perfil([[-c / 2, 0], [c / 2, 0], [c / 2, h], [0, hc], [-c / 2, h]], [.05, .05, .05, .1, .05], l, .06), par, [0, 0, 0], g);
  const L = Math.hypot(c / 2, hc - h) + .5, a = Math.atan2(hc - h, c / 2);
  for (const s of [-1, 1]) malha(caixa(L, .16, l + .7, .05), tel, [s * (c / 4 + .12), (h + hc) / 2 + .1, 0], g, [0, 0, -s * a]);
  malha(caixa(c + .1, .5, l + .1, .05), mat('#D9E0E7', A), [0, .25, 0], g);   // rodapé
  if (o.porta !== false) { const pw = Math.min(c * .42, 4.6), ph = Math.min(h * .82, 4); malha(caixa(pw + .3, ph + .15, .12, .04), esc, [0, ph / 2 + .07, l / 2 + .02], g);
    for (let i = 0; i < Math.floor(ph / .3); i++) malha(caixa(pw, .25, .06, .02), mat('#C3CCD5', A), [0, .16 + i * .3, l / 2 + .08], g); }
  malha(caixa(c * .3, .7, .1, .04), mat('#F2B63D', { emi: .5, alt: hc }), [0, h + c * .03 + .1, l / 2 + .06], g);
  g.userData = { topo: [0, hc + .9, 0], porta: [0, 0, l / 2 + 1.5], placa: [0, h + c * .03 + .1, l / 2 + .12] }; return g;
}
