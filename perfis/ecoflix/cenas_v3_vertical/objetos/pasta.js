// Pasta de arquivo (âmbar: fundo alto com a aba e a frente mais baixa), em pé, face para +z, origem no centro da base.
// A folha entra entre o fundo e a frente: ponha-a em userData.dentro e desça-a até a frente cobrir.
// uso: const pa = pasta(CENA, [x, 0, z], { w: 1.2 });  userData: dentro, boca, topo, w, h
import { mat, caixa, perfil, malha, grupo, mancha } from '../motor.js';
export function pasta(pai, pos = [0, 0, 0], o = {}) {
  const w = o.w ?? 1.0, h = o.h ?? w * .76, g = grupo(pai, pos), A = { alt: h * 1.3, emi: .32, bri: .2 }, amb = mat(o.cor ?? '#F2B63D', A), ambE = mat('#DFA02E', A), e = w * .03;
  mancha(w + .9 * w, w * .9, [0, 0, .04], { pai: g, op: .65 });
  malha(caixa(w, h, e, e * .45), ambE, [0, h / 2, -e * 2.2], g);
  malha(perfil([[-w * .46, h], [-w * .08, h], [-w * .02, h + w * .09], [w * .3, h + w * .09], [w * .36, h]], w * .025, e, e * .4), ambE, [0, -e * .2, -e * 2.2], g);
  malha(caixa(w, h * .86, e, e * .45), amb, [0, h * .43, e * 2.2], g); malha(caixa(w, e * 1.2, e * 5.4, e * .4), ambE, [0, e * .6, 0], g);
  malha(caixa(w * .3, h * .13, e * .3, e * .1), mat('#FBFBF7', { emi: .5 }), [0, h * .5, e * 2.75], g);
  g.userData = { w, h, dentro: [0, h * .5, 0], boca: [0, h * .95, e * 2.2], topo: [0, h + w * .35, 0] }; return g;
}
