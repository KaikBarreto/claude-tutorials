// Saco de ráfia: fechado e amarrado (a tara, o material ensacado) ou aberto, com a carga na boca (o bruto).
// uso: saco(CENA, [x, 0, z]);   saco(CENA, [x, 0, z], { aberto: true, carga: 'latinha' });   sacoAberto(pai, pos, o) = o mesmo
// o: s (escala; 1 = 95 cm de altura), cor, carga (tipo de monte.js: latinha, pet, cobre...), n (peças na boca).
// userData: boca (y da boca, local), topo, lotes (a carga, para cai()).
import { PI, mat, torno, toro, malha, grupo, mancha } from '../motor.js';
import { pecas, pontosMonte } from './monte.js';
export function saco(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), s = o.s ?? 1, c = grupo(g), rafia = mat(o.cor ?? '#EBDDB9', { alt: 1.1 * s, bri: .16, emi: .14, ds: !!o.aberto }), fio = mat('#C6AB78', { alt: 1.1 * s, emi: .14 });
  c.scale.set(s, s, s * .84); mancha(1.5 * s, 1.3 * s, [0, 0, .05], { pai: g, op: .7 });
  if (o.aberto) {
    malha(torno([[0, 0], [.24, .004], [.34, .05], [.385, .17], [.395, .34], [.38, .5], [.35, .62], [.33, .7], [.345, .75], [.365, .775]], 34), rafia, [0, 0, 0], c);
    malha(toro(.358, .026, 40), fio, [0, .765, 0], c, [PI / 2, 0, 0]); for (const y of [.22, .4]) malha(toro(.392, .008, 44), fio, [0, y, 0], c, [PI / 2, 0, 0]);
    g.userData = { boca: .76 * s, topo: [0, 1.25 * s, 0] };
    if (o.carga) g.userData.lotes = pecas(c, o.carga, pontosMonte(o.n ?? 16, .27, .27, .2, .68), { s: o.sp ?? .62 });
  } else {
    malha(torno([[0, 0], [.2, .004], [.29, .05], [.325, .17], [.335, .34], [.315, .5], [.26, .62], [.17, .71], [.085, .77], [.072, .81], [.1, .87], [.115, .92], [.07, .95], [0, .955]], 30), rafia, [0, 0, 0], c);
    malha(toro(.083, .024, 20), fio, [0, .79, 0], c, [PI / 2, 0, 0]); for (const [y, r] of [[.25, .331], [.42, .33]]) malha(toro(r, .008, 40), fio, [0, y, 0], c, [PI / 2, 0, 0]);
    g.userData = { boca: .95 * s, topo: [0, 1.35 * s, 0] };
  }
  return g;
}
export const sacoAberto = (pai, pos, o = {}) => saco(pai, pos, { ...o, aberto: true });
