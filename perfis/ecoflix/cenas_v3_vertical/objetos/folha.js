// Folha de documento genérica em 3D (papel claro, faixa colorida no alto, linhas cinza e um quadro), sem texto: o rótulo
// ("NF-e", "MTR", "Manifesto") é um chip preso em userData.topo. Pivô no centro, face para +z. É a folha FÍSICA (clima claro,
// na mão do motorista, na pasta); o documento do sistema, com campos, é dados/documento.js.
// uso: const f = folha(CENA, [x, y, z], { cor: '#50D088', w: .5, h: .66, linhas: 4 }); f.rotation.y = -.3;
import { mat, malha, caixa, grupo, pintura, THREE } from '../motor.js';
export function folha(pai, pos = [0, 0, 0], o = {}) {
  const w = o.w ?? .5, h = o.h ?? w * 1.32, n = o.linhas ?? 4, cor = o.cor ?? '#50D088', g = grupo(pai, pos), W = 400, H = Math.round(W * h / w);
  const m = pintura(W, H, x => { x.fillStyle = '#FBFBF7'; x.fillRect(0, 0, W, H); const bar = (a, b, c, d, f) => { x.fillStyle = f; x.beginPath(); x.roundRect(a, b, c, d, Math.min(d / 2, 9)); x.fill(); };
    bar(0, 0, W, H * .13, cor); bar(34, H * .2, W * .44, 20, '#667085'); bar(34, H * .2 + 36, W * .3, 13, '#B4BCC8');
    const y0 = H * .37, e = Math.min(40, (H * .42) / n); for (let i = 0; i < n; i++) { bar(34, y0 + i * e, W * (.42 + (i % 2) * .12), 13, '#C8CED8'); bar(W - 34 - W * .18, y0 + i * e, W * .18, 13, '#98A2B3'); }
    x.strokeStyle = '#D0D5DD'; x.lineWidth = 4; x.beginPath(); x.roundRect(34, H * .82, W * .34, H * .1, 10); x.stroke(); bar(W - 34 - W * .3, H * .845, W * .3, 22, cor); }, { emi: .5 });
  malha(caixa(w, h, w * .012, w * .005), mat('#FBFBF7', { emi: .36, bri: .1 }), [0, 0, 0], g); malha(new THREE.PlaneGeometry(w * .985, h * .985), m, [0, 0, w * .0068], g);
  g.userData = { w, h, topo: [0, h / 2 + w * .12, 0] }; return g;
}
