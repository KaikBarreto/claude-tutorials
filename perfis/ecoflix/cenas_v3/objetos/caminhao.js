// Caminhão (cabine verde da marca) no material de degradê do kit v3 (serve nos dois climas).
// uso: const T = caminhao(CENA, { carga: 260 });  dirige(T, x, altura, { sobe, arfa });  bascula(T, ang);
//   o.tipo: 'truck' (padrão: 3 eixos, 7,3 m) | 'tres4' (o 3/4: 2 eixos, caçamba curta, 12% menor)
//   o.bau:  'basculante' (padrão, aço) | 'grade' (carroceria de madeira, carga à vista) | 'nenhum' (só o chassi)
//   o.carga: número de latinhas (padrão 260) | 0 (vazio) | 'bateria' (baterias em camadas). Outra carga: ponha você em
//            T.userData.bau, com monte.js: pecas(u.bau, 'ferro', pontosMonte(40, u.dim.C / 2 - .5, u.dim.LZ - .3, .5, u.dim.H * .5).map(p => [p[0] + u.dim.cx, p[1], p[2]]))
//   o.placa: 'ABC1D23' (placa genérica na frente e atrás; sem ela o caminhão sai sem placa), o.cor (cabine), o.cubo (cubo da roda)
//   T.userData: { corpo, bau, tampa, rodas, carga (InstancedMesh das latinhas, filha do baú), locais (posição de cada lata no
//     baú), dim { cx, C, H, LZ } (o baú por dentro, no referencial dele), eixos, k (escala), topo, placas }
// Frente em +x. Origem no chão, no meio do entre-eixos. Medidas em metros (truck: 7,3 de comprimento, 2,44 de largura).
import { THREE, PI, cl, lerp, rng, ri, mat, caixa, perfil, cil, malha, grupo } from '../motor.js';
import { placa } from './placa.js';
import { baterias } from './baterias.js';

export const CORES_LATA = ['#E9EEF2', '#DCE3EA', '#F4F6F8', '#CDD6DE', '#E9EEF2', '#DCE3EA', '#F4F6F8', '#C8553D', '#5B8FD6', '#3FA45B', '#F2B63D', '#D9734A', '#50D088', '#2C5FA8'];   // alumínio com algumas estampas
export const EIXOS = [-2.75, -1.62, 2.5], RAIO = .52, TRAS = -3.75;

export function caminhao(pai, o = {}) {
  const t34 = o.tipo === 'tres4', grade = o.bau === 'grade', eixos = t34 ? [-1.9, 2.5] : EIXOS, k = t34 ? .88 : 1;
  const g = grupo(pai), corpo = grupo(g), verde = mat(o.cor ?? '#50D088', { emi: .30, bri: .26 }), escuro = mat('#2B323B', { bri: .12 }), cinza = mat('#CBD3DC'), cinzaE = mat('#8F9BAA');
  // rodas (na raiz: não balançam com a suspensão)
  const rodas = [];
  for (const x of eixos) for (const z of [-1.0, 1.0]) {
    const r = grupo(g, [x, RAIO, z]); r.rotation.x = PI / 2; const gira = grupo(r);
    malha(cil(RAIO, .36, 36), mat('#262C34', { bri: .10 }), [0, 0, 0], gira); malha(cil(.31, .38, 28), mat('#E6EBF0', { emi: .1 }), [0, 0, 0], gira);
    malha(cil(.11, .40, 16), mat(o.cubo ?? '#50D088', { emi: 1.1 }), [0, 0, 0], gira);
    for (let i = 0; i < 5; i++) malha(cil(.035, .385, 8), escuro, [.2 * Math.cos(i * 2 * PI / 5), 0, .2 * Math.sin(i * 2 * PI / 5)], gira);
    rodas.push(gira);
  }
  // chassi, tanque, para-choque
  malha(caixa(t34 ? 6.1 : 7.0, .24, 1.0, .06), escuro, [t34 ? .25 : -.2, .76, 0], corpo); malha(caixa(1.9, .36, 2.2, .08), escuro, [2.52, .62, 0], corpo);
  malha(cil(.2, 1.0, 20), mat('#DCE3EA'), [.45, .56, 1.0], corpo, [0, 0, PI / 2]); malha(caixa(.2, .42, 2.44, .07), escuro, [3.6, .64, 0], corpo);
  // cabine: perfil com o para-brisa inclinado, janelas e faróis
  const PF = [[1.5, .78], [3.55, .78], [3.55, 1.78], [3.2, 2.66], [3.0, 2.8], [1.5, 2.8]];
  malha(perfil(PF, [.08, .1, .1, .12, .16, .16], 2.44, .07), verde, [0, 0, 0], corpo);
  const vidro = mat('#DDF1F7', { emi: .62, bri: .35, alt: 2.9 });
  malha(perfil([[2.22, 1.86], [3.18, 1.86], [2.95, 2.56], [2.22, 2.56]], .07, 2.47, .01), vidro, [0, 0, 0], corpo);
  malha(caixa(.78, .03, 2.06, .012), vidro, [3.40, 2.22, 0], corpo, [0, 0, 1.944]);
  for (const z of [-.86, .86]) malha(caixa(.05, .2, .34, .02), mat('#FFE9A8', { emi: 1.0, emiC: .1 }), [3.555, 1.18, z], corpo);
  malha(caixa(.06, .34, .1, .02), escuro, [3.3, 2.1, 1.3], corpo); malha(caixa(.06, .34, .1, .02), escuro, [3.3, 2.1, -1.3], corpo);
  // caçamba: gira na dobradiça de trás (bascula)
  const X0 = t34 ? -2.85 : TRAS, X1 = 1.32, Y0 = .98, H = 1.24, LZ = 1.18, bau = grupo(corpo, [X0 + .15, Y0, 0]), dx = -(X0 + .15), cx = (X0 + X1) / 2 + dx, C = X1 - X0;
  malha(caixa(C, .1, 2 * LZ, .03), cinzaE, [cx, .02, 0], bau);
  if (grade) {   // carroceria de madeira: três tábuas de cada lado, montantes escuros, frente e traseira de tábua
    const md = mat('#D8B58C', { alt: 3, emi: .16 }), mdE = mat('#BC9468', { alt: 3, emi: .16 });
    for (const y of [.22, .52, .82]) { for (const z of [-LZ, LZ]) malha(caixa(C, .22, .07, .025), md, [cx, y, z], bau);
      malha(caixa(.07, .22, 2 * LZ, .025), mdE, [X1 + dx, y, 0], bau); }
    for (const z of [-LZ, LZ]) for (let i = 0; i <= 4; i++) malha(caixa(.1, 1.0, .06, .02), escuro, [X0 + dx + .06 + i * (C - .12) / 4, .52, z + Math.sign(z) * .05], bau);
  } else for (const z of [-LZ, LZ]) { malha(caixa(C, H, .08, .03), cinza, [cx, H / 2, z], bau); malha(caixa(C + .06, .1, .13, .04), cinzaE, [cx, H, z], bau);
    for (let i = 1; i < 5; i++) malha(caixa(.1, H - .16, .05, .02), cinzaE, [X0 + dx + i * C / 5, H / 2 - .02, z + Math.sign(z) * .045], bau); }
  if (!grade) malha(caixa(.08, H + .16, 2 * LZ + .08, .03), cinzaE, [X1 + dx, H / 2 + .08, 0], bau);
  const tampa = grupo(bau, [X0 + dx, grade ? .93 : H, 0]); if (grade) { for (const y of [.22, .52, .82]) malha(caixa(.07, .22, 2 * LZ, .025), mat('#D8B58C', { alt: 3, emi: .16 }), [0, y - .93, 0], tampa); }
  else malha(caixa(.07, H, 2 * LZ, .03), cinza, [0, -H / 2, 0], tampa);
  // carga: latinhas (instâncias) num monte dentro do baú; locais = posição de cada uma no referencial do baú
  const u = { corpo, bau, tampa, rodas, x: 0, eixos, k, dim: { cx, C, H: grade ? .93 : H, LZ }, topo: [1.5 * k, 3.3 * k, 0] }; g.userData = u; g.scale.setScalar(k);
  if (o.bau === 'nenhum') bau.visible = false;   // só o chassi (o poliguindaste.js monta o resto)
  if (o.placa) u.placas = [placa(corpo, [3.705, .66, 0], o.placa, { w: .62 }), placa(corpo, [(t34 ? 6.1 : 7.0) / -2 + (t34 ? .25 : -.2) - .012, .76, 0], o.placa, { w: .62 })].map((p, i) => { p.rotation.y = i ? -PI / 2 : PI / 2; return p; });
  if (o.carga === 'bateria') { u.cargaBat = baterias(bau, [cx, .07, 0], { nx: Math.floor((C - .3) / .4), nz: Math.floor((2 * LZ - .25) / .27), camadas: 2 }); return g; }
  if (o.carga === 0 || o.carga === false || o.bau === 'nenhum') return g;
  const n = o.carga ?? 260, locais = [], im = new THREE.InstancedMesh(cil(.125, .26, 12), mat('#FFFFFF', { bri: .3, emi: .42, alt: 3.4 }), n), M = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), c = new THREE.Color();
  const hx = C / 2 - .2, hz = LZ - .16;
  for (let i = 0; i < n; i++) {
    const x = ri(-hx, hx), z = ri(-hz, hz), topo = H + .12 + .52 * (1 - (x / hx) ** 4) * (1 - .75 * (z / hz) ** 2), y = topo - .42 * rng() ** 1.6;
    const p = [cx + x, y, z, ri(0, 2 * PI), ri(0, 2 * PI), ri(0, 2 * PI)]; locais.push(p);
    e.set(p[3], p[4], p[5]); q.setFromEuler(e); M.compose(new THREE.Vector3(p[0], p[1], p[2]), q, new THREE.Vector3(1, 1, 1)); im.setMatrixAt(i, M);
    const h = parseInt(CORES_LATA[Math.floor(rng() * CORES_LATA.length)].slice(1), 16); c.setRGB((h >> 16 & 255) / 255, (h >> 8 & 255) / 255, (h & 255) / 255, THREE.LinearSRGBColorSpace); im.setColorAt(i, c);
  }
  im.frustumCulled = false; bau.add(im);
  u.carga = im; u.locais = locais;
  return g;
}
// põe o caminhão em x sobre o piso de altura(x) (rampa da balança), gira as rodas e responde com a suspensão:
// o.sobe = quanto a carroceria levanta (m; sem carga sobe), o.arfa = inclinação da carroceria (rad; freada e arrancada)
export function dirige(T, x, altura = () => 0, o = {}) {
  const u = T.userData, E = u.eixos, k = u.k, xf = E[E.length - 1] * k, xt = (E.length > 2 ? (E[0] + E[1]) / 2 : E[0]) * k, hf = altura(x + xf), ht = altura(x + xt);
  T.position.x = x; T.position.y = (hf + ht) / 2 - (hf - ht) / 5.2 * .16; T.rotation.z = Math.atan2(hf - ht, xf - xt);
  for (const r of u.rodas) r.rotation.y = x / (RAIO * k);
  u.corpo.position.y = o.sobe ?? 0; u.corpo.rotation.z = o.arfa ?? 0; u.x = x; return x;
}
export function bascula(T, ang) { const u = T.userData; u.bau.rotation.z = ang; u.tampa.rotation.z = -Math.min(1.25, ang * 2.6); }
