// Portão de entrada do pátio, sem marca: dois pilares, viga com a placa verde-escura e um trecho de cerca de cada lado.
// uso: portao(CENA, [x, 0, z], { placa: 'Recicla Vale' });   de lado: g.rotation.y = PI / 2
// A placa fica para +z; passa-se pelo vão ao longo de z. o: vao (5.2), h (4.4), cerca (comprimento de cada trecho, 3), hc (1.8),
// placa (texto em branco; '' = placa lisa: o nome da empresa só onde a cena o mostra). userData: placa, topo, vao.
import { mat, caixa, cil, malha, grupo, mancha, pintura, THREE } from '../motor.js';
export function portao(pai, pos = [0, 0, 0], o = {}) {
  const vao = o.vao ?? 5.2, h = o.h ?? 4.4, ce = o.cerca ?? 3, hc = o.hc ?? 1.8, g = grupo(pai, pos), con = mat('#E3E8EC', { alt: h, emi: .11 }), cz = mat('#AEB9C5', { alt: h, emi: .14 }), esc = mat('#56626F', { alt: h, emi: .24 });
  mancha(vao + 2 * ce + 2.5, 2.6, [0, 0, .1], { pai: g, op: .6 });
  for (const s of [-1, 1]) { const x = s * (vao / 2 + .3); malha(caixa(.6, h, .6, .07), con, [x, h / 2, 0], g); malha(caixa(.7, .14, .7, .04), cz, [x, .07, 0], g); malha(caixa(.68, .12, .68, .04), cz, [x, h + .02, 0], g);
    for (let i = 0; i <= Math.round(ce / .5); i++) malha(cil(.03, hc, 8), esc, [x + s * (.4 + i * .5), hc / 2, 0], g);
    for (const y of [.25, hc - .15]) malha(caixa(ce + .1, .06, .05, .02), esc, [x + s * (.35 + ce / 2), y, 0], g); }
  malha(caixa(vao + 1.5, .5, .5, .08), cz, [0, h - .45, 0], g);
  const pw = Math.min(vao * .72, 4), ph = .82;
  malha(caixa(pw, ph, .1, .04), mat('#1F5C40', { emi: .6, alt: h + 1, bri: .2 }), [0, h - .45, .28], g);
  if (o.placa) malha(new THREE.PlaneGeometry(pw * .92, ph * .8), pintura(920, Math.round(920 * ph * .8 / (pw * .92)), (x, W, H) => { x.fillStyle = '#1F5C40'; x.fillRect(0, 0, W, H); x.fillStyle = '#fff';
    x.font = `800 ${Math.round(H * .62)}px M, Montserrat, sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(o.placa, W / 2, H * .54, W * .94); }, { emi: .8 }), [0, h - .45, .333], g);
  g.userData = { vao, placa: [0, h - .45, .34], topo: [0, h + .6, 0] }; return g;
}
