// Fundição genérica (o destino do material): galpão baixo cinza-azulado, forno em cúpula, portão escuro com o brilho âmbar
// e a chaminé de faixa âmbar. Sem nome nem marca (o nome é um chip em userData.topo).
// uso: fundicao(CENA, [x, 0, z], { c: 12, l: 8, h: 4.6 });  Frente para +z. userData: topo, porta, chamine.
import { mat, caixa, cil, esfera, malha, grupo, mancha } from '../motor.js';
export function fundicao(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 12, l = o.l ?? 8, h = o.h ?? 4.6, g = grupo(pai, pos), A = { alt: h * 1.6, emi: .13 }, par = mat('#B9C6D3', A), esc = mat('#6F7C8A', { ...A, emi: .24 }), amb = mat('#F2B63D', { emi: .65, alt: h * 2 });
  mancha(c + 5, l + 4.5, [0, 0, .2], { pai: g, op: .75 });
  malha(caixa(c, h, l, .12), par, [0, h / 2, 0], g); malha(caixa(c + .3, .3, l + .3, .08), esc, [0, h + .05, 0], g); malha(caixa(c + .1, .5, l + .1, .05), esc, [0, .25, 0], g);
  malha(esfera(l * .3, [1, .8, 1], 28), mat('#8F9BAA', A), [-c * .2, h, 0], g); malha(cil(.5, .6, 18, .36), esc, [-c * .2, h + l * .25, 0], g);
  malha(caixa(c * .28, h * .7, .12, .05), mat('#2B323B', { bri: .08, emi: .24 }), [c * .2, h * .35, l / 2 + .02], g);
  malha(caixa(c * .24, h * .22, .08, .03), mat('#F7A93B', { emi: 1.21, emiC: .25, bri: .3 }), [c * .2, h * .14, l / 2 + .07], g);   // o brilho do forno
  const hx = c * .36, hh = h * 1.9; malha(cil(.55, hh, 22, .42), par, [hx, hh / 2, -l * .2], g); malha(cil(.5, .5, 22, .47), amb, [hx, hh * .8, -l * .2], g); malha(cil(.46, .14, 22), esc, [hx, hh + .05, -l * .2], g);
  for (let i = 0; i < 3; i++) malha(caixa(c * .1, .8, .06, .03), mat('#DDF1F7', { emi: .88, bri: .35 }), [-c * .36 + i * c * .14, h * .66, l / 2 + .03], g);
  g.userData = { topo: [0, h + l * .3 + 1.2, 0], porta: [c * .2, 0, l / 2 + 1.5], chamine: [hx, hh + .2, -l * .2] }; return g;
}
