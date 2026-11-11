// pasta(pai, p, o): pasta de arquivo (âmbar: aba, fundo alto e frente mais baixa) em pé, face para +z, origem no centro da base.
// A folha entra entre o fundo e a frente: userData.dentro = ponto entre os dois, userData.boca = ponto acima da borda da frente.
// Para a folha ficar "dentro", ponha-a em userData.dentro e esconda o que passar da frente (ou deixe-a descer até a frente cobrir).
// o: w (1.0), h (.76). Uso (T16): const pa = pasta(CENA, [x, 0, z], { w: 1.2 }).
import { grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function pasta(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), w = o.w ?? 1.0, h = o.h ?? .76, mA = M(COR.ambar), mE = M(COR.ambarE), hf = h * .74;
  poe(rbox(w, h, .05, .03, 2), mE, g, [0, h / 2, -.1]);
  poe(rbox(w * .34, .09, .05, .03, 1), mE, g, [-w * .3, h + .03, -.1]);
  poe(rbox(.05, h * .5, .22, .02, 1), mE, g, [-w / 2 + .03, h * .25, -.0]); poe(rbox(.05, h * .5, .22, .02, 1), mE, g, [w / 2 - .03, h * .25, -.0]);
  poe(rbox(w, hf, .05, .03, 2), mA, g, [0, hf / 2, .06]);
  g.userData.dentro = [0, h * .55, -.03]; g.userData.boca = [0, hf + .04, .02]; g.userData.topo = [0, h + .1, 0];
  mancha(g, w + .6, .8, .26); return g;
}
