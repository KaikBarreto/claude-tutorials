// Palete de madeira (1,2 x 1,0 m). userData.sup = altura do tampo: ponha a carga em [x, sup, z] dentro dele.
// uso: const p = palete(CENA, [x, 0, z]); fardo(p, [0, p.userData.sup, 0], { mancha: false });
import { mat, caixa, malha, grupo, mancha } from '../motor.js';
export function palete(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), m = mat('#D8B58C', { alt: .5, emi: .14 }), e = mat('#BC9468', { alt: .5, emi: .14 });
  if (o.mancha !== false) mancha(2.1, 1.9, [0, 0, .05], { pai: g, op: .65 });
  for (const z of [-.42, 0, .42]) { malha(caixa(1.2, .022, .13, .01), m, [0, .011, z], g); for (const x of [-.52, 0, .52]) malha(caixa(.14, .08, .13, .015), e, [x, .062, z], g); }
  for (const x of [-.52, 0, .52]) malha(caixa(.14, .022, 1.0, .01), e, [x, .112, 0], g);
  for (let i = 0; i < 6; i++) malha(caixa(1.2, .024, .135, .01), m, [0, .135, -.4325 + i * .173], g);
  g.userData = { sup: .147, topo: [0, .7, 0] }; return g;
}
