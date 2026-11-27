// Estrada: faixa de asfalto cinza com o acostamento claro e a linha central tracejada, ao longo de x; topo em y .03.
// uso: estrada(CENA, [cx, 0, z], { c: 40, l: 7 });   a divisa de estado é o porticoEstado.js em cima dela
import { mat, caixa, malha, grupo, lote, poeInst } from '../motor.js';
export function estrada(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 40, l = o.l ?? 7, g = grupo(pai, pos);
  malha(caixa(c, .03, l + 1.2, .012), mat('#E3E8EC', { alt: .2, emi: .08 }), [0, .005, 0], g).renderOrder = -3;
  malha(caixa(c, .03, l, .012), mat('#8E99A6', { alt: .2, emi: .13, bri: .05 }), [0, .016, 0], g).renderOrder = -2;
  for (const s of [-1, 1]) malha(caixa(c, .012, .12, .004), mat('#F4F6F8', { emi: .36 }), [0, .028, s * (l / 2 - .3)], g);
  const n = Math.floor(c / 3.2), tr = lote(caixa(1.7, .012, .14, .004), mat('#F4F6F8', { emi: .5 }), n, g); for (let i = 0; i < n; i++) poeInst(tr, i, [-c / 2 + 1.6 + i * 3.2, .028, 0]);
  g.userData = { c, l, y: .031 }; return g;
}
