// Tambor de aço de 200 litros (azul, com os dois frisos e a tampa com o bujão). o.aberto = sem tampa (a carga vai por cima).
// uso: tambor(CENA, [x, 0, z], { cor: '#4F86B0' });  userData: boca (y), topo.
import { PI, mat, cil, toro, malha, grupo, mancha } from '../motor.js';
export function tambor(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), m = mat(o.cor ?? '#4F86B0', { alt: 1, bri: .3, emi: .55 }), e = mat(o.corE ?? '#3C6A8E', { alt: 1, bri: .25, emi: .55 });
  mancha(1.4, 1.3, [0, 0, .05], { pai: g, op: .7 });
  malha(cil(.29, .88, 36), m, [0, .44, 0], g);
  for (const y of [.3, .58]) malha(toro(.292, .018, 40), e, [0, y, 0], g, [PI / 2, 0, 0]); for (const y of [.014, .866]) malha(toro(.283, .022, 40), e, [0, y, 0], g, [PI / 2, 0, 0]);
  if (o.aberto) malha(cil(.262, .02, 32), mat('#22303B', { bri: .05 }), [0, .872, 0], g);
  else { malha(cil(.262, .02, 32), e, [0, .874, 0], g); malha(cil(.045, .035, 16), mat('#DCE3EA', { emi: .6 }), [.14, .895, .06], g); malha(cil(.022, .03, 12), mat('#DCE3EA', { emi: .6 }), [-.15, .892, -.08], g); }
  g.userData = { boca: .88, topo: [0, 1.4, 0] }; return g;
}
