// Prensa vertical de fardos: câmara âmbar com porta, duas colunas, travessa, cilindro e a placa que desce.
// uso: const p = prensa(CENA, [x, 0, z]); aperta(p, eio(pr(t, a, 1.2)));   // 0 = aberta, 1 = prensando
// Frente (a porta) para +z. 3,1 m de altura. userData: placa, haste, boca (ponto da boca de carga), saida (onde o fardo sai), topo.
import { cl, lerp, mat, caixa, cil, malha, grupo, mancha, PI } from '../motor.js';
export function prensa(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), A = { alt: 3.2, emi: .28, bri: .22 }, amb = mat(o.cor ?? '#F2B63D', A), ambE = mat('#D99A2B', A), esc = mat('#39424A', { alt: 3.2, bri: .12, emi: .24 }), aco = mat('#C3CCD5', { alt: 3.2, emi: .14 });
  mancha(3.6, 3.2, [0, 0, .1], { pai: g, op: .8 });
  malha(caixa(1.6, .12, 1.4, .04), esc, [0, .06, 0], g); malha(caixa(1.44, 1.45, 1.24, .07), amb, [0, .845, 0], g);
  malha(caixa(1.06, 1.0, .06, .03), ambE, [0, .7, .625], g); malha(caixa(.07, .44, .09, .025), esc, [.41, .72, .67], g);
  malha(caixa(.92, .2, .04, .02), mat('#22282E', { bri: .05 }), [0, 1.38, .615], g);
  for (const x of [-.62, .62]) malha(caixa(.17, 1.3, .17, .04), esc, [x, 2.2, 0], g);
  malha(caixa(1.56, .26, .54, .06), amb, [0, 2.95, 0], g); malha(cil(.14, .52, 20), aco, [0, 2.57, 0], g);
  const haste = malha(cil(.06, 1, 14), mat('#E6EBF0', { emi: .24, bri: .4 }), [0, 0, 0], g), placa = malha(caixa(1.06, .11, .98, .035), aco, [0, 0, 0], g);
  malha(caixa(.11, .42, .32, .03), esc, [.775, 1.15, .25], g);
  malha(cil(.05, .04, 16), mat('#50D088', { emi: .88 }), [.84, 1.23, .25], g, [0, 0, PI / 2]); malha(cil(.05, .04, 16), mat('#E5574A', { emi: .7 }), [.84, 1.08, .25], g, [0, 0, PI / 2]);
  g.userData = { haste, placa, boca: [0, 1.38, .7], saida: [0, 0, 1.6], topo: [0, 3.6, 0] }; aperta(g, 0); return g;
}
export function aperta(g, p) { const y = lerp(2.22, 1.64, cl(p)), u = g.userData; u.placa.position.set(0, y, 0); u.haste.position.set(0, (2.32 + y) / 2, 0); u.haste.scale.set(1, 2.32 - y, 1); }
