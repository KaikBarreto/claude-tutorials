// pessoa(pai, p, o): figura de argila sem rosto que anda (pernas, tronco, braços, cabeça e cabelo), de frente para +x, pés em
// y 0, ~1,7 m (o.s escala). o: pele, cabelo, camisa, calca, sapato, coque (cabelo preso no alto), bone (cor do boné).
// userData.anda(f, braco): pernas na fase f (radianos; f = distância andada * 5.2 dá passada de ~1,2 m; anda(0) = parada);
//   braco indefinido = braços balançam com o passo; braco = ângulo fixo dos dois braços (positivo = à frente, ex.: segurar algo).
// userData.mao = [esquerda (-z), direita (+z)] (grupos na ponta dos braços), userData.topo = ponto acima da cabeça.
// Uso (T00): const ci = pessoa(CENA, [x, 0, z], { camisa: '#C8664A', coque: true }); ci.rotation.y = giro; ci.userData.anda(d * 5.2);
import { THREE, grupo, poe, rbox, M, mancha } from '../kit3d.js';

export function pessoa(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), u = g.userData, s = o.s ?? 1, corpo = grupo(g);
  const mPele = M(o.pele ?? '#C98E6B'), mCab = M(o.cabelo ?? '#3A2A22'), mCam = M(o.camisa ?? '#5B8DB8'), mCal = M(o.calca ?? '#3E4A59'),
    mSap = M(o.sapato ?? '#2B2F36');
  corpo.scale.setScalar(s);
  // pernas: pivô no quadril; a perna gira em z (positivo leva o pé para +x)
  u.pernas = [-1, 1].map(sz => { const q = grupo(corpo, [0, .86, sz * .095]);
    poe(new THREE.CapsuleGeometry(.072, .64, 4, 10), mCal, q, [0, -.41, 0]); poe(rbox(.25, .08, .12, .03, 1), mSap, q, [.045, -.8, 0]); return q; });
  const tronco = grupo(corpo);
  poe(new THREE.CapsuleGeometry(.17, .36, 5, 14), mCam, tronco, [0, 1.17, 0], [0, 0, 0], [.74, 1, 1.12]);
  u.bracos = [-1, 1].map(sz => { const q = grupo(tronco, [0, 1.4, sz * .245]);
    poe(new THREE.CapsuleGeometry(.056, .46, 4, 10), mCam, q, [0, -.27, 0]); const mao = grupo(q, [0, -.58, 0]);
    poe(new THREE.SphereGeometry(.062, 12, 10), mPele, mao); q.userData.mao = mao; return q; });
  poe(new THREE.CylinderGeometry(.05, .058, .1, 12), mPele, tronco, [0, 1.56, 0]);
  poe(new THREE.SphereGeometry(.135, 20, 16), mPele, tronco, [0, 1.69, 0]);
  if (o.bone) { poe(new THREE.SphereGeometry(.143, 20, 10, 0, Math.PI * 2, 0, Math.PI * .5), M(o.bone), tronco, [-.005, 1.71, 0]);
    poe(rbox(.16, .022, .22, .01, 1), M(o.bone), tronco, [.13, 1.72, 0]); }
  else {
    poe(new THREE.SphereGeometry(.143, 20, 12, 0, Math.PI * 2, 0, Math.PI * .56), mCab, tronco, [-.014, 1.705, 0], [0, 0, .32]);
    if (o.coque) poe(new THREE.SphereGeometry(.072, 14, 12), mCab, tronco, [-.085, 1.83, 0]);
  }
  u.tronco = tronco; u.mao = u.bracos.map(b => b.userData.mao); u.topo = [0, 1.95 * s, 0];
  mancha(g, .8, .6, .28);
  u.anda = (f, braco) => {
    const a = .42 * Math.sin(f);
    u.pernas[0].rotation.z = a; u.pernas[1].rotation.z = -a;
    if (braco === undefined) { u.bracos[0].rotation.z = -.55 * a; u.bracos[1].rotation.z = .55 * a; }
    else { u.bracos[0].rotation.z = braco; u.bracos[1].rotation.z = braco; }
    tronco.position.y = .022 * (Math.abs(Math.cos(f)) - 1); tronco.rotation.z = -.04 * Math.abs(Math.sin(f));
  };
  u.anda(0); return g;
}
