// Cadeira simples de escritório (assento e encosto verdes, pés claros), de frente para +x, base em y 0. É a "vaga": a
// pessoaSenta.js senta nela com o quadril em x -0,12 do centro. Para sumir com a cadeira: g.scale.setScalar(k).
// uso: const c = cadeira(CENA, [x, 0, z], { cor: '#50D088' }); c.rotation.y = -PI / 2;   // de frente para a câmera (+z)
// o: s (escala), cor (assento e encosto), pe (cor dos pés), mancha. userData: assento (altura do tampo), topo.
import { mat, caixa, cil, malha, grupo, mancha } from '../motor.js';
export function cadeira(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), s = o.s ?? 1, c = grupo(g), A = { alt: 1.2 * s, bri: .2, emi: .26 }, cor = mat(o.cor ?? '#50D088', A), pe = mat(o.pe ?? '#D5DDE3', { ...A, emi: .16 });
  c.scale.setScalar(s); if (o.mancha !== false) mancha(1.5 * s, 1.3 * s, [0, 0, .03], { pai: g, op: .7 });
  for (const [x, z] of [[.2, .2], [.2, -.2], [-.2, .2], [-.2, -.2]]) malha(cil(.022, .37, 12, .026), pe, [x, .185, z], c);
  malha(caixa(.52, .07, .52, .03), cor, [0, .385, 0], c);
  for (const z of [.2, -.2]) malha(cil(.02, .5, 12), pe, [-.235, .66, z], c);
  malha(caixa(.06, .36, .5, .028), cor, [-.24, .83, 0], c);
  g.userData = { assento: .42 * s, topo: [0, 1.25 * s, 0] }; return g;
}
