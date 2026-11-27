// Pessoa que senta e levanta: a mesma figura da pessoa.js (sem rosto, de frente para +x, pés em y 0, 1,72 m), com a perna
// em duas partes (coxa e canela) para dobrar o joelho. A origem do grupo é o eixo do quadril.
// uso: const p = pessoaSenta(CENA, [x, 0, z], { camisa: '#5B8FD6' }); p.rotation.y = -PI / 2; p.userData.senta(1);
//      sentada na cadeira.js: ponha o grupo 0,12 m atrás do centro do assento (o quadril encosta no encosto).
// o: s, pele, cabelo, camisa, calca, sapato, coque, assento (altura do tampo da cadeira, 0.42).
// userData.senta(k): 0 = de pé, 1 = sentada (o quadril desce, a coxa vai para a frente, a canela fica a prumo, mãos no colo).
// userData.anda(f): fase do passo em radianos (distância * 5.2), só de pé. userData: topo (acompanha o senta), altura(k).
import { mat, caixa, cil, capsula, esfera, malha, grupo, mancha, THREE, PI, lerp } from '../motor.js';
export function pessoaSenta(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), u = g.userData, s = o.s ?? 1, corpo = grupo(g), A = { alt: 1.9 * s, bri: .16, emi: .22 }, QS = (o.assento ?? .42) + .05;
  const pele = mat(o.pele ?? '#DCA580', A), cab = mat(o.cabelo ?? '#3A2A22', { ...A, emi: .36 }), cam = mat(o.camisa ?? '#5B8FD6', A), cal = mat(o.calca ?? '#3E4A59', { ...A, emi: .32 }), sap = mat(o.sapato ?? '#2B2F36', { ...A, emi: .32 });
  corpo.scale.setScalar(s); mancha(1.3 * s, 1.0 * s, [.03, 0, .03], { pai: g, op: .7 });
  const cima = grupo(corpo);   // tudo o que desce ao sentar (quadril para cima)
  u.pernas = [-1, 1].map(sz => { const q = grupo(cima, [0, .86, sz * .095]); malha(capsula(.074, .27), cal, [0, -.2, 0], q);
    const j = grupo(q, [0, -.41, 0]); malha(capsula(.068, .26), cal, [0, -.2, 0], j); malha(caixa(.26, .09, .125, .035), sap, [.045, -.395, 0], j); q.userData.joelho = j; return q; });
  const tronco = grupo(cima), tr = malha(capsula(.17, .36, 16), cam, [0, 1.17, 0], tronco); tr.scale.set(.76, 1, 1.12);
  u.bracos = [-1, 1].map(sz => { const q = grupo(tronco, [0, 1.4, sz * .25]); malha(capsula(.056, .46), cam, [0, -.27, 0], q); malha(esfera(.064, [1, 1, 1], 12), pele, [0, -.58, 0], q); return q; });
  malha(cil(.058, .1, 12, .05), pele, [0, 1.56, 0], tronco); malha(esfera(.137), pele, [0, 1.69, 0], tronco);
  const meia = (r, ang) => new THREE.SphereGeometry(r, 20, 12, 0, 2 * PI, 0, PI * ang);
  malha(meia(.146, .56), cab, [-.014, 1.705, 0], tronco, [0, 0, .32]); if (o.coque) malha(esfera(.074, [1, 1, 1], 14), cab, [-.085, 1.83, 0], tronco);
  let K = 0;
  u.altura = k => lerp(2.0, 2.0 - (.86 - QS), k) * s;
  u.senta = k => { K = k; cima.position.y = -(.86 - QS) * k; for (const q of u.pernas) { q.rotation.z = k * PI / 2; q.userData.joelho.rotation.z = -k * PI / 2; }
    for (const b of u.bracos) b.rotation.z = .5 * k; tronco.rotation.z = 0; u.topo = [0, u.altura(k), 0]; };
  u.anda = f => { if (K > .02) return; const a = .42 * Math.sin(f); u.pernas[0].rotation.z = a; u.pernas[1].rotation.z = -a; u.pernas[0].userData.joelho.rotation.z = -.5 * Math.max(0, -a); u.pernas[1].userData.joelho.rotation.z = -.5 * Math.max(0, a);
    u.bracos[0].rotation.z = -.55 * a; u.bracos[1].rotation.z = .55 * a; cima.position.y = .022 * (Math.abs(Math.cos(f)) - 1); };
  u.senta(0); return g;
}
