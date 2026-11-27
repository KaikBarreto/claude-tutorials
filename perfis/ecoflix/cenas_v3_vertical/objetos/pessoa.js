// Pessoa: figura sem rosto que anda (pernas, tronco, braços, cabeça e cabelo), de frente para +x, pés em y 0, 1,72 m.
// uso: const p = pessoa(CENA, [x, 0, z], { camisa: '#C8664A', coque: true }); p.rotation.y = giro; p.userData.anda(dist * 5.2);
// o: s (escala), pele, cabelo, camisa, calca, sapato, coque (cabelo preso), bone (cor do boné), colete (cor do colete de pátio).
// userData.anda(f, braco): f = fase do passo em radianos (distância andada * 5.2 = passada de ~1,2 m; anda(0) = parada);
//   braco indefinido = os braços balançam com o passo; braco = ângulo fixo dos dois (positivo = à frente: segurar algo).
// userData: pernas, bracos, mao [esquerda (-z), direita (+z)] (grupos na ponta dos braços), tronco, topo.
import { mat, caixa, cil, capsula, esfera, malha, grupo, mancha, THREE, PI } from '../motor.js';
export function pessoa(pai, pos = [0, 0, 0], o = {}) {
  const g = grupo(pai, pos), u = g.userData, s = o.s ?? 1, corpo = grupo(g), A = { alt: 1.9 * s, bri: .16, emi: .22 };
  const pele = mat(o.pele ?? '#DCA580', A), cab = mat(o.cabelo ?? '#3A2A22', { ...A, emi: .36 }), cam = mat(o.camisa ?? '#5B8FD6', A), cal = mat(o.calca ?? '#3E4A59', { ...A, emi: .32 }), sap = mat(o.sapato ?? '#2B2F36', { ...A, emi: .32 });
  corpo.scale.setScalar(s); mancha(1.3 * s, 1.0 * s, [.03, 0, .03], { pai: g, op: .7 });
  u.pernas = [-1, 1].map(sz => { const q = grupo(corpo, [0, .86, sz * .095]); malha(capsula(.074, .64), cal, [0, -.41, 0], q); malha(caixa(.26, .09, .125, .035), sap, [.045, -.805, 0], q); return q; });
  const tronco = grupo(corpo), tr = malha(capsula(.17, .36, 16), cam, [0, 1.17, 0], tronco); tr.scale.set(.76, 1, 1.12);
  if (o.colete) { const c = malha(capsula(.176, .2, 16), mat(o.colete, { ...A, emi: .36 }), [0, 1.2, 0], tronco); c.scale.set(.78, 1, 1.14); malha(caixa(.28, .035, .41, .012), mat('#F4F6F8', { emi: .5 }), [0, 1.14, 0], tronco); }
  u.bracos = [-1, 1].map(sz => { const q = grupo(tronco, [0, 1.4, sz * .25]); malha(capsula(.056, .46), cam, [0, -.27, 0], q); const mao = grupo(q, [0, -.58, 0]); malha(esfera(.064, [1, 1, 1], 12), pele, [0, 0, 0], mao); q.userData.mao = mao; return q; });
  malha(cil(.058, .1, 12, .05), pele, [0, 1.56, 0], tronco); malha(esfera(.137), pele, [0, 1.69, 0], tronco);
  const meia = (r, ang) => new THREE.SphereGeometry(r, 20, 12, 0, 2 * PI, 0, PI * ang);
  if (o.bone) { malha(meia(.146, .5), mat(o.bone, { ...A, emi: .36 }), [-.005, 1.71, 0], tronco); malha(caixa(.17, .024, .22, .011), mat(o.bone, { ...A, emi: .36 }), [.13, 1.722, 0], tronco); }
  else { malha(meia(.146, .56), cab, [-.014, 1.705, 0], tronco, [0, 0, .32]); if (o.coque) malha(esfera(.074, [1, 1, 1], 14), cab, [-.085, 1.83, 0], tronco); }
  u.tronco = tronco; u.mao = u.bracos.map(b => b.userData.mao); u.topo = [0, 2.0 * s, 0];
  u.anda = (f, braco) => { const a = .42 * Math.sin(f); u.pernas[0].rotation.z = a; u.pernas[1].rotation.z = -a;
    if (braco === undefined) { u.bracos[0].rotation.z = -.55 * a; u.bracos[1].rotation.z = .55 * a; } else { u.bracos[0].rotation.z = braco; u.bracos[1].rotation.z = braco; }
    tronco.position.y = .022 * (Math.abs(Math.cos(f)) - 1); tronco.rotation.z = -.04 * Math.abs(Math.sin(f)); };
  u.anda(0); return g;
}
