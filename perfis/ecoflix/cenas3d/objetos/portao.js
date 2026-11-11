// portao(pai, p, o): portão de entrada do pátio, sem marca: dois pilares, viga com a placa verde-escura na frente e um trecho de
// cerca de grade de cada lado. Frente (a placa) para +z; passa-se pelo vão ao longo de z; base em y 0, centro do vão em x 0.
// o: vao (largura livre, 4.2), h (altura dos pilares, 3.2), cerca (comprimento de cada trecho, 1.8), hc (altura da cerca, 1.5),
//    placa (texto pintado em branco na placa; '' ou ausente = placa lisa: o nome da empresa só onde a fala/cena o mostra).
// userData.placa = ponto (local) no meio da placa; userData.topo = ponto acima da viga; userData.vao.
// Uso (T00): portao(CENA, [x, 0, z], { placa: 'Recicla Vale Metais' }); de lado: g.rotation.y = PI / 2.
import { THREE, grupo, poe, rbox, M, mancha } from '../kit3d.js';

export function portao(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), vao = o.vao ?? 4.2, h = o.h ?? 3.2, ce = o.cerca ?? 1.8, hc = o.hc ?? 1.5, px = vao / 2 + .2;
  const mPil = M('#7E8994'), mVi = M('#5B636C'), mBa = M('#AAB2BA'), mTr = M('#8A949E');
  for (const s of [-1, 1]) { poe(rbox(.4, h, .4, .05, 2), mPil, g, [s * px, h / 2, 0]); poe(rbox(.5, .08, .5, .03, 1), mVi, g, [s * px, h + .04, 0]); }
  poe(rbox(2 * px + .5, .26, .3, .04, 2), mVi, g, [0, h - .2, 0]);                                              // viga
  const pw = Math.min(vao - .2, 3.6), ph = .72, py = h - .75;
  poe(rbox(pw, ph, .08, .04, 2), M('#2E7D57'), g, [0, py, .2]);                                                 // placa
  for (const s of [-1, 1]) poe(rbox(.08, .5, .08, .02, 1), mVi, g, [s * pw * .36, py + .5, .18]);
  if (o.placa) {
    const cv = document.createElement('canvas'), W = 1400, H = Math.round(W * ph / pw); cv.width = W; cv.height = H;
    const x = cv.getContext('2d'); x.fillStyle = '#2E7D57'; x.fillRect(0, 0, W, H);
    let fs = H * .5; x.font = `800 ${fs}px M, Montserrat, sans-serif`; const mw = x.measureText(o.placa).width; if (mw > W * .88) fs *= W * .88 / mw;
    x.font = `800 ${fs.toFixed(1)}px M, Montserrat, sans-serif`; x.fillStyle = '#FFFFFF'; x.textAlign = 'center'; x.textBaseline = 'middle';
    x.fillText(o.placa, W / 2, H * .53);
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    const f = new THREE.Mesh(new THREE.PlaneGeometry(pw - .08, ph - .08), new THREE.MeshStandardMaterial({ map: t, roughness: .8, metalness: 0 }));
    f.position.set(0, py, .2405); g.add(f);
  }
  // cerca de grade: postes, travessas e barras
  for (const s of [-1, 1]) {
    const x0 = s * (px + .2), x1 = s * (px + .2 + ce);
    poe(rbox(.12, hc + .1, .12, .03, 1), mVi, g, [x1, (hc + .1) / 2, 0]);
    for (const y of [.22, hc - .12]) poe(rbox(ce, .05, .05, .015, 1), mTr, g, [(x0 + x1) / 2, y, 0]);
    for (let i = 1; i * .2 < ce - .05; i++) poe(rbox(.045, hc, .045, .012, 1), mBa, g, [x0 + s * i * .2, hc / 2, 0]);
  }
  for (const s of [-1, 1]) mancha(g, .9, .9, .28, [s * px, 0, 0]);
  g.userData.placa = [0, py, .25]; g.userData.topo = [0, h + .15, 0]; g.userData.vao = vao; return g;
}
