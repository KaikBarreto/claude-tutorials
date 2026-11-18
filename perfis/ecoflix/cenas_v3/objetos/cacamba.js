// Caçamba pequena de pátio (a de empilhadeira): corpo em trapézio, boca aberta e dois patins. A carga vai por cima.
// uso: const k = cacamba(CENA, [x, 0, z], { cor: '#7F8B98' });  pecas(k, 'ferro', pontos, { s: .5 })  ·  userData: boca (y), dentro, topo
// Não é a caçamba do caminhão (caminhao.js) nem a estacionária de rua (cacambaEstacionaria.js).
import { mat, caixa, perfil, malha, grupo, mancha } from '../motor.js';
export function cacamba(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), s = o.s ?? 1, c = grupo(g), m = mat(o.cor ?? '#7F8B98', { alt: 1, emi: .5 }), e = mat('#59646F', { alt: 1, emi: .5 }); c.scale.setScalar(s);
  mancha(2.2 * s, 1.7 * s, [0, 0, .05], { pai: g, op: .7 });
  for (const z of [-.5, .5]) malha(perfil([[-.62, .1], [.62, .1], [.8, .78], [-.8, .78]], .03, .05, .012), m, [0, 0, z], c);
  const inc = Math.atan2(.18, .68); for (const sx of [-1, 1]) malha(caixa(.05, .72, 1.02, .016), m, [sx * .71, .44, 0], c, [0, 0, -sx * inc]);
  malha(caixa(1.26, .05, 1.0, .016), e, [0, .12, 0], c); malha(caixa(1.66, .05, 1.1, .02), e, [0, .78, 0], c);
  malha(caixa(1.52, .06, .94, .02), mat("#3B444E", { bri: .05 }), [0, .786, 0], c);   // o vão escuro da boca (some debaixo da carga)
  for (const x of [-.38, .38]) malha(caixa(.16, .1, 1.1, .03), e, [x, .05, 0], c);
  g.userData = { boca: .8 * s, dentro: [0, .8 * s, 0], topo: [0, 1.5 * s, 0] }; return g;
}
