// Monte de latinhas no chão e a transferência das latas da caçamba para o monte (com gravidade e quique).
// uso: const alvo = domo(n, [x, 0, z], { r: 1.5, h: .95 });
//      despeja(T.userData.carga, T.userData.locais, alvo, t, a, { d: .62, passo: .6 / n, arco: .2, ordem });
//      (a InstancedMesh é filha do baú: enquanto a lata não saiu, ela acompanha a báscula)
import { THREE, PI, cl, lerp, rng, ri, golpe } from '../motor.js';
export function domo(n, c, o = {}) {   // posições finais [x, y, z, rx, ry, rz] no mundo, do miolo para a borda
  const r = o.r ?? 1.5, h = o.h ?? .95, L = [];
  for (let i = 0; i < n; i++) { const u = Math.sqrt((i + .5) / n), a = i * 2.39996 + ri(-.2, .2), rr = r * u * ri(.9, 1.06), topo = h * (1 - u * u) ** .8;
    L.push([c[0] + rr * Math.cos(a) * 1.08, .13 + topo * rng() ** .7, c[2] + rr * Math.sin(a) * .82, ri(0, 2 * PI), ri(0, 2 * PI), ri(0, 2 * PI)]); }
  return L;
}
const _m = new THREE.Matrix4(), _i = new THREE.Matrix4(), _p = new THREE.Vector3(), _q = new THREE.Quaternion(), _q2 = new THREE.Quaternion(), _e = new THREE.Euler(), _s = new THREE.Vector3(1, 1, 1), _a = new THREE.Vector3(), _qp = new THREE.Quaternion(), _s2 = new THREE.Vector3();
// ordem = índices das latas na ordem de saída (padrão: de trás para a frente do baú); cada lata escorrega até a boca,
// cai acelerando até o lugar dela no monte e dá um quique curto
export function despeja(im, locais, alvo, t, a, o = {}) {
  const n = locais.length, d = o.d ?? .62, passo = o.passo ?? .6 / n, arco = o.arco ?? .18;
  const ordem = o.ordem ?? (im.userData.ordem ??= locais.map((p, i) => i).sort((i, j) => locais[i][0] - locais[j][0]));
  const pai = im.parent; pai.updateWorldMatrix(true, false); _i.copy(pai.matrixWorld).invert();
  pai.matrixWorld.decompose(_a, _qp, _s2);
  for (let k = 0; k < n; k++) {
    const i = ordem[k], L = locais[i], A = alvo[k], u = (t - a - k * passo) / d, x = cl(u);
    _e.set(L[3], L[4], L[5]); _q.setFromEuler(_e);
    if (x <= 0) { _p.set(L[0], L[1], L[2]); _m.compose(_p, _q, _s); im.setMatrixAt(i, _m); continue; }
    _a.set(L[0], L[1], L[2]).applyMatrix4(pai.matrixWorld);   // de onde sai (mundo), já com a báscula
    const q = x * x * (3 - 2 * x), quique = u > 1 ? .07 * Math.abs(golpe(cl((u - 1) * d / .34), 1, 3)) : 0;
    _p.set(lerp(_a.x, A[0], q), lerp(_a.y, A[1], x * x) + arco * 4 * x * (1 - x) * (1 - x) + quique, lerp(_a.z, A[2], q));
    _e.set(A[3], A[4], A[5]); _q.premultiply(_qp).slerp(_q2.setFromEuler(_e), q);
    _m.compose(_p, _q, _s).premultiply(_i); im.setMatrixAt(i, _m);
  }
  im.instanceMatrix.needsUpdate = true;
}
