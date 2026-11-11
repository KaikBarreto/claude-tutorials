// Galpão genérico (paredes claras, telhado de duas águas, porta de enrolar e uma placa âmbar), sem nome nem marca. Frente para +z,
// base em y 0, centro em x/z. Uso: galpao(CENA, [x, 0, z], { c: 4, l: 3, h: 1.5 }); o nome da empresa é um chip HTML (ancora).
// o.porta (padrão true), o.cor das paredes. userData.topo = [0, altura do cume, 0].
import { PI, THREE, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function galpao(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 4, l = o.l ?? 3, h = o.h ?? 1.5, cu = o.cume ?? .9;
  poe(rbox(c, h, l, .05, 2), M(o.cor ?? '#E3E7EC'), g, [0, h / 2, 0]);
  const sh = new THREE.Shape([[-c / 2 - .15, 0], [c / 2 + .15, 0], [0, cu]].map(v => new THREE.Vector2(...v)));
  const rg = new THREE.ExtrudeGeometry(sh, { depth: l + .3, bevelEnabled: false }); rg.translate(0, 0, -(l + .3) / 2);
  poe(rg, M('#5E6B78'), g, [0, h, 0]);
  if (o.porta !== false) {
    const pw = c * .5, ph = h * .78;
    poe(rbox(pw, ph, .06, .02, 1), M('#9AA3AD'), g, [-c * .1, ph / 2, l / 2 + .02]);
    for (let i = 1; i < 6; i++) poe(rbox(pw - .06, .03, .02, .008, 1), M('#7E8994'), g, [-c * .1, i * ph / 6, l / 2 + .06]);
    poe(rbox(c * .17, h * .34, .05, .02, 1), M('#C9D5DE'), g, [c * .33, h * .55, l / 2 + .02]);
    poe(rbox(c * .2, h * .17, .05, .02, 1), M(COR.ambar), g, [c * .33, h * .86, l / 2 + .03]);
  }
  g.userData.topo = [0, h + cu, 0]; mancha(g, c + 1.2, l + 1.2, .26); return g;
}
