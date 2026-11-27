// Guichê do caixa do pátio: casinha clara com a janela de atendimento, o balcão para fora (onde vai a registradora.js) e a
// laje verde por cima. Sem nome nem marca. Frente para +z.
// uso: const gu = guiche(CENA, [x, 0, z]); registradora(gu, [-.4, gu.userData.balcao[1], gu.userData.balcao[2]]);
// o: c (2.6), l (1.9), h (2.4), cor, laje. userData: balcao (meio do tampo, do lado de fora), janela, topo.
import { mat, caixa, malha, grupo, mancha } from '../motor.js';
export function guiche(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 2.6, l = o.l ?? 1.9, h = o.h ?? 2.4, g = grupo(pai, pos), A = { alt: h + .4, emi: .12 }, par = mat(o.cor ?? '#EEF2F5', A), cz = mat('#CBD3DC', A);
  mancha(c + 2.4, l + 2.6, [0, 0, .3], { pai: g, op: .75 });
  malha(caixa(c, h, l, .08), par, [0, h / 2, 0], g); malha(caixa(c + .06, .3, l + .06, .04), cz, [0, .15, 0], g);
  malha(caixa(c + .7, .2, l + 1.3, .07), mat(o.laje ?? '#50D088', { emi: .3, alt: h + .5, bri: .25 }), [0, h + .1, .3], g);
  const jw = c * .68, jh = .95, jy = 1.62; malha(caixa(jw + .16, jh + .16, .08, .04), cz, [0, jy, l / 2 + .01], g);
  malha(caixa(jw, jh, .06, .03), mat('#2E3A44', { bri: .3, emi: .36 }), [0, jy, l / 2 + .04], g); malha(caixa(jw * .5, .05, .07, .02), mat('#DDF1F7', { emi: .88 }), [0, jy - jh / 2 + .12, l / 2 + .05], g);
  malha(caixa(c * .9, .08, .6, .03), mat('#D8B58C', { alt: h, emi: .14 }), [0, 1.04, l / 2 + .28], g); for (const s of [-1, 1]) malha(caixa(.07, .3, .5, .02), cz, [s * c * .36, .88, l / 2 + .22], g);
  g.userData = { balcao: [0, 1.08, l / 2 + .3], janela: [0, jy, l / 2 + .08], topo: [0, h + .9, 0] }; return g;
}
