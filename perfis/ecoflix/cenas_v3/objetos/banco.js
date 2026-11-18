// Banco genérico, sem nome nem marca: escada, quatro colunas, viga e frontão com o disco verde, e a parede do fundo com a porta.
// uso: banco(CENA, [x, 0, z], { s: 1 });   s = 1 → 7 m de frente e 7,2 m de altura (como ícone de estação: s = .4)
// Frente para +z. userData: topo (acima do frontão), porta (ponto no chão, à frente da escada).
import { PI, mat, caixa, perfil, cil, malha, grupo, mancha } from '../motor.js';
export function banco(pai, pos = [0, 0, 0], o = {}) {
  const s = o.s ?? 1, G = grupo(pai, pos), g = grupo(G), A = { alt: 7.5 * s, emi: .12 }, ped = mat('#EEF2F5', A), pedE = mat('#CBD3DC', A), vd = mat('#50D088', { emi: .65, alt: 9 * s, bri: .25 });
  g.scale.setScalar(s); mancha(11 * s, 9 * s, [0, 0, .3 * s], { pai: G, op: .75 });
  for (let i = 0; i < 3; i++) malha(caixa(7.4 - i * .5, .22, 5.6 - i * .5, .05), i ? ped : pedE, [0, .11 + i * .22, 0], g);
  malha(caixa(6.2, 4.0, 3.2, .08), ped, [0, 2.66, -.7], g);
  malha(caixa(1.3, 2.5, .12, .05), mat('#39424A', { bri: .1, emi: .28 }), [0, 1.91, .92], g); malha(caixa(1.1, .1, .14, .03), vd, [0, 3.22, .93], g);
  for (const x of [-2.55, -.95, .95, 2.55]) { malha(cil(.3, 3.7, 22, .27), ped, [x, 2.51, 1.9], g); malha(caixa(.78, .18, .78, .05), pedE, [x, .75, 1.9], g); malha(caixa(.74, .16, .74, .05), pedE, [x, 4.44, 1.9], g); }
  malha(caixa(6.9, .5, 4.9, .08), ped, [0, 4.77, .1], g);
  malha(perfil([[-3.6, 5.02], [3.6, 5.02], [0, 6.9]], [.08, .08, .14], 4.9, .08), ped, [0, 0, .1], g);
  malha(cil(.5, .1, 30), vd, [0, 5.7, 2.56], g, [PI / 2, 0, 0]);
  G.userData = { topo: [0, 7.6 * s, 0], porta: [0, 0, 4 * s] }; return G;
}
