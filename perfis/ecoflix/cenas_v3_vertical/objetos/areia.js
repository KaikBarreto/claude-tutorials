// Areia (ou terra, brita fina): monte liso de grão, para a carga de um caminhão caçamba ou um monte no chão. Material do
// kit v3 (serve nos dois climas). Base em y 0, pivô no centro da base.
// uso: const u = T.userData, d = u.dim; areia(u.bau, [d.cx, d.H - .2, 0], { c: d.C - .3, l: 2 * d.LZ - .2, h: .75, mancha: false });   // carga do caminhao.js (carga: 0)
//      areia(CENA, [x, 0, z], { c: 3.2, l: 2.6, h: 1.1 });                                                                     // monte no pátio
// o: c (comprimento em x), l (largura em z), h (altura), cor ('#E3C58F'), quadra (0 a 1: 0 = cone redondo, 1 = enche a caixa;
//    padrão .55), alt (altura do degradê, 3), mancha (false tira a sombra). userData: topo [x, y, z] local (prenda ali o chip), h.
import { THREE, PI, mat, malha, grupo, mancha } from '../motor.js';
export function areia(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 3.2, l = o.l ?? 2.6, h = o.h ?? 1.1, q = 1 - .5 * (o.quadra ?? .55), g = grupo(pai, pos);
  const geo = new THREE.SphereGeometry(1, 40, 14, 0, 2 * PI, 0, PI / 2), P = geo.attributes.position;
  for (let i = 0; i < P.count; i++) {   // meia esfera → monte: a planta fica mais quadrada e a crista ganha ondas leves (sem ruído: função do ponto)
    const x = P.getX(i), y = P.getY(i), z = P.getZ(i), sx = Math.sign(x) * Math.pow(Math.abs(x), q), sz = Math.sign(z) * Math.pow(Math.abs(z), q);
    const onda = 1 + .07 * Math.sin(x * 5.3 + 1.1) * Math.cos(z * 4.1) + .05 * Math.sin(x * 9.7 - z * 6.3);
    P.setXYZ(i, sx * c / 2, Math.pow(y, .8) * h * onda, sz * l / 2);
  }
  geo.computeVertexNormals();
  malha(geo, mat(o.cor ?? '#E3C58F', { alt: o.alt ?? 3, emi: .34, bri: .1 }), [0, 0, 0], g);
  if (o.mancha !== false) mancha(c * 1.5, l * 1.5, [0, 0, .1], { pai: g, op: .7 });
  g.userData = { topo: [0, h + .25, 0], h }; return g;
}
