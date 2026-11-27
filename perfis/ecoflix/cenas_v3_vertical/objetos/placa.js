// Placa de veículo genérica (tarja azul no alto e os caracteres grandes), face para +z, pivô no centro. Sem brasão nem bandeira.
// uso: const p = placa(CENA, [x, y, z], 'RCV2E26', { w: .62 }); p.rotation.y = -PI / 2;   (o caminhao.js já a põe com o.placa)
// Para a placa "voar" até um cartão, mexa em position/rotation do grupo. userData: w, h, troca(texto).
import { mat, caixa, malha, grupo, pintura, THREE } from '../motor.js';
export function placa(pai, pos, texto, o = {}) {
  const g = grupo(pai, pos), w = o.w ?? .52, h = w * .31;
  const des = txt => (x, W, H) => { x.fillStyle = '#F7F8F9'; x.fillRect(0, 0, W, H); x.fillStyle = '#2F5FB0'; x.fillRect(0, 0, W, 34);
    x.fillStyle = '#18202A'; x.font = '800 98px M, Montserrat, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'alphabetic'; x.fillText(txt, 260, 138, 470); };
  const m = pintura(520, 160, des(texto), { emi: .7 });
  malha(caixa(w, h, .03, .012), mat('#2B323B', { bri: .12, emi: .24 }), [0, 0, 0], g); malha(new THREE.PlaneGeometry(w * .94, h * .86), m, [0, 0, .0165], g);
  g.userData = { w, h, troca: t => m.userData.refaz(des(t)) }; return g;
}
