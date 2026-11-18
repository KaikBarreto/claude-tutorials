// Big bag de ráfia clara, sem marca. o.estado: 'cheio' (alças nos quatro cantos, boca amarrada), 'aberto' (a boca aberta:
// a carga vai acima de userData.h) ou 'vazio' (dobrado no chão). o: w (.95), h (1.05), carga (tipo de monte.js, no aberto).
// uso: bigBag(CENA, [x, 0, z], { estado: 'aberto', carga: 'pet' });  userData: h, topo, lotes
import { PI, mat, caixa, cil, toro, malha, grupo, mancha } from '../motor.js';
import { pecas, pontosMonte } from './monte.js';
export function bigBag(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), w = o.w ?? .95, h = o.h ?? 1.05, r = mat('#E9DDC2', { alt: 1.2, bri: .16, emi: .14 }), c = mat('#C2B18C', { alt: 1.2, emi: .14 }), a = mat('#D2C19C', { alt: 1.4, emi: .14 });
  if (o.estado === 'vazio') {
    malha(caixa(w * 1.1, .09, w * .8, .04), r, [0, .045, 0], g); malha(caixa(w * 1.04, .014, .03, .006), c, [0, .092, -.05], g);
    for (const [x, z, k] of [[-.3, -.2, .5], [.3, -.2, -.4], [-.28, .22, 2.7], [.3, .2, -2.9]]) malha(toro(.09, .02, 14, PI), a, [x * w / .78, .1, z * w / .78], g, [-PI / 2, 0, k]);
    if (o.mancha !== false) mancha(w * 2.0, w * 1.7, [0, 0, .04], { pai: g, op: .6 }); g.userData = { h: .09, topo: [0, .6, 0] }; return g;
  }
  const corpo = caixa(w, h, w, .15), P = corpo.attributes.position;
  for (let i = 0; i < P.count; i++) { const y = P.getY(i) / h * 2, b = 1 + .08 * (1 - y * y); P.setX(i, P.getX(i) * b); P.setZ(i, P.getZ(i) * b); } corpo.computeVertexNormals();
  malha(corpo, r, [0, h / 2, 0], g);
  for (const y of [.26 * h, .6 * h]) malha(caixa(w * 1.085, .012, w * 1.085, .005), c, [0, y, 0], g);   // costuras
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) malha(toro(.1, .022, 16, PI), a, [sx * (w / 2 - .08), h - .015, sz * (w / 2 - .08)], g, [0, sx * sz > 0 ? -PI / 4 : PI / 4, 0]);
  g.userData = { h, topo: [0, h + .7, 0] };
  if (o.estado === 'aberto') { malha(toro(w * .44, .024, 40), c, [0, h - .005, 0], g, [PI / 2, 0, 0]); malha(cil(w * .43, .02, 32), mat('#B7AA8C', { bri: .05, emi: .11 }), [0, h - .012, 0], g);
    if (o.carga) g.userData.lotes = pecas(g, o.carga, pontosMonte(o.n ?? 26, w * .36, w * .36, .26, h + .02), { s: o.sp ?? .7 }); }
  else { malha(cil(.14, .16, 18, .11), r, [0, h + .07, 0], g); malha(toro(.112, .018, 20), c, [0, h + .11, 0], g, [PI / 2, 0, 0]); }
  if (o.mancha !== false) mancha(w * 2.1, w * 2.0, [0, 0, .06], { pai: g, op: .75 }); return g;
}
