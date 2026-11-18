// A mesma cena em 3D (three.js local, CPU): caminhão carregado sobre a balança rodoviária e o poste do visor, com as medidas do
// kit da trilha (perfis/ecoflix/cenas3d/kit3d.js). O estilo entra por fora: est.mat(cor, tipo) dá o material, est.caixa/est.seg
// dão o acabamento da forma (canto vivo, chanfro ou arredondado) e est.contorno liga o traço (casca invertida).
import * as THREE from '../../../perfis/ecoflix/cenas3d/three.module.min.js';
import { sorteio, LG, AL, CORES_LATA } from './comum.js';
export { THREE };
export const PI = Math.PI;
export const COR = { verde: '#50D088', cinzaE: '#2F353C', vidro: '#CFE0EA', farol: '#FFF4DA', ambar: '#F2B63D', bau: '#98A2AD', aco: '#7E8995', pneu: '#23282E', aro: '#C9D1DA',
  deck: '#8E98A3', deckTopo: '#B9C1CA', rampa: '#C5CCD4', poste: '#AEB7C1', ferrugem: '#A8603A', chapa: '#5F6B77' };

// caixa de canto arredondado (seg >= 2) ou chanfrado (seg 1); r 0 = caixa viva
export function rbox(w, h, d, r = .04, seg = 2) {
  r = Math.min(r, w / 2 - .001, h / 2 - .001, d / 2 - .001); if (!(r > .002)) return new THREE.BoxGeometry(w, h, d);
  const s = new THREE.Shape(), x = w / 2 - r, y = h / 2 - r;
  s.moveTo(-x, -y); s.lineTo(x, -y); s.lineTo(x, y); s.lineTo(-x, y); s.closePath();
  const g = new THREE.ExtrudeGeometry(s, { depth: d - 2 * r, bevelEnabled: true, bevelThickness: r, bevelSize: r, bevelSegments: seg, curveSegments: 1 });
  g.translate(0, 0, -(d - 2 * r) / 2); return g;
}
// normais médias por posição (atributo aN): a casca do contorno abre sem rasgar nas quinas
function suaves(g) {
  const p = g.attributes.position, n = g.attributes.normal, m = new Map(), o = new Float32Array(p.count * 3), k = i => `${Math.round(p.getX(i) * 500)},${Math.round(p.getY(i) * 500)},${Math.round(p.getZ(i) * 500)}`;
  for (let i = 0; i < p.count; i++) { const c = k(i), v = m.get(c) || [0, 0, 0]; v[0] += n.getX(i); v[1] += n.getY(i); v[2] += n.getZ(i); m.set(c, v); }
  for (let i = 0; i < p.count; i++) { const v = m.get(k(i)), l = Math.hypot(...v) || 1; o.set([v[0] / l, v[1] / l, v[2] / l], i * 3); }
  g.setAttribute('aN', new THREE.BufferAttribute(o, 3));
}
export function casca(raiz, esp = .03, cor = '#161618') {
  const m = new THREE.ShaderMaterial({ side: THREE.BackSide, uniforms: { e: { value: esp }, c: { value: new THREE.Color(cor) } },
    vertexShader: 'attribute vec3 aN;uniform float e;void main(){vec4 v=modelViewMatrix*vec4(position,1.);v.xyz+=normalize(normalMatrix*aN)*e;gl_Position=projectionMatrix*v;}',
    fragmentShader: 'uniform vec3 c;void main(){gl_FragColor=vec4(c,1.);\n#include <colorspace_fragment>\n}' });
  const L = []; raiz.traverse(o => { if (o.isMesh && !o.userData.semCasca) L.push(o); });
  for (const o of L) { if (!o.geometry.attributes.aN) suaves(o.geometry); const h = new THREE.Mesh(o.geometry, m); h.userData.casca = true; o.add(h); }
}

// est: { mat(cor, tipo), r (raio do canto), seg (segmentos do canto), nr (lados da roda), carga: 'lata' | 'bloco', moldura (vidros com aro escuro) }
export function cena3d(est) {
  const rnd = sorteio(est.semente ?? 11), ri = (a, b) => a + (b - a) * rnd();
  const raiz = new THREE.Group(), mc = {};
  const M = (c, tipo = '') => mc[c + tipo] || (mc[c + tipo] = est.mat(c, tipo));
  const poe = (g, m, pai, p = [0, 0, 0], r = [0, 0, 0]) => { const o = new THREE.Mesh(g, m); o.position.set(...p); o.rotation.set(...r); o.castShadow = o.receiveShadow = true; pai.add(o); return o; };
  const cx = (w, h, d, c, pai, p, r, o = {}) => poe(rbox(w, h, d, o.r ?? est.r ?? 0, est.seg ?? 2), M(c, o.tipo), pai, p, r);
  const cil = (r1, r2, h, n) => new THREE.CylinderGeometry(r1, r2, h, n);
  const nr = est.nr ?? 26;
  // ---- balança: tampo, frisos, rampas, poste
  const bc = est.bc ?? 7.4, bl = 3.0, rp = est.rampa ?? .9, bh = .172, bal = new THREE.Group(); raiz.add(bal);
  cx(bc, .16, bl, COR.deck, bal, [0, .08, 0], undefined, { r: Math.min(est.r ?? 0, .05) });
  poe(new THREE.BoxGeometry(bc - .14, .02, bl - .14), M(COR.deckTopo), bal, [0, .163, 0]).userData.semCasca = true;
  if (est.frisos !== false) { const n = Math.floor((bc - .6) / .4) + 1; for (let i = 0; i < n; i++) poe(new THREE.BoxGeometry(.04, .012, bl - .3), M('#A5AEB8'), bal, [(i - (n - 1) / 2) * .4, .176, 0]).userData.semCasca = true; }
  const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(rp, 0); sh.lineTo(rp, bh); sh.closePath();
  for (const s of [-1, 1]) { const rg = new THREE.ExtrudeGeometry(sh, { depth: bl - .2, bevelEnabled: false }); rg.translate(0, 0, -(bl - .2) / 2); if (s > 0) rg.rotateY(PI);
    poe(rg, M(COR.rampa), bal, [s * (bc / 2 + rp), 0, 0]); }
  const [px, pz] = est.poste ?? [bc / 2 + .35, -1.9], hp = est.hp ?? 3.25;
  cx(.5, .06, .5, '#9AA3AD', bal, [px, .03, pz]); poe(cil(.07, .08, hp, est.np ?? 14), M(COR.poste), bal, [px, hp / 2 + .03, pz]);
  // ---- caminhão
  const c = 6.6, Wd = 2.3, R = .46, ww = .34, cc = 1.85, hc = 1.7, y0 = 2 * R + .06, bt = est.r ? .06 : 0, T = new THREE.Group(); T.position.set(est.tx ?? 0, bh + .012, 0); raiz.add(T);
  cx(c - .45, .26, Wd * .44, COR.cinzaE, T, [-.05, R + .2, 0]);
  for (const x of [c / 2 - .95, -c / 2 + 1.0, -c / 2 + 2.0]) for (const s of [-1, 1]) { const z = s * (Wd / 2 - ww / 2 - .03), k = est.r ? .08 : 0;
    const pn = est.r ? new THREE.LatheGeometry([[R * .6, -ww / 2], [R - k, -ww / 2], [R - k * .3, -ww / 2 + k * .3], [R, -ww / 2 + k], [R, ww / 2 - k], [R - k * .3, ww / 2 - k * .3], [R - k, ww / 2], [R * .6, ww / 2]].map(v => new THREE.Vector2(...v)), nr) : cil(R, R, ww, nr);
    poe(pn, M(COR.pneu), T, [x, R, z], [PI / 2, 0, 0]); poe(cil(R * .6, R * .6, ww * (est.r ? .86 : 1.05), nr), M(COR.aro), T, [x, R, z], [PI / 2, 0, 0]).userData.semCasca = true;
    poe(cil(R * .2, R * .2, ww * (est.r ? .95 : 1.1), Math.min(nr, 12)), M(COR.cinzaE), T, [x, R, z], [PI / 2, 0, 0]).userData.semCasca = true; }
  poe(cil(.2, .2, .8, Math.min(nr, 16)), M(COR.aro), T, [c / 2 - cc - .55, R + .1, Wd / 2 - .32], [0, 0, PI / 2]);
  cx(cc - .1, y0 - R - .3, Wd - 2 * ww - .25, COR.cinzaE, T, [c / 2 - cc / 2, (R + .33 + y0) / 2, 0]);
  cx(.2, .3, Wd + .04, COR.cinzaE, T, [c / 2 + .06, R + .32, 0]);
  const cab = new THREE.Group(); cab.position.set(c / 2 - cc / 2, y0, 0); T.add(cab);
  const perfil = new THREE.Shape([[0, 0], [cc, 0], [cc, hc * .56], [cc - .3, hc * .93], [cc - .44, hc], [0, hc]].map(v => new THREE.Vector2(...v)));
  const eg = new THREE.ExtrudeGeometry(perfil, { depth: Wd - 2 * bt, bevelEnabled: bt > 0, bevelThickness: bt, bevelSize: bt, bevelSegments: est.seg === 1 ? 1 : 3, curveSegments: 1 });
  eg.translate(-cc / 2, 0, -(Wd - 2 * bt) / 2); poe(eg, M(COR.verde, 'cab'), cab);
  const th = Math.atan2(.3, .37 * hc), Ls = Math.hypot(.3, .37 * hc), dec = [];
  const placa = (w, h, d, cor, p, r, tipo) => { const o = poe(new THREE.BoxGeometry(w, h, d), M(cor, tipo), cab, p, r); o.userData.semCasca = true; dec.push([o, w, h, d]); return o; };
  placa(.03, Ls * .8, Wd - .44, COR.vidro, [cc / 2 - .15 + Math.cos(th) * (bt + .012), hc * .745 + Math.sin(th) * (bt + .012), 0], [0, 0, th], 'vidro');
  placa(.03, hc * .24, Wd * .46, COR.cinzaE, [cc / 2 + bt + .006, hc * .3, 0]);
  for (const s of [-1, 1]) {
    placa(.7, hc * .29, .03, COR.vidro, [cc / 2 - .66, hc * .73, s * (Wd / 2 + .006)], undefined, 'vidro');
    placa(.03, .14, .3, COR.farol, [cc / 2 + bt + .006, hc * .2, s * (Wd / 2 - .34)], undefined, 'luz');
    placa(.03, .12, .12, COR.ambar, [cc / 2 + bt + .006, hc * .2, s * (Wd / 2 - .12)], undefined, 'luz');
    cx(.2, .04, .04, COR.cinzaE, cab, [cc / 2 - .12, hc * .68, s * (Wd / 2 + .1)], undefined, { r: 0 });
    cx(.06, .32, .13, '#161618', cab, [cc / 2 - .02, hc * .62, s * (Wd / 2 + .2)], undefined, { r: .02 });
  }
  if (est.moldura) for (const [o, w, h, d] of dec) { const e = .045, m = poe(new THREE.BoxGeometry(w < .05 ? w * .6 : w + 2 * e, h + 2 * e, d < .05 ? d * .6 : d + 2 * e), M('#161618', 'traco'), cab, o.position.toArray(), [o.rotation.x, o.rotation.y, o.rotation.z]); m.userData.semCasca = true; m.castShadow = false; }
  const cb = c - cc - .32, hb = .9, x0 = -c / 2 + .04, B = new THREE.Group(); B.position.set(x0, y0 - .04, 0); T.add(B);
  cx(cb - .3, .15, Wd * .5, COR.cinzaE, T, [x0 + cb / 2, R + .33 + .075, 0]);
  cx(cb, .1, Wd, COR.bau, B, [cb / 2, .05, 0]);
  for (const s of [-1, 1]) { cx(cb, hb, .08, COR.bau, B, [cb / 2, .1 + hb / 2, s * (Wd / 2 - .04)], undefined, { r: Math.min(est.r ?? 0, .02) });
    cx(cb + .04, .08, .14, COR.aco, B, [cb / 2, .1 + hb, s * (Wd / 2 - .04)], undefined, { r: Math.min(est.r ?? 0, .03) });
    for (let i = 1; i < 5; i++) cx(.08, hb - .06, .06, COR.aco, B, [i * cb / 5, .1 + hb / 2, s * (Wd / 2 + .012)], undefined, { r: 0 }).userData.semCasca = true; }
  cx(.09, hb + .3, Wd, COR.bau, B, [cb - .045, .1 + (hb + .3) / 2, 0], undefined, { r: Math.min(est.r ?? 0, .02) });
  cx(.09, hb, Wd - .02, COR.aco, B, [.045, .1 + hb / 2, 0], undefined, { r: Math.min(est.r ?? 0, .02) });
  // ---- carga: monte de latinha e ferro acima da borda da caçamba
  const rx = cb / 2 - .2, rz = Wd / 2 - .2, alt = (x, z) => .1 + hb + (est.monte ?? .42) * (1 - x ** 4) * (1 - z ** 4);
  const bloco = est.carga === 'bloco', nL = est.nLata ?? 170, gL = bloco ? cil(.13, .13, .34, 6) : cil(.1, .1, .28, est.nlata ?? 12);
  cx(cb - .3, hb * .9, Wd - .3, '#77818C', B, [cb / 2, .1 + hb * .5, 0], undefined, { r: 0 }).userData.semCasca = true;   // enchimento (o monte não fica oco)
  for (let i = 0; i < nL; i++) { const x = ri(-1, 1), z = ri(-1, 1), y = alt(x, z) - ri(0, .3);
    const cor = rnd() < .34 ? '#DDE3E9' : CORES_LATA[Math.floor(rnd() * CORES_LATA.length)];
    poe(gL, M(cor, 'lata'), B, [cb / 2 + x * rx, y, z * rz], [ri(0, PI), ri(0, PI), ri(0, PI)]); }
  const nF = est.nFerro ?? 14;
  for (let i = 0; i < nF; i++) { const x = ri(-.85, .85), z = ri(-.8, .8), y = alt(x, z) + ri(-.05, .1), p = [cb / 2 + x * rx, y, z * rz], r = [ri(-.35, .35), ri(0, PI), ri(-.4, .4)];
    if (i % 3 === 0) cx(ri(.9, 1.5), .1, .12, COR.ferrugem, B, p, r, { r: 0 });
    else if (i % 3 === 1) poe(cil(.1, .1, ri(.7, 1.2), bloco ? 6 : 12), M(COR.aco, 'metal'), B, p, [r[0], r[1], PI / 2 + r[2]]);
    else if (bloco) poe(new THREE.IcosahedronGeometry(ri(.2, .3), 0), M(i % 2 ? COR.chapa : COR.aco, 'metal'), B, p, r);
    else cx(ri(.5, .8), .05, ri(.35, .6), COR.chapa, B, p, r, { r: 0 }); }
  return { raiz, T, bal, topoPoste: [px, hp + .03, pz], topoCarga: [T.position.x + x0 + cb / 2, T.position.y + y0 + hb + (est.monte ?? .42) + .62, 0] };
}

// palco: tela 3D do tamanho do painel (2x por dentro), câmera em órbita no alvo; devolve tela(p) → px do painel
export function palco3d(o = {}) {
  const cv = document.createElement('canvas'); cv.id = 'gl'; (document.getElementById('ov') || {}).before ? document.getElementById('ov').before(cv) : document.body.appendChild(cv);
  const rd = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true }); rd.setPixelRatio(o.pr ?? 2); rd.setSize(LG, AL, false); rd.setClearColor(0x000000, 0);
  rd.shadowMap.enabled = true; rd.shadowMap.type = o.sombraDura ? THREE.BasicShadowMap : THREE.PCFSoftShadowMap;
  const cena = new THREE.Scene(), k = { x: .9, y: 1.1, z: 0, d: 25.8, az: .47, el: .36, oy: 0, ...(o.cam || {}) };
  const cam = o.orto ? new THREE.OrthographicCamera(-o.orto * LG / AL, o.orto * LG / AL, o.orto, -o.orto, .1, 200) : new THREE.PerspectiveCamera(o.fov ?? 26, LG / AL, .1, 300);
  const ce = Math.cos(k.el); cam.position.set(k.x + k.d * Math.sin(k.az) * ce, k.y + k.d * Math.sin(k.el), k.z + k.d * Math.cos(k.az) * ce); cam.lookAt(k.x, k.y, k.z);
  cam.setViewOffset(LG, AL, 0, k.oy, LG, AL); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  const sol = new THREE.DirectionalLight(0xffffff, o.sol ?? 2.3), L = new THREE.Vector3(...(o.luz ?? [-4.5, 9, 5.5])).normalize(), r = o.raio ?? 8;
  sol.position.copy(L).multiplyScalar(40); sol.castShadow = true; sol.shadow.mapSize.setScalar(o.mapa ?? 2048);
  Object.assign(sol.shadow.camera, { left: -r, right: r, top: r, bottom: -r, near: 1, far: 90 }); sol.shadow.bias = -.0004; sol.shadow.normalBias = .02; sol.shadow.radius = o.sombraRaio ?? 4;
  cena.add(sol, sol.target, new THREE.HemisphereLight(0xffffff, o.chaoLuz ?? 0xB9C2CB, o.hemi ?? 1.7));
  const v = new THREE.Vector3();
  return { rd, cena, cam, sol, tela: p => { v.set(...p).project(cam); return [(v.x + 1) * LG / 2, (1 - v.y) * AL / 2]; }, desenha: () => rd.render(cena, cam) };
}
