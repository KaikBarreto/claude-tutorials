// Pino de local (gota de ponta para baixo, verde, com o miolo branco): marca origem e destino num mapa ou numa rota.
// A ponta fica em pos. Altura total = 1 * s. uso: const pn = pinoLocal(CENA, [x, 0, z], { s: 2 }); pn.position.y = .1 + .1 * Math.sin(t * 2);
// o: s, cor ('#50D088'; destino em âmbar: '#F2B63D'). userData: topo.
import { PI, mat, torno, cil, malha, grupo, mancha } from '../motor.js';
export function pinoLocal(pai, pos = [0, 0, 0], o = {}) {
  const s = o.s ?? 1, G = grupo(pai, pos), g = grupo(G), pts = [[0, 0]]; g.scale.setScalar(s);
  for (let i = 0; i <= 18; i++) { const a = -PI / 2 + .62 + (PI - .62 + PI / 2 - .0) * i / 18 * .78; pts.push([.3 * Math.cos(a), .68 + .3 * Math.sin(a)]); } pts.push([0, .98]);
  const m = malha(torno(pts, 32), mat(o.cor ?? '#50D088', { emi: .65, bri: .3, alt: 1.2 * s }), [0, 0, 0], g); m.scale.z = .5;
  for (const z of [-1, 1]) malha(cil(.13, .02, 24), mat('#FFFFFF', { emi: .88, emiC: .1 }), [0, .7, z * .145], g, [PI / 2, 0, 0]);
  if (o.mancha !== false) mancha(.9 * s, .7 * s, [0, 0, 0], { pai: G, op: .6 });
  G.userData = { topo: [0, 1.25 * s, 0] }; return G;
}
