// Computador de mesa: monitor de tela escura LISA (nada do app nela: a tela é a porta dos dados, o que aparece é um plano
// HTML preso em userData.tela, ou a câmera mergulha nela), teclado e mouse. Frente para +z, base em y 0.
// uso: const pc = computador(CENA, [x, y, z], { s: 2 }); const T = pc.userData.tela;   // { centro [x, y, z] local, w, h, incl }
//      plano(html, { pos: mundo(pc, T.centro), rot: [T.incl, 0, 0], esc: T.w / larguraPx });
// o: s (escala; 1 = monitor de 66 cm; ao lado de gente, 1.6 a 2.5), mesa (true põe o tampo). userData: tela, topo, usb (onde sai o cabo).
import { mat, caixa, esfera, malha, grupo, mancha, lote, poeInst } from '../motor.js';
export function computador(pai, pos = [0, 0, 0], o = {}) {
  const s = o.s ?? 1, G = grupo(pai, pos), g = grupo(G), A = { alt: .8 * s, bri: .2 }, esc = mat('#39424A', { ...A, emi: .36 }), cz = mat('#E6EBF0', { ...A, emi: .14 }); g.scale.setScalar(s);
  let y0 = 0; if (o.mesa) { y0 = .74; malha(caixa(1.5, .05, .75, .02), mat('#D8B58C', { alt: 1, emi: .14 }), [0, .715, .08], g); for (const x of [-.68, .68]) malha(caixa(.06, .7, .66, .02), mat('#AEB9C5', { alt: 1, emi: .14 }), [x, .35, .08], g); mancha(2.4 * s, 1.6 * s, [0, 0, .1 * s], { pai: G, op: .7 }); }
  else mancha(1.3 * s, 1.0 * s, [0, 0, .08 * s], { pai: G, op: .7 });
  malha(caixa(.28, .022, .18, .01), esc, [0, y0 + .011, -.06], g); malha(caixa(.06, .24, .04, .015), esc, [0, y0 + .13, -.1], g);
  const mon = grupo(g, [0, y0 + .41, -.07]); mon.rotation.x = -.08; malha(caixa(.68, .44, .04, .022), esc, [0, 0, 0], mon);
  const tela = malha(caixa(.63, .385, .012, .008), mat('#131514', { bri: .14, emi: .7, novo: true }), [0, .008, .017], mon), luz = malha(caixa(.05, .008, .012, .003), mat('#50D088', { emi: 1.32, emiC: .2 }), [0, -.2, .021], mon);
  malha(caixa(.5, .024, .17, .01), cz, [0, y0 + .012, .22], g);
  const tk = lote(caixa(.028, .008, .026, .004), mat('#C3CCD5', { emi: .24 }), 56, g); for (let r = 0; r < 4; r++) for (let c = 0; c < 14; c++) poeInst(tk, r * 14 + c, [-.221 + c * .034, y0 + .027, .163 + r * .038]);
  malha(esfera(.036, [1, .55, 1.45], 14), cz, [.36, y0 + .02, .23], g);
  G.userData = { tela: { centro: [0, (y0 + .418) * s, (-.07 + .026) * s], w: .63 * s, h: .385 * s, incl: -.08, malha: tela }, topo: [0, (y0 + .85) * s, 0], usb: [.2 * s, (y0 + .05) * s, -.14 * s] }; return G;
}
