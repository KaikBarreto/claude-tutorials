// Caçamba estacionária (a de entulho/sucata que fica parada no cliente): corpo âmbar de lados inclinados, boca aberta, nervuras
// e dois patins. Comprimento em x (c), largura em z (l), altura h; base em y 0. NÃO é a caçamba do caminhão nem a de empilhadeira
// do kit. Uso: const k = cacambaEstacionaria(CENA, [x, 0, z], { c: 2.6, l: 1.5, h: 1.0 }); k.userData.boca = y da borda.
import { PI, THREE, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function cacambaEstacionaria(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 2.6, l = o.l ?? 1.5, h = o.h ?? 1.0, mt = M(o.cor ?? COR.ambar), mr = M(COR.ambarE), y0 = .14;
  const sh = new THREE.Shape([[-c / 2 + .3, 0], [c / 2 - .3, 0], [c / 2, h - y0], [-c / 2, h - y0]].map(v => new THREE.Vector2(...v)));
  const gl = new THREE.ExtrudeGeometry(sh, { depth: .05, bevelEnabled: true, bevelThickness: .012, bevelSize: .012, bevelSegments: 1, curveSegments: 1 });
  for (const s of [-1, 1]) { poe(gl, mt, g, [0, y0, s * (l / 2 - .05) - .025]);
    poe(rbox(c + .04, .06, .09, .02, 1), mr, g, [0, h, s * (l / 2 - .02)]);
    for (let i = 1; i < 4; i++) poe(rbox(.07, h - y0 - .1, .05, .015, 1), mr, g, [-c / 2 + .3 + i * (c - .6) / 4 + (i - 2) * .02, y0 + (h - y0) / 2, s * (l / 2 + .02)]); }
  const inc = Math.atan2(.3, h - y0);
  for (const s of [-1, 1]) { poe(rbox(.05, h - y0 + .04, l - .12, .015, 1), mt, g, [s * (c / 2 - .15), y0 + (h - y0) / 2, 0], [0, 0, -s * inc]);
    poe(rbox(.09, .06, l + .02, .02, 1), mr, g, [s * (c / 2 + .01), h, 0]); }
  poe(rbox(c - .5, .05, l - .5, .015, 1), mr, g, [0, y0 + .02, 0]);
  for (const z of [-l / 2 + .2, l / 2 - .2]) poe(rbox(c - .1, .11, .12, .03, 1), M(COR.cinzaE), g, [0, .055, z]);
  g.userData.boca = h; mancha(g, c + .9, l + .9, .3); return g;
}
