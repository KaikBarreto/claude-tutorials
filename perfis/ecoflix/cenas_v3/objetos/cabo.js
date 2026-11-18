// Cabo (USB, rede, serial): tubo por uma curva suave que passa pelos pontos, com um conector em cada ponta.
// uso: const c = cabo(CENA, [[0, .05, 0], [1, .02, .4], [2, .05, .5]], { r: .02 }); caboAte(c, eio(pr(t, a, .6)));   // estica da origem ao destino
// o: r (.012), cor (grafite), seg (64), conector (false tira). userData.curva.getPoint(u) dá o ponto para o que "viaja" pelo cabo:
// sinal(c, u) leva uma conta de luz verde até a fração u (u < 0 ou > 1 esconde).
import { mat, tubo, caixa, esfera, malha, grupo } from '../motor.js';
export function cabo(pai, pts, o = {}) {
  const r = o.r ?? .012, g = grupo(pai), geo = tubo(pts, r, o.seg ?? 64), m = malha(geo, mat(o.cor ?? '#39424A', { bri: .15, emi: .55 }), [0, 0, 0], g), n = geo.index.count;
  const pontas = o.conector === false ? [] : [0, 1].map(i => malha(caixa(r * 5, r * 3.2, r * 3.6, r * .7), mat('#8F9BAA', { emi: .5 }), pts[i ? pts.length - 1 : 0], g));
  const luz = malha(esfera(r * 2.2, [1, 1, 1], 12), mat('#6CF0A8', { emi: 1.65, emiC: .25 }), [0, 0, 0], g); luz.visible = false;
  g.userData = { curva: geo.userData.curva, tubo: m, n, pontas, luz }; return g;
}
export function caboAte(g, p) { const u = g.userData; p = Math.min(1, Math.max(0, p)); u.tubo.geometry.setDrawRange(0, Math.floor(u.n * p / 48) * 48); u.tubo.visible = p > .001; if (u.pontas[0]) { u.pontas[0].visible = p > .001; u.pontas[1].visible = p > .995; } }
export function sinal(g, p) { const u = g.userData; u.luz.visible = p > 0 && p < 1; if (u.luz.visible) u.luz.position.copy(u.curva.getPoint(p)); }
