// Fardo prensado, por material: bloco com as peças amassadas nas faces e as cintas.
// uso: fardo(CENA, [x, 0, z], { tipo: 'latinha' });   tipos: latinha, pet, papelao, aluminio, cobre, plastico, ferro
// o: w (1.0), h (.78), d (.78), cintas (2). Empilha: fardo(pai, [x, .78, z]) (use mancha: false nos de cima).
// userData: h, topo. fardoLatinhas e fardoPapelao são os atalhos com o nome do kit antigo.
import { THREE, PI, ri, pega, mat, caixa, malha, grupo, mancha, lote, poeInst } from '../motor.js';
import { peca, CORES } from './monte.js';
const MIOLO = { latinha: '#C4CDD6', pet: '#CFE7F1', aluminio: '#C9D1DA', cobre: '#C8703A', plastico: '#B9C7D8', ferro: '#6E7884' };
const FACE = { latinha: 'lataAm', pet: 'petAm', aluminio: 'blocoAl', cobre: 'novelo', plastico: 'caco', ferro: 'chapa' }, PASSO = { latinha: .15, pet: .17, aluminio: .2, cobre: .2, plastico: .2, ferro: .3 };
export function fardo(pai, pos = [0, 0, 0], o = {}) {
  const tipo = o.tipo ?? 'latinha', w = o.w ?? 1.0, h = o.h ?? .78, d = o.d ?? .78, g = grupo(pai, pos), cinta = mat('#3B444E', { bri: .14, emi: .5 });
  if (o.mancha !== false) mancha(w + 1.1, d + 1.1, [0, 0, .08], { pai: g, op: .75 });
  if (tipo === 'papelao') {   // camadas de papelão em tons de pardo
    const n = Math.max(6, Math.round(h / .06)), e = (h - .02) / n;
    for (let i = 0; i < n; i++) malha(caixa(w + ri(-.05, .05), e * .98, d + ri(-.05, .05), .014), mat(CORES.papelao[i % 4], { bri: .1, emi: .3, alt: 3 }), [ri(-.025, .025), (i + .5) * e + .01, ri(-.025, .025)], g, [0, ri(-.03, .03), 0]);
    for (const x of [-w * .3, 0, w * .3]) malha(caixa(.022, h + .03, d + .07, .008), cinta, [x, h / 2, 0], g);
  } else {
    malha(caixa(w, h, d, .06), mat(MIOLO[tipo], { bri: .2, emi: .35, alt: 3, op: tipo === 'pet' ? .9 : 1 }), [0, h / 2, 0], g);
    const e = PASSO[tipo], P = [], R = [], grade = (a, b) => { const n = Math.max(1, Math.floor((a - .1) / e)), m = Math.max(1, Math.floor((b - .1) / e)), L = [];
      for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) L.push([(i - (n - 1) / 2) * e + ri(-.02, .02), (j - (m - 1) / 2) * e + ri(-.02, .02)]); return L; };
    // a peça deita na face, achatada contra ela (o eixo z da peça = a normal da face)
    for (const s of [-1, 1]) { for (const [x, y] of grade(w, h)) { P.push([x, h / 2 + y, s * (d / 2 + .012)]); R.push([ri(-.15, .15), s < 0 ? PI : 0, ri(0, 2 * PI)]); }
      for (const [z, y] of grade(d, h)) { P.push([s * (w / 2 + .012), h / 2 + y, z]); R.push([ri(-.15, .15), s * PI / 2, ri(0, 2 * PI)]); } }
    for (const [x, z] of grade(w, d)) { P.push([x, h + .012, z]); R.push([-PI / 2 + ri(-.15, .15), 0, ri(0, 2 * PI)]); }
    const [geo, m, cores] = peca(FACE[tipo]), im = lote(geo, m(), P.length, g), k = tipo === 'ferro' ? .42 : tipo === 'aluminio' || tipo === 'plastico' ? .6 : tipo === 'cobre' ? .55 : .62;
    // gira a peça para ela ficar de frente (o eixo y dela vira a normal) e achata
    const q = new THREE.Quaternion(), q2 = new THREE.Quaternion().setFromEuler(new THREE.Euler(PI / 2, 0, 0)), M = new THREE.Matrix4(), c = new THREE.Color();
    P.forEach((p, i) => { q.setFromEuler(new THREE.Euler(R[i][0], R[i][1], 0)).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, R[i][2]))).multiply(q2);
      im.setMatrixAt(i, M.compose(new THREE.Vector3(...p), q, new THREE.Vector3(k * ri(.9, 1.15), .34, k * ri(.9, 1.15))));
      const hx = parseInt(pega(cores).slice(1), 16); im.setColorAt(i, c.setRGB((hx >> 16 & 255) / 255, (hx >> 8 & 255) / 255, (hx & 255) / 255, THREE.LinearSRGBColorSpace)); });
    const nc = o.cintas ?? 2; for (let i = 0; i < nc; i++) malha(caixa(.04, h + .07, d + .07, .012), cinta, [w * (-.28 + .56 * (nc > 1 ? i / (nc - 1) : .5)), h / 2, 0], g);
  }
  g.userData = { h, topo: [0, h + .5, 0] }; return g;
}
export const fardoLatinhas = (pai, pos, o = {}) => fardo(pai, pos, { ...o, tipo: 'latinha' });
export const fardoPapelao = (pai, pos, o = {}) => fardo(pai, pos, { ...o, tipo: 'papelao' });
