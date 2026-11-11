// guiche(pai, p, o): guichê do caixa do pátio: casinha clara com a janela de atendimento na frente, o balcão saindo para fora
// (onde vai a registradora.js) e a laje verde por cima. Frente para +z, base em y 0, centro em x/z. Sem nome nem marca.
// o: c (largura em x, 2.6), l (fundo em z, 1.9), h (altura das paredes, 2.4), cor (paredes), laje (cor da laje, verde da marca).
// userData.balcao = ponto (local) no meio do tampo do balcão, do lado de fora; userData.topo = ponto acima da laje.
// Uso (T00): const gu = guiche(CENA, [x, 0, z]); const reg = registradora(gu, [-.35, gu.userData.balcao[1], gu.userData.balcao[2]]).
import { grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function guiche(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 2.6, l = o.l ?? 1.9, h = o.h ?? 2.4, e = .14, mP = M(o.cor ?? '#E3E7EC'), mE = M('#C9D1DA');
  const jx = c / 2 - .42, y0 = 1.0, y1 = 2.0;                                                       // janela: x em ±jx, y de y0 a y1
  poe(rbox(c, h, e, .04, 2), mP, g, [0, h / 2, -l / 2 + e / 2]);                                      // fundo
  for (const s of [-1, 1]) poe(rbox(e, h, l, .04, 2), mP, g, [s * (c / 2 - e / 2), h / 2, 0]);          // laterais
  const zf = l / 2 - e / 2;
  poe(rbox(c, y0, e, .04, 2), mP, g, [0, y0 / 2, zf]);                                                // frente embaixo da janela
  poe(rbox(c, h - y1, e, .04, 2), mP, g, [0, (h + y1) / 2, zf]);                                      // em cima
  for (const s of [-1, 1]) poe(rbox(c / 2 - jx, y1 - y0, e, .03, 1), mP, g, [s * (jx + (c / 2 - jx) / 2), (y0 + y1) / 2, zf]);
  poe(rbox(c - 2 * e, .04, l - 2 * e, .01, 1), M('#B9C1CA'), g, [0, .02, 0]);                           // piso de dentro
  poe(rbox(c - .5, .9, .5, .03, 1), mE, g, [0, .45, -l / 2 + .4]);                                     // mesa do fundo
  poe(rbox(2 * jx + .3, .06, .62, .02, 1), M('#7E8994'), g, [0, y0 + .03, zf + .14]);                  // balcão (tampo)
  poe(rbox(2 * jx + .3, .05, .08, .02, 1), M('#7E8994'), g, [0, y1 + .02, zf + .05]);                  // pingadeira da janela
  poe(rbox(c + .5, .14, l + .6, .05, 2), M(o.laje ?? COR.verde), g, [0, h + .07, .1]);                  // laje
  mancha(g, c + 1.2, l + 1.3, .28);
  g.userData.balcao = [0, y0 + .06, zf + .2]; g.userData.topo = [0, h + .2, 0]; return g;
}
