// Baterias automotivas (caixa escura, tampa, faixa âmbar, polo vermelho e polo cinza), arrumadas em camadas.
// uso: baterias(CENA, [x, 0, z], { nx: 4, nz: 3, camadas: 2 });   ou   baterias(pai, pos, { P: [[x, y, z, giro], ...] })
// Sobre um palete: baterias(pal, [0, pal.userData.sup, 0], { nx: 3, nz: 3 }). Para um monte solto: monte(..., { tipo: 'bateria' }).
// userData: lotes (para cai() de monte.js), topo.
import { rng, ri, grupo, mancha } from '../motor.js';
import { bateriasLote } from './monte.js';
export function baterias(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), nx = o.nx ?? 3, nz = o.nz ?? 2, cam = o.camadas ?? 2, s = o.s ?? 1, P = o.P ? o.P.map(p => [...p]) : [];
  if (!o.P) for (let k = 0; k < cam; k++) for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) if (k === 0 || rng() < (o.cheio ?? .82))
    P.push([(i - (nx - 1) / 2) * .4 * s, k * .245 * s, (j - (nz - 1) / 2) * .27 * s, ri(-.05, .05)]);
  if (o.mancha) mancha(nx * .4 * s + .9, nz * .27 * s + .8, [0, 0, .05], { pai: g, op: .7 });
  g.userData = { lotes: bateriasLote(g, P, s), topo: [0, cam * .245 * s + .5, 0] }; return g;
}
