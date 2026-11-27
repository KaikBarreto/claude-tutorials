// Monte de material no chão, por tipo, e as peças soltas (para pôr em saco, caçamba, baia, esteira, baú de caminhão).
// uso: const m = monte(CENA, [x, 0, z], { tipo: 'pet', n: 150, r: 1.4, h: .9 });        cai(m, t, a) faz as peças caírem no lugar
//      const p = pecas(pai, 'cobre', P, { s: .6 });   P = [[x, y, z], ...] no pai; devolve a lista de lotes (InstancedMesh)
// tipos: latinha (coloridas e de alumínio, inteiras e amassadas), pet (transparente e verde, inteiro e amassado, com tampa),
//        ferro (vergalhão, cano, chapa, cantoneira, com ferrugem), papelao, cobre (bobina, tubo, novelo de fio), aluminio
//        (perfil, chapa, bloco), plastico (cacos e galões coloridos), bateria, misto.
// As peças têm tamanho de ilustração (lata de 26 cm, garrafa de 42 cm), o mesmo da carga do caminhão: leem de longe.
// o: n, r (raio em x), rz (padrão r * .78), h (altura do monte), s (escala das peças), mancha (false tira a sombra).
// userData: lotes, h, topo [x, y, z] local (prenda ali o chip do material).
import { THREE, PI, cl, lerp, rng, ri, pega, golpe, mat, caixa, perfil, cil, toro, torno, grupo, mancha, lote, poeInst } from '../motor.js';
// as mesmas cores da carga do caminhão (caminhao.js): alumínio com algumas estampas
const CORES_LATA = ['#E9EEF2', '#DCE3EA', '#F4F6F8', '#CDD6DE', '#E9EEF2', '#DCE3EA', '#F4F6F8', '#C8553D', '#5B8FD6', '#3FA45B', '#F2B63D', '#D9734A', '#50D088', '#2C5FA8'];

export const CORES = {
  latinha: CORES_LATA, pet: ['#E3F3FA', '#D3ECF6', '#EEF8FC', '#DDF1F8', '#62C783', '#49AD6C', '#62C783'], tampa: ['#E5574A', '#3D7DD8', '#F4F6F8', '#F2B63D', '#3FA45B'],
  ferro: ['#727D8A', '#84909D', '#626D79', '#939EAA', '#A2714F', '#8E5C44', '#727D8A'], papelao: ['#CFA672', '#BF9160', '#DAB582', '#B08457'],
  cobre: ['#DD8650', '#CC7440', '#E8A06A', '#BE6734'], aluminio: ['#DCE3EA', '#C9D1DA', '#EEF2F5', '#B8C2CC'],
  plastico: ['#4F8EDC', '#E9EEF4', '#E5574A', '#F2B63D', '#50D088', '#3E7BC6'] };
// material de cada família: o mesmo material do kit (dois climas), com a cor de cada peça na instância
const M = { metal: () => mat('#FFFFFF', { bri: .3, emi: .42, alt: 3.4 }), pet: () => mat('#FFFFFF', { bri: .6, emi: .55, emiC: .06, alt: 3, op: .62 }),
  fosco: () => mat('#FFFFFF', { bri: .1, emi: .3, alt: 3 }), ferro: () => mat('#FFFFFF', { bri: .2, emi: .32, alt: 3 }), cobre: () => mat('#FFFFFF', { bri: .42, emi: .6, emiC: .05, alt: 3 }) };
const amassa = (g, f) => { const P = g.attributes.position; for (let i = 0; i < P.count; i++) { const [x, y, z] = f(P.getX(i), P.getY(i), P.getZ(i)); P.setXYZ(i, x, y, z); } g.computeVertexNormals(); return g; };
const LATA = [[0, -.13], [.09, -.13], [.122, -.112], [.125, -.09], [.125, .085], [.108, .122], [.1, .13], [0, .13]];
const PET = [[0, -.21], [.085, -.21], [.106, -.19], [.106, -.11], [.096, -.09], [.106, -.07], [.106, .05], [.07, .13], [.038, .165], [.038, .2], [0, .2]];
const G = {}, deitado = () => [ri(-.3, .3), ri(0, 2 * PI), PI / 2 + ri(-.3, .3)], livre = () => [ri(0, 2 * PI), ri(0, 2 * PI), ri(0, 2 * PI)], plano = () => [ri(-.32, .32), ri(0, 2 * PI), ri(-.32, .32)];
// peça: [geometria, material, cores, giro, [escala mín, máx]]
const PECA = {
  lata: () => [torno(LATA, 14), M.metal, CORES.latinha, livre, [.92, 1.08]],
  lataAm: () => [amassa(torno(LATA, 14), (x, y, z) => [x * 1.08 + y * .28, y * .52 + .05 * Math.sin(x * 22), z * 1.1]), M.metal, CORES.latinha, livre, [.92, 1.08]],
  pet: () => [torno(PET, 16), M.pet, CORES.pet, deitado, [.9, 1.1]],
  petAm: () => [amassa(torno(PET, 16), (x, y, z) => [x * 1.12 + .035 * Math.sin(y * 21), y * .9, z * .42 + .02 * Math.sin(y * 31 + 1)]), M.pet, CORES.pet, deitado, [.9, 1.1]],
  vergalhao: () => [cil(.024, 1.55, 8), M.ferro, CORES.ferro, deitado, [.7, 1.1]], cano: () => [cil(.075, .95, 14), M.ferro, CORES.ferro, deitado, [.8, 1.1]],
  chapa: () => [caixa(.78, .035, .5, .012), M.ferro, CORES.ferro, plano, [.7, 1.1]],
  cantoneira: () => [perfil([[0, 0], [.17, 0], [.17, .035], [.035, .035], [.035, .17], [0, .17]], .006, 1.05, .004), M.ferro, CORES.ferro, plano, [.8, 1.1]],
  caixaP: () => [caixa(.52, .36, .42, .025), M.fosco, CORES.papelao, plano, [.8, 1.15]], folhaP: () => [caixa(.66, .045, .5, .015), M.fosco, CORES.papelao, plano, [.8, 1.2]],
  bobina: () => [toro(.19, .085, 22), M.cobre, CORES.cobre, () => [PI / 2 + ri(-.5, .5), ri(0, 2 * PI), ri(-.4, .4)], [.85, 1.15]],
  tuboCu: () => [cil(.04, .85, 10), M.cobre, CORES.cobre, deitado, [.7, 1.1]],
  novelo: () => [new THREE.TorusKnotGeometry(.15, .034, 56, 6, 2, 3), M.cobre, CORES.cobre, livre, [.85, 1.2]],
  perfilAl: () => [perfil([[0, 0], [.2, 0], [.2, .1], [.17, .1], [.17, .03], [.03, .03], [.03, .1], [0, .1]], .006, 1.1, .004), M.metal, CORES.aluminio, plano, [.8, 1.1]],
  chapaAl: () => [caixa(.7, .03, .48, .012), M.metal, CORES.aluminio, plano, [.75, 1.1]], blocoAl: () => [caixa(.34, .2, .26, .03), M.metal, CORES.aluminio, livre, [.8, 1.1]],
  caco: () => [caixa(.36, .06, .28, .02), M.fosco, CORES.plastico, plano, [.7, 1.2]],
  galao: () => [torno([[0, -.19], [.13, -.19], [.15, -.17], [.15, .09], [.1, .15], [.045, .17], [.045, .21], [0, .21]], 14), M.fosco, CORES.plastico, deitado, [.85, 1.1]] };
export const peca = k => (G[k] ??= PECA[k]());
export const TIPOS = { latinha: ['lata', 'lata', 'lata', 'lataAm', 'lataAm'], pet: ['pet', 'pet', 'pet', 'petAm', 'petAm'], ferro: ['vergalhao', 'vergalhao', 'cano', 'chapa', 'cantoneira', 'vergalhao'],
  papelao: ['caixaP', 'folhaP', 'folhaP'], cobre: ['bobina', 'tuboCu', 'tuboCu', 'novelo'], aluminio: ['perfilAl', 'perfilAl', 'chapaAl', 'blocoAl'], plastico: ['caco', 'caco', 'galao'],
  misto: ['lata', 'lataAm', 'pet', 'cano', 'chapa', 'caixaP', 'bobina', 'blocoAl', 'caco'] };
const tampa = () => (G.tampa ??= cil(.043, .045, 10));
const _m = new THREE.Matrix4(), _t = new THREE.Matrix4().makeTranslation(0, .212, 0);
// pecas: põe as peças do tipo nos pontos P (no pai). o.s = escala, o.r(i) = giro da peça i, o.tipos = lista de peças
export function pecas(pai, tipo, P, o = {}) {
  if (tipo === 'bateria') { const L = bateriasLote(pai, P.map(p => [p[0], p[1], p[2], ri(0, 2 * PI), ri(-.5, .5)]), o.s ?? 1); return L; }
  const ks = o.tipos ?? TIPOS[tipo], qual = P.map(() => pega(ks)), lotes = [], s = o.s ?? 1;
  for (const k of new Set(ks)) {
    const ix = qual.map((q, i) => q === k ? i : -1).filter(i => i >= 0); if (!ix.length) continue;
    const [g, m, cores, giro, es] = peca(k), im = lote(g, m(), ix.length, pai), tp = k.startsWith('pet') ? lote(tampa(), mat('#FFFFFF', { bri: .2, emi: .5 }), ix.length, pai) : null;
    ix.forEach((i, j) => { const p = P[i], r = o.r ? o.r(i) : p.length > 3 ? [p[3], p[4], p[5]] : giro(), e = s * ri(es[0], es[1]);
      poeInst(im, j, p, r, e, pega(cores)); if (tp) { im.getMatrixAt(j, _m); tp.setMatrixAt(j, _m.multiply(_t)); corInst(tp, j, pega(CORES.tampa)); } });
    im.userData.base = ix.map((i, j) => { const b = new THREE.Matrix4(); im.getMatrixAt(j, b); return b; }); im.userData.ordem = ix; lotes.push(im);
    if (tp) { tp.userData.base = ix.map((i, j) => { const b = new THREE.Matrix4(); tp.getMatrixAt(j, b); return b; }); tp.userData.ordem = ix; lotes.push(tp); }
  }
  return lotes;
}
const _c = new THREE.Color();
function corInst(im, i, cor) { const h = parseInt(cor.slice(1), 16); im.setColorAt(i, _c.setRGB((h >> 16 & 255) / 255, (h >> 8 & 255) / 255, (h & 255) / 255, THREE.LinearSRGBColorSpace)); im.instanceColor.needsUpdate = true; }
// pontos de um monte (do miolo para a borda), no referencial do monte
export function pontosMonte(n, r, rz, h, y0 = .12) {
  const L = []; for (let i = 0; i < n; i++) { const u = Math.sqrt((i + .5) / n), a = i * 2.39996 + ri(-.2, .2), rr = u * ri(.9, 1.06);
    L.push([r * rr * Math.cos(a), y0 + h * (1 - u * u) ** .8 * rng() ** .7, rz * rr * Math.sin(a)]); }
  return L;
}
const NPAD = { latinha: 220, pet: 150, ferro: 80, papelao: 46, cobre: 70, aluminio: 70, plastico: 90, bateria: 26, misto: 110 };
export function monte(pai, pos = [0, 0, 0], o = {}) {
  const tipo = o.tipo ?? 'latinha', r = o.r ?? 1.5, rz = o.rz ?? r * .78, h = o.h ?? .95, g = grupo(pai, pos), s = o.s ?? 1;
  if (o.mancha !== false) mancha(2 * r + 1.6, 2 * rz + 1.5, [0, 0, .1], { pai: g, op: .8 });
  const P = pontosMonte(o.n ?? NPAD[tipo] ?? 100, r, rz, h, tipo === 'ferro' ? .06 : .12 * s);
  g.userData = { lotes: pecas(g, tipo, P, { s, tipos: o.tipos }), h, r, tipo, topo: [0, h + .75, 0] }; return g;
}
// cai: as peças do monte (ou de pecas()) caem no lugar, uma atrás da outra, com um quique curto. p de 0 a 1 no intervalo
// [a, a + d]; antes de a o monte não existe. alvo = monte (grupo) ou lista de lotes.
export function cai(alvo, t, a, o = {}) {
  const lotes = alvo.userData?.lotes ?? alvo, d = o.d ?? 1.1, q = o.queda ?? .42, alt = o.alt ?? 2.4, n = Math.max(...lotes.map(l => Math.max(...l.userData.ordem))) + 1;
  for (const im of lotes) { const B = im.userData.base;
    for (let j = 0; j < B.length; j++) { const u = (t - a - (d - q) * im.userData.ordem[j] / n) / q, x = cl(u);
      _m.copy(B[j]); if (x < 1) _m.elements[13] += alt * (1 - x * x) + (x <= 0 ? 1e4 : 0); else _m.elements[13] += .06 * Math.abs(golpe(cl((u - 1) * q / .3), 1, 3));
      im.setMatrixAt(j, _m); }
    im.instanceMatrix.needsUpdate = true; }
}
// baterias em lote (caixa escura, tampa, faixa âmbar e os dois polos): P = [x, y (base), z, giro em y, tombo]
const BG = () => (G.bat ??= [caixa(.36, .2, .22, .028), caixa(.37, .04, .23, .014), cil(.028, .05, 10), caixa(.3, .07, .008, .003)]);
export function bateriasLote(pai, P, s = 1) {
  const [gb, gt, gp, gf] = BG(), n = P.length, b = lote(gb, mat('#2F3640', { bri: .16, emi: .9 }), n, pai), tp = lote(gt, mat('#566270', { bri: .2, emi: .8 }), n, pai),
    po = lote(gp, mat('#FFFFFF', { bri: .3, emi: .9 }), 2 * n, pai), fx = lote(gf, mat('#F2B63D', { emi: 1, bri: .1 }), n, pai), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), S = new THREE.Vector3(s, s, s);
  const poe = (im, i, base, dx, dy, dz) => { v.set(dx * s, dy * s, dz * s).applyQuaternion(q).add(base); im.setMatrixAt(i, _m.compose(v, q, S)); };
  P.forEach(([x, y, z, ry = 0, rz = 0], i) => { e.set(0, ry, rz); q.setFromEuler(e); const base = new THREE.Vector3(x, y, z);
    poe(b, i, base, 0, .1, 0); poe(tp, i, base, 0, .215, 0); poe(fx, i, base, 0, .1, .112); poe(po, 2 * i, base, -.11, .255, 0); poe(po, 2 * i + 1, base, .11, .255, 0);
    corInst(po, 2 * i, '#E5574A'); corInst(po, 2 * i + 1, '#C9D1DA'); });
  const L = [b, tp, po, fx]; L.forEach((im, k) => { im.instanceMatrix.needsUpdate = true; const m = k === 2 ? 2 : 1;
    im.userData.base = [...Array(im.count)].map((_, j) => { const B = new THREE.Matrix4(); im.getMatrixAt(j, B); return B; }); im.userData.ordem = [...Array(im.count)].map((_, j) => Math.floor(j / m)); });
  return L;
}
