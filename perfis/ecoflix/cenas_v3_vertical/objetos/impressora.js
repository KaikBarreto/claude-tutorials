// Impressora térmica de cupom (corpo escuro, tampa, fenda e o botão verde), com o cupom (cupom.js) que sai da fenda.
// uso: const imp = impressora(CENA, [x, y, z], { s: 1 }); imprime(imp, eo(pr(t, a, .9)));   // 0 a 1
// o: s (escala; 1 = 34 cm de largura. Para aparecer ao lado de gente e caminhão, s = 2 ou 3), cupom ({ tipo, h } do cupom.js).
// Frente para +z. userData: fenda (ponto local), cupom (grupo), topo, entrada (onde chega o cabo).
import { mat, caixa, cil, malha, grupo, mancha } from '../motor.js';
import { cupom } from './cupom.js';
export function impressora(pai, pos = [0, 0, 0], o = {}) {
  const s = o.s ?? 1, G = grupo(pai, pos), g = grupo(G), esc = mat('#39424A', { alt: .3 * s, bri: .2, emi: .36 }), esc2 = mat('#4B5661', { alt: .3 * s, bri: .22, emi: .36 }); g.scale.setScalar(s);
  mancha(.75 * s, .75 * s, [0, 0, .03 * s], { pai: G, op: .7 });
  malha(caixa(.34, .13, .4, .05), esc, [0, .065, 0], g); malha(caixa(.32, .08, .25, .04), esc2, [0, .155, -.06], g);
  malha(caixa(.26, .012, .016, .004), mat('#17191A', { bri: .02 }), [0, .196, .066], g); malha(cil(.02, .014, 14), mat('#50D088', { emi: 1.21, emiC: .2 }), [.12, .134, .15], g);
  const c = cupom(g, [0, .196, .068], { w: .22, h: .34, ...(o.cupom ?? {}) });
  G.userData = { fenda: [0, .196 * s, .068 * s], cupom: c, topo: [0, .7 * s, 0], entrada: [0, .05 * s, -.2 * s] }; imprime(G, 0); return G;
}
export function imprime(g, p) { g.userData.cupom.userData.sai(p); }
