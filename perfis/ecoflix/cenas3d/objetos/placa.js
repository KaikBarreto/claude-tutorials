// placa(pai, p, texto, o): placa de veículo (Mercosul genérica: tarja azul no alto e a sigla grande), face para +z, pivô no centro.
// o: w (largura, .52). userData.w, userData.h. Para voar de um lugar a outro, mexa em position/rotation do grupo.
// Uso (T16): const pl = placa(CENA, [x, y, z], 'FJR3B27'); pl.rotation.y = -PI / 2 (na traseira do caminhão).
import { THREE, grupo, poe, rbox, M, COR } from '../kit3d.js';

export function placa(pai, p, texto, o = {}) {
  const g = grupo(pai, p), w = o.w ?? .52, h = w * .31, cv = document.createElement('canvas'); cv.width = 520; cv.height = 160;
  const x = cv.getContext('2d'); x.fillStyle = '#F7F8F9'; x.fillRect(0, 0, 520, 160);
  x.fillStyle = '#2F5FB0'; x.fillRect(0, 0, 520, 34);
  x.fillStyle = '#18202A'; x.font = '800 98px M, Montserrat, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'alphabetic';
  x.save(); x.translate(260, 138); x.scale(1, 1); x.fillText(texto, 0, 0, 470); x.restore();
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  poe(rbox(w, h, .022, .014, 2), M('#2B323B'), g);
  const f = new THREE.Mesh(new THREE.PlaneGeometry(w * .94, h * .86), new THREE.MeshStandardMaterial({ map: t, roughness: .7, metalness: 0 }));
  f.position.z = .0125; f.castShadow = f.receiveShadow = false; g.add(f);
  g.userData.w = w; g.userData.h = h; return g;
}
