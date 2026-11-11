// EcoFlix · kit 3D de argila (three.js r170 local: ./three.module.min.js, licença MIT em three.LICENSE). Ver LEIA.md.
// Uma cena 3D é uma página com <script type="module"> que importa este arquivo e chama cena(monta): o render_cenas.cjs
// (com --allow-file-access-from-files, que o import de módulo em file:// pede) chama window.setup(dados) e window.R(t),
// a mesma API da cena 2D. A página não usa rede. O kit monta o palco (#st, a tela WebGL #gl e a camada de rótulos #ov).
// Nada de marca, de tela do app nem de dado inventado nos objetos: rótulos e números vêm da fala e do inventário da aula.
import * as THREE from './three.module.min.js';
export { THREE };

// ------------------------------------------------------------------ tempo e movimento (os do kit 2D)
export const PI = Math.PI;
export const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const eo = x => 1 - Math.pow(1 - cl(x), 3);
export const eio = x => { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
export const pr = (t, a, d = .45) => cl((t - a) / d);
export const lerp = (a, b, p) => a + (b - a) * p;
let S = 0;   // sorteio com semente (mulberry32): a cena sai igual em todo quadro e em todo render
export const semente = s => { S = s | 0; };
export const rng = () => { S = S + 0x6D2B79F5 | 0; let t = Math.imul(S ^ S >>> 15, 1 | S); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
export const ri = (a, b) => lerp(a, b, rng());
export const pega = a => a[Math.floor(rng() * a.length)];

// ------------------------------------------------------------------ ponte com a fala (dados do renderizador)
let D = null;
const norm = w => w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%./-]+/g, '');
export function W(linha, palavra, n = 1, campo = 's') {   // instante da n-ésima "palavra" da linha (campo 'e' = fim)
  const alvo = norm(palavra); let k = 0;
  for (const w of D.words) if (w.linha === linha && norm(w.w).replace(/[.,]$/, '') === alvo && ++k === n) return w[campo];
  for (const w of D.words) if (w.linha === linha && norm(w.w).startsWith(alvo) && ++k >= n) return w[campo];
  console.warn('palavra não achada', linha, palavra); return L(linha);
}
export const L = i => (D.linhas[i] || { s: 0 }).s, LE = i => (D.linhas[i] || { e: D.dur }).e;

// ------------------------------------------------------------------ palco e rótulos HTML (estilo saturado da marca)
const FT = new URL('../../../ferramentas/web/fonts/', import.meta.url).href;   // se não achar, o renderizador põe as da skill
const ff = (w, x) => `@font-face{font-family:M;font-weight:${w};src:url(${FT}montserrat-latin${x ? '-ext' : ''}-${w}-normal.woff2) format('woff2')${x ? ';unicode-range:U+0100-024F' : ''}}`;
const CSS = [500, 600, 700, 800].map(w => ff(w) + ff(w, 1)).join('') + `
:root{--v:#50D088;--ve:#2E7D57;--a:#F2B63D;--ae:#8A5A00;--t:#121212;--e:#121212;--vs:#50D088;--as:#F2B63D;--cz:#4B5563}
*{box-sizing:border-box;margin:0;padding:0;transition:none!important;animation:none!important}
html,body{width:1280px;height:800px;overflow:hidden;background:#fff}
body{font-family:M,sans-serif;color:var(--t);-webkit-font-smoothing:antialiased}
#st{position:absolute;inset:0;overflow:hidden;background:radial-gradient(1100px 650px at 92% -12%,rgba(80,208,136,.09),transparent 62%),
  radial-gradient(900px 600px at -12% 112%,rgba(80,208,136,.06),transparent 60%),#fff}
#gl{position:absolute;left:0;top:0;width:1280px;height:800px}
#ov{position:absolute;inset:0}
.ab{position:absolute}
.kick{font-weight:700;font-size:15px;letter-spacing:.3em;color:var(--ve);text-transform:uppercase}
.h{font-weight:800;font-size:46px;letter-spacing:-.01em;line-height:1.1;white-space:nowrap}
.tag{display:inline-flex;align-items:center;gap:9px;padding:9px 18px;border-radius:999px;font-weight:800;font-size:21px;
  white-space:nowrap;color:#fff;background:var(--cz);box-shadow:0 6px 16px rgba(16,24,40,.12)}
.tag.v{background:var(--vs)} .tag.a{background:var(--as)} .tag.e{background:var(--e)}
.tag.p{font-size:15px;padding:5px 13px;box-shadow:0 3px 8px rgba(16,24,40,.10)}
.sub{font-weight:600;font-size:17px;line-height:1.3;color:#4B5563;white-space:nowrap}
.selo{position:absolute;display:flex;flex-direction:column;align-items:center;gap:8px}
.col{position:absolute;width:200px;display:flex;flex-direction:column;align-items:center;gap:8px}
.op{position:absolute;width:46px;height:46px;border-radius:50%;background:var(--cz);color:#fff;display:flex;align-items:center;
  justify-content:center;font-weight:800;font-size:28px;line-height:1}
.card{position:absolute;background:#fff;border:1px solid #E1E8E4;border-radius:18px;
  box-shadow:0 18px 40px rgba(16,24,40,.10),0 3px 8px rgba(16,24,40,.06)}
.cp{width:296px;height:112px;padding:16px 20px}
.num{font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.01em;white-space:nowrap}
.most{position:absolute;width:250px;background:var(--e);border-radius:16px;padding:14px 20px 16px;box-shadow:0 16px 34px rgba(16,24,40,.22)}
.most .ml{position:relative;height:20px;font-weight:700;font-size:14px;letter-spacing:.2em;color:#A9E9C6;text-transform:uppercase}
.most .ml span{position:absolute;left:0;top:0;white-space:nowrap}
.most .mn{margin-top:6px;font-weight:800;font-size:42px;color:var(--v);font-variant-numeric:tabular-nums;white-space:nowrap}
.rip{position:absolute;width:56px;height:56px;margin:-28px 0 0 -28px;border-radius:50%;border:3px solid var(--v);opacity:0}
.ic{display:inline-flex;align-items:center;justify-content:center;flex:none}.ic svg{width:100%;height:100%}`;
export let OV = null, GL = null;   // GL: a tela 3D inteira (GL.style.opacity faz o mundo entrar sem transparência nos objetos)
{ const s = document.createElement('style'); s.textContent = CSS; document.head.prepend(s);
  document.body.insertAdjacentHTML('afterbegin', '<div id="st"><canvas id="gl" width="1280" height="800"></canvas><div id="ov"></div></div>');
  OV = document.getElementById('ov'); GL = document.getElementById('gl'); }

export function el(html, pai = OV) { const d = document.createElement('div'); d.innerHTML = html.trim(); const f = d.firstElementChild; pai.appendChild(f); return f; }
export function ic(n, px) { return `<span class="ic" style="width:${px}px;height:${px}px">${(window.ICONS || {})[n] || ''}</span>`; }   // nome literal na página
export function vis(e, t, a, b = 1e9, o = {}) {   // entra em a, sai em b (opacidade, deslize dy/dx e escala sc)
  const din = o.din ?? .5, dout = o.dout ?? .4, dy = o.dy ?? 16, dx = o.dx ?? 0, sc = o.sc ?? .985;
  const p = eo(pr(t, a, din)), q = 1 - eo(pr(t, b, dout)), op = Math.min(p, q);
  e.style.opacity = op.toFixed(4); e.style.visibility = op <= .001 ? 'hidden' : 'visible';
  const s = sc + (1 - sc) * p - (1 - q) * (1 - sc);
  e.style.transform = `translate(${((1 - p) * dx).toFixed(2)}px,${((1 - p) * dy - (1 - q) * dy * .5).toFixed(2)}px) scale(${s.toFixed(4)})`;
  return op;
}
export function ripple(r, t, a) { const p = pr(t, a, .7); r.style.opacity = (p > 0 && p < 1) ? (.6 * (1 - p)).toFixed(3) : 0; r.style.transform = `scale(${(.4 + 2.0 * eo(p)).toFixed(3)})`; }
export function pulse(e, t, a, amp = .045, dur = .9) { const p = pr(t, a, dur); e.style.scale = (p > 0 && p < 1) ? (1 + amp * Math.sin(PI * p)).toFixed(4) : ''; }
const NF = new Intl.NumberFormat('pt-BR'), NF1 = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 1 });
export const kg = v => NF.format(Math.round(v)) + ' kg', kgd = v => NF1.format(Math.round(v * 10) / 10) + ' kg';
export function conta(e, t, a, d, v0, v1, fmt = kg) { const s = fmt(lerp(v0, v1, eo(pr(t, a, d)))); if (e.textContent !== s) e.textContent = s; }
export function posTitulo(e, t, a, sobe, sai = 1e9) {   // título grande no meio que sobe quando o desenho entra
  vis(e, t, a, sai, { dy: 14 }); const p = eio(pr(t, sobe, .7));
  e.style.top = lerp(318, 46, p).toFixed(2) + 'px'; e.style.scale = lerp(1.12, 1, p).toFixed(4);
}
export function titulo(kick, ...hs) {   // chamada + um ou mais títulos no mesmo lugar (troca com vis em cada e.hs[i])
  const e = el(`<div class="ab" style="left:0;top:0;width:1280px;text-align:center"><div class="kick">${kick}</div>
    <div style="position:relative;height:51px;margin-top:12px">${hs.map(h => `<div class="h ab" style="left:0;width:1280px">${h}</div>`).join('')}</div></div>`);
  e.hs = [...e.querySelectorAll('.h')]; return e;
}
// selo (etiqueta cheia + legenda embaixo), chip (etiqueta pequena), coluna da conta, operador, cartão de número, onda
export const selo = (cls, txt, sub = '') => el(`<div class="selo"><div class="tag ${cls}">${txt}</div>${sub ? `<div class="sub">${sub}</div>` : ''}</div>`);
export const chip = (txt, cls = '') => el(`<div class="tag p ab ${cls}">${txt}</div>`);
export const coluna = (cx, y, cls, txt, sub) => el(`<div class="col" style="left:${cx - 100}px;top:${y}px"><div class="tag ${cls}">${txt}</div><div class="sub" style="font-size:16px">${sub}</div></div>`);
export const op = (cx, y, s) => el(`<div class="op" style="left:${cx - 23}px;top:${y}px">${s}</div>`);
export const onda = (pai, x, y) => el(`<div class="rip" style="left:${x}px;top:${y}px"></div>`, pai);
export function cartao(x, y, cls, rot, sub, v, o = {}) {   // o.res: cartão do resultado (contorno verde); o.fmt: kg ou kgd
  return el(`<div class="card cp" style="left:${x}px;top:${y}px;${o.w ? `width:${o.w}px;` : ''}${o.res ? 'border:2px solid var(--v);background:#F4FBF7' : ''}">
    <div style="display:flex;align-items:center;gap:10px"><div class="tag p ${cls}" style="font-size:16px">${rot}</div><div class="sub" style="font-size:16px">${sub}</div></div>
    <div class="num" style="margin-top:10px;font-size:36px;${o.res ? 'color:var(--ve)' : ''}">${(o.fmt || kg)(v)}</div></div>`);
}
export function mostrador(r1, r2 = '', w = 250) {   // painel escuro com o número verde; e.troca(t, a) passa do rótulo 1 ao 2
  const e = el(`<div class="most" style="width:${w}px"><div class="ml"><span class="m1">${r1}</span><span class="m2">${r2}</span></div><div class="mn">0 kg</div></div>`);
  e.mn = e.querySelector('.mn'); e.m1 = e.querySelector('.m1'); e.m2 = e.querySelector('.m2');
  e.troca = (t, a) => { const p = eo(pr(t, a, .35)); e.m1.style.opacity = 1 - p; e.m2.style.opacity = p; };
  e.troca(0, 1e9); return e;
}

// ------------------------------------------------------------------ 3D: palco, luz, sombra macia e câmera
const Q = new URLSearchParams(location.search);   // variantes de custo (aa=0, sm=2048, st=pcf|vsm, pr=1, sh=0, mt=l, rs=1)
export let RD = null, CENA = null, CAM = null, SOL = null, CHAO = null;
const OPC = { sombra: 6.5, mapa: 1024, fov: 26, chao: true, aquece: [] };
const LUZ = new THREE.Vector3(-4.5, 9, 5.5).normalize();
function base() {
  if (!RD) {   // 3D a 1,5x no máximo (1920x1200); os rótulos HTML ficam na resolução cheia
    RD = new THREE.WebGLRenderer({ canvas: GL, antialias: Q.get('aa') !== '0', alpha: true, preserveDrawingBuffer: true });
    RD.setPixelRatio(Math.min(window.devicePixelRatio || 1, +(Q.get('pr') || 1.5))); RD.setSize(1280, 800, false); RD.setClearColor(0x000000, 0);
    RD.shadowMap.enabled = Q.get('sh') !== '0';
    RD.shadowMap.type = { pcf: THREE.PCFShadowMap, vsm: THREE.VSMShadowMap }[Q.get('st')] ?? THREE.PCFSoftShadowMap;
  }
  CENA = new THREE.Scene(); CAM = new THREE.PerspectiveCamera(OPC.fov, 1280 / 800, .1, 300);
  CENA.add(new THREE.HemisphereLight(0xffffff, 0xB9C2CB, 1.7));
  SOL = new THREE.DirectionalLight(0xffffff, 2.3); SOL.castShadow = true; SOL.shadow.mapSize.setScalar(+(Q.get('sm') || OPC.mapa));
  const r = OPC.sombra, sc = SOL.shadow.camera; sc.left = sc.bottom = -r; sc.right = sc.top = r; sc.near = 1; sc.far = 6 * r + 40;
  SOL.shadow.bias = -.0004; SOL.shadow.normalBias = .02; SOL.shadow.radius = 4; SOL.shadow.blurSamples = 8; CENA.add(SOL, SOL.target);
  const fill = new THREE.DirectionalLight(0xEAF4FF, .55); fill.position.set(6, 3, 8); CENA.add(fill);
  // chão invisível que só recebe sombra (o quadrado que o mapa de sombra cobre, seguindo o alvo da câmera)
  CHAO = new THREE.Mesh(new THREE.PlaneGeometry(2 * r + 1, 2 * r + 1), new THREE.ShadowMaterial({ color: 0x1d2b24, opacity: .16 }));
  CHAO.rotation.x = -PI / 2; CHAO.receiveShadow = true; CHAO.visible = OPC.chao; CENA.add(CHAO);
}
// câmera: chaves [t, {x,y,z (alvo), d (distância), az, el (radianos), oy (px; positivo sobe o desenho)}, 'eio'|'lin', arco]
let CK = [[0, { x: 0, y: 0, z: 0, d: 12, az: 0, el: .35, oy: 0 }]];
export const camera = ck => { CK = ck; };
export function pose(t) {
  let k = CK[0][1];
  if (t > CK[0][0]) for (let i = 1; i < CK.length; i++) {
    const [t1, p1, modo, arco] = CK[i], [t0, p0] = CK[i - 1];
    if (t <= t1) { const q0 = (t - t0) / (t1 - t0), q = modo === 'lin' ? q0 : eio(q0); k = {};
      for (const c in p0) k[c] = lerp(p0[c], p1[c], q); if (arco) k.d += arco * Math.sin(PI * q); return k; }
    k = p1;
  }
  return k;
}
function aplicaCam(k) {
  const ce = Math.cos(k.el), dl = 2 * OPC.sombra + 6;
  CAM.position.set(k.x + k.d * Math.sin(k.az) * ce, k.y + k.d * Math.sin(k.el), k.z + k.d * Math.cos(k.az) * ce); CAM.lookAt(k.x, k.y, k.z);
  CAM.setViewOffset(1280, 800, 0, k.oy, 1280, 800); CAM.updateMatrixWorld();
  SOL.position.set(k.x + LUZ.x * dl, LUZ.y * dl, k.z + LUZ.z * dl); SOL.target.position.set(k.x, 0, k.z); SOL.target.updateMatrixWorld();
  CHAO.position.set(k.x, 0, k.z);
}
const _v = new THREE.Vector3();
export function tela(p) { _v.set(p[0], p[1], p[2]).project(CAM); return [(_v.x + 1) * 640, (1 - _v.y) * 400]; }   // mundo → px
// prende um rótulo HTML a um ponto do mundo (ax/ay: que ponto do rótulo fica no ponto; dx/dy em px)
export function ancora(e, p, ax = .5, ay = 1, dx = 0, dy = 0) {
  if (e._w == null) { e._w = e.offsetWidth; e._h = e.offsetHeight; } const [x, y] = tela(p);
  e.style.left = (x - e._w * ax + dx).toFixed(1) + 'px'; e.style.top = (y - e._h * ay + dy).toFixed(1) + 'px';
}
export function mundo(o, p) { o.updateWorldMatrix(true, false); _v.set(p[0], p[1], p[2]); o.localToWorld(_v); return [_v.x, _v.y, _v.z]; }
// a cena: monta(dados) devolve a função do tempo; o = opções (sombra: meia largura coberta, mapa, fov, chao, aquece, semente)
let RENDER = null;
export function cena(monta, o = {}) {
  window.setup = d => { D = d; Object.assign(OPC, typeof o === 'function' ? o(d) : o); OV.innerHTML = ''; base(); semente(OPC.semente ?? 20261111);
    camera([[0, { x: 0, y: 0, z: 0, d: 12, az: 0, el: .35, oy: 0 }]]); RENDER = monta(d);
    for (const t of OPC.aquece) quadro(t); quadro(0); return true; };
  window.R = t => { quadro(t); return true; };
}
function quadro(t) { aplicaCam(pose(t)); RENDER(t); RD.render(CENA, CAM); }

// ------------------------------------------------------------------ 3D: argila na paleta da marca
export const COR = { verde: '#50D088', verdeE: '#2E7D57', escuro: '#121212', ambar: '#F2B63D', ambarE: '#C98A26', argila: '#DEE3E8',
  cinza: '#8E98A3', cinzaC: '#B9C1CA', cinzaE: '#2F353C', pneu: '#23282E', aro: '#AEB7C1', vidro: '#CFE0EA', farol: '#FFF4DA',
  aco: '#7E8995', alu: '#C9D1DA', cobre: '#C8703A', madeira: '#C9A27A', madeiraE: '#B48C64', rafia: '#E9D6AC', rafiaE: '#B89A62',
  concreto: '#EBEEF1', junta: '#DCE1E6', papel: '#FBFBF7', tela: '#EAF8F0' };
const MAT = o => { if (Q.get('mt') === 'l') { delete o.roughness; delete o.metalness; return new THREE.MeshLambertMaterial(o); } return new THREE.MeshStandardMaterial(o); };
const MC = {};
export function M(c, o = {}) {   // material fosco reaproveitado (argila: rugosidade alta, sem metal); f = facetado, ds = dois lados
  const k = c + (o.f ? 'f' : '') + (o.ds ? 'd' : '') + (o.r ?? '');
  return MC[k] || (MC[k] = MAT({ color: c, roughness: o.r ?? .86, metalness: 0, flatShading: !!o.f, side: o.ds ? THREE.DoubleSide : THREE.FrontSide }));
}
export const MU = (c, o = {}) => MAT({ color: c, roughness: o.r ?? .88, metalness: 0, side: o.ds ? THREE.DoubleSide : THREE.FrontSide });
export const ARGILA = { verde: M(COR.verde), escuro: M(COR.escuro), ambar: M(COR.ambar) };   // as três cores da marca
export const ARG = new THREE.Color(COR.argila);   // argila crua
export function argila(g) {   // o objeto ganha materiais próprios para tinge(g, p): argila crua (0) → cor dele (1)
  const L = []; g.traverse(o => { if (o.isMesh && !o.isInstancedMesh && (o.material.isMeshStandardMaterial || o.material.isMeshLambertMaterial)) {
    o.material = o.material.clone(); L.push([o.material, o.material.color.clone()]); } });
  g.userData.tinta = L; return g;
}
export function tinge(g, p) { for (const [m, c] of g.userData.tinta) m.color.copy(ARG).lerp(c, p); }

// ------------------------------------------------------------------ 3D: utilidades de forma e de movimento
export function poe(g, m, pai, p = [0, 0, 0], r = [0, 0, 0], s = 1) {
  const o = new THREE.Mesh(g, m); o.position.set(...p); o.rotation.set(...r);
  if (Array.isArray(s)) o.scale.set(...s); else o.scale.setScalar(s); o.castShadow = o.receiveShadow = true; pai.add(o); return o;
}
export function grupo(pai, p = [0, 0, 0]) { const g = new THREE.Group(); g.position.set(...p); pai.add(g); return g; }
export const torno = (pts, n) => new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), n);
// caixa de cantos arredondados (o RoundedBoxGeometry dos exemplos do three, sem addon)
export function rbox(w, h, d, r = .04, seg = 2) {
  seg = seg * 2 + 1; r = Math.min(w / 2, h / 2, d / 2, r);
  const g = new THREE.BoxGeometry(1, 1, 1, seg, seg, seg).toNonIndexed(), P = g.attributes.position.array, N = g.attributes.normal.array;
  const bx = w / 2 - r, by = h / 2 - r, bz = d / 2 - r, hs = .5 / seg, n = new THREE.Vector3();
  for (let i = 0; i < P.length; i += 3) { const x = P[i], y = P[i + 1], z = P[i + 2];
    n.set(x - Math.sign(x) * hs, y - Math.sign(y) * hs, z - Math.sign(z) * hs).normalize();
    P[i] = bx * Math.sign(x) + n.x * r; P[i + 1] = by * Math.sign(y) + n.y * r; P[i + 2] = bz * Math.sign(z) + n.z * r; N[i] = n.x; N[i + 1] = n.y; N[i + 2] = n.z; }
  g.deleteAttribute('uv'); return g;
}
let TXS = null;   // sombra de contato: mancha macia no chão, por baixo da sombra da luz
export function mancha(pai, w, d, op = .3, p = [0, 0, 0]) {
  if (!TXS) { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.5, 'rgba(255,255,255,.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 128, 128); TXS = new THREE.CanvasTexture(c); }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshBasicMaterial({ map: TXS, color: 0x1d2b24, transparent: true, opacity: op, depthWrite: false }));
  m.rotation.x = -PI / 2; m.position.set(p[0], .004, p[2]); m.renderOrder = 1; m.userData.op = op; pai.add(m); return m;
}
export function anel(pai, r, w = .07, p = [0, 0, 0]) {   // anel verde no chão (destaque); um segundo anel faz a onda
  const m = new THREE.Mesh(new THREE.RingGeometry(r - w / 2, r + w / 2, 72), new THREE.MeshBasicMaterial({ color: 0x50D088, transparent: true, opacity: 0, depthWrite: false }));
  m.rotation.x = -PI / 2; m.position.set(p[0], p[1] + .008, p[2]); m.renderOrder = 2; pai.add(m); return m;
}
export function destaque(an, onda3, t, a) {
  const p = eo(pr(t, a, .45)); an.material.opacity = .95 * p; an.visible = p > 0; an.scale.setScalar(lerp(.85, 1, p));
  const q = pr(t, a + .05, .9); onda3.visible = q > 0 && q < 1; onda3.material.opacity = .7 * (1 - q); onda3.scale.setScalar(1 + .7 * eo(q));
}
// entrada de um objeto: cresce do chão (escala) com um leve giro; nada de pulo. userData.s = escala base, userData.ry = giro base
export function cresce(o, t, a, d = .6, giro = .35) {
  const p = eo(pr(t, a, d)), s = o.userData.s ?? 1; o.visible = p > 0; o.scale.setScalar(Math.max(1e-4, p) * s);
  o.rotation.y = (o.userData.ry ?? 0) - giro * (1 - p); return p;
}
export function pulso(o, t, a, amp = .07, dur = .7) { const p = pr(t, a, dur); if (p > 0 && p < 1) o.scale.multiplyScalar(1 + amp * Math.sin(PI * p)); }
// pontos de um monte: domo de raio rx/rz e altura h, mais perto da superfície (o miolo não aparece)
export function domo(n, rx, rz, h, y0 = 0, sup = .45) {
  const P = []; for (let i = 0; i < n; i++) { const a = rng() * 2 * PI, u = Math.sqrt(rng()), top = h * Math.pow(1 - u * u, .8);
    P.push([Math.cos(a) * u * rx, y0 + top * (sup + (1 - sup) * rng()) + .03, Math.sin(a) * u * rz]); } return P;
}

// ------------------------------------------------------------------ 3D: peças de sucata e de impureza (genéricas)
const GEO = {
  tubo: new THREE.CylinderGeometry(.042, .042, .46, 12), bobina: new THREE.TorusGeometry(.1, .032, 8, 18), chapa: rbox(.32, .035, .24, .012, 1),
  bloco: new THREE.DodecahedronGeometry(.12, 0), lata: new THREE.CylinderGeometry(.05, .05, .14, 14), perfil: rbox(.52, .055, .055, .014, 1),
  terra: new THREE.DodecahedronGeometry(.075, 0), pneu: new THREE.TorusGeometry(.12, .045, 8, 14, PI * 1.1), mangueira: new THREE.CylinderGeometry(.03, .03, .32, 10),
  caco: rbox(.17, .014, .11, .006, 1), garrafa: new THREE.CylinderGeometry(.045, .05, .17, 12), pino: new THREE.CylinderGeometry(1, 1, 1, 8) };
export const PAL = { cobre: ['#C8703A', '#B45F2D', '#D98C58'], alu: ['#C9D1DA', '#AFB9C4', '#DDE3E9'], aco: ['#7E8995', '#646F7B', '#8F99A4'],
  ferrugem: ['#9A5B3A', '#86513A', '#A86A48'], terra: ['#7A5233', '#8B6240', '#6A4529'], borracha: ['#22272E', '#2E343C'], plastico: ['#4F8EDC', '#E6EEF7', '#3E7BC6'] };
const TIPOS = { cobre: ['tubo', 'bobina', 'bloco', 'tubo', 'bobina'], alu: ['lata', 'perfil', 'chapa', 'lata'], aco: ['chapa', 'bloco', 'perfil', 'chapa'],
  ferrugem: ['bloco', 'chapa', 'perfil'], terra: ['terra'], borracha: ['pneu', 'mangueira'], plastico: ['caco', 'caco', 'garrafa'] };
function giro(k) {
  if (k === 'tubo' || k === 'mangueira' || k === 'garrafa') return [ri(-.4, .4), ri(0, 2 * PI), PI / 2 + ri(-.4, .4)];
  if (k === 'bobina' || k === 'pneu') return [PI / 2 + ri(-.5, .5), ri(0, 2 * PI), ri(-.4, .4)];
  if (k === 'bloco' || k === 'terra') return [ri(0, 2 * PI), ri(0, 2 * PI), ri(0, 2 * PI)];
  if (k === 'lata') return [ri(-.4, .4) + (rng() < .5 ? PI / 2 : 0), ri(0, 2 * PI), ri(-.4, .4)];
  return [ri(-.3, .3), ri(0, 2 * PI), ri(-.3, .3)];
}
export function peca(pai, metal, p, s = 1) {   // uma peça de sucata (cobre, alu, aco, ferrugem) ou de impureza (terra, borracha, plastico)
  const k = pega(TIPOS[metal]), cor = pega(PAL[metal]);
  const sc = (k === 'bloco' || k === 'terra') ? [s * ri(.8, 1.3), s * ri(.55, .95), s * ri(.8, 1.25)] : s * ri(.85, 1.15);
  const o = poe(GEO[k], M(cor, { f: k === 'bloco' || k === 'terra' }), pai, p, giro(k), sc); o.receiveShadow = Q.get('rs') === '1'; o.userData.s0 = o.scale.clone(); return o;
}
export function monte(pai, p, o = {}) {   // monte de sucata; o: n, rx, rz, h, metais, mancha ([w, d] ou false)
  const g = grupo(pai, p), rx = o.rx ?? .9, rz = o.rz ?? .76;
  for (const q of domo(o.n ?? 34, rx, rz, o.h ?? .56)) peca(g, pega(o.metais ?? ['aco', 'aco', 'ferrugem', 'cobre', 'alu']), q);
  if (o.mancha !== false) mancha(g, ...(o.mancha ?? [rx * 2.55, rz * 2.5]), .3); return g;
}

// ------------------------------------------------------------------ 3D: lote de peças iguais (InstancedMesh) e o voo entre lugares
const _m = new THREE.Matrix4(), _mi = new THREE.Matrix4(), _p = new THREE.Vector3(), _p2 = new THREE.Vector3(), _pp = new THREE.Vector3(),
  _q = new THREE.Quaternion(), _q2 = new THREE.Quaternion(), _pq = new THREE.Quaternion(), _s = new THREE.Vector3(), _e = new THREE.Euler(), _c = new THREE.Color();
export function lote(geo, mat, n, pai) {
  const im = new THREE.InstancedMesh(geo, mat, n); im.castShadow = true; im.receiveShadow = Q.get('rs') === '1'; im.frustumCulled = false;
  im.userData.A = []; pai.add(im); return im;
}
export function poeInst(im, i, p, r = [0, 0, 0], s = 1) {
  _m.compose(_p.set(p[0], p[1], p[2]), _q.setFromEuler(_e.set(r[0], r[1], r[2])), Array.isArray(s) ? _s.set(...s) : _s.setScalar(s));
  im.setMatrixAt(i, _m); im.userData.A[i] = { p: _p.clone(), q: _q.clone(), s }; im.instanceMatrix.needsUpdate = true;
}
// leva cada peça do lugar de origem (A, no pai do lote) ao destino B[i] = [x, y, z, rx, ry, rz] no MUNDO, com arco e
// cada uma no seu tempo (a + ordem[i]·passo); chamar a cada quadro (o pai pode se mover: a peça que chegou fica no lugar)
export function transfere(im, B, t, a, d, o = {}) {
  const A = im.userData.A, pai = im.parent; pai.updateWorldMatrix(true, false);
  const PW = pai.matrixWorld; _mi.copy(PW).invert(); PW.decompose(_pp, _pq, _s);
  const passo = o.passo ?? .002, arco = o.arco ?? .5;
  for (let i = 0; i < A.length; i++) {
    const q = eio(pr(t, a + (o.ordem ? o.ordem[i] : i) * passo, d)), Ai = A[i], s = Ai.s, b = B[i];
    const sv = Array.isArray(s) ? _s.set(...s) : _s.setScalar(s);
    if (q <= 0) { _m.compose(Ai.p, Ai.q, sv); im.setMatrixAt(i, _m); continue; }
    _p.copy(Ai.p).applyMatrix4(PW).lerp(_p2.set(b[0], b[1], b[2]), q); _p.y += arco * Math.sin(PI * q);
    _q.copy(_pq).multiply(Ai.q).slerp(_q2.setFromEuler(_e.set(b[3] ?? 0, b[4] ?? 0, b[5] ?? 0)), q);
    _m.compose(_p, _q, sv).premultiply(_mi); im.setMatrixAt(i, _m);
  }
  im.instanceMatrix.needsUpdate = true;
}
export const ordemPor = (im, f) => { const A = im.userData.A, ix = A.map((_, i) => i).sort((i, j) => f(A[i].p) - f(A[j].p)), o = []; ix.forEach((i, k) => { o[i] = k; }); return o; };

// ------------------------------------------------------------------ 3D: objetos do pátio (sem marca)
// saco de ráfia fechado (tara)
export function saco(pai, p) {
  const g = grupo(pai, p), s = [1, 1, .82];
  poe(torno([[0, 0], [.2, .004], [.29, .05], [.325, .17], [.335, .34], [.315, .5], [.26, .62], [.17, .71], [.085, .77], [.072, .81], [.1, .87], [.115, .92], [.07, .95], [0, .955]], 30), M(COR.rafia), g, [0, 0, 0], [0, 0, 0], s);
  poe(new THREE.TorusGeometry(.083, .024, 8, 20), M(COR.rafiaE), g, [0, .79, 0], [PI / 2, 0, 0], [1, .82, 1]);
  for (const [y, r] of [[.25, .331], [.42, .33]]) poe(new THREE.TorusGeometry(r, .007, 6, 40), M('#C9AF7E'), g, [0, y, 0], [PI / 2, 0, 0], [1, .82, 1]);
  return g;
}
// saco aberto (o bruto): ráfia por fora; a carga vai num grupo à parte, na boca (y até .75)
export function sacoAberto(pai, p = [0, 0, 0]) {
  const g = grupo(pai, p), mf = M('#C9AF7E');
  poe(torno([[0, 0], [.24, .004], [.34, .05], [.385, .17], [.395, .34], [.38, .5], [.35, .62], [.33, .7], [.345, .75], [.365, .775]], 34), M(COR.rafia, { ds: true }), g, [0, 0, 0], [0, 0, 0], [1, 1, .84]);
  poe(new THREE.TorusGeometry(.358, .026, 8, 40), mf, g, [0, .765, 0], [PI / 2, 0, 0], [1, .84, 1]);
  for (const y of [.22, .4]) poe(new THREE.TorusGeometry(.392, .007, 6, 44), mf, g, [0, y, 0], [PI / 2, 0, 0], [1, .84, 1]);
  return g;
}
// tambor de aço
export function tambor(pai, p) {
  const g = grupo(pai, p), mt = M('#557891'), ma = M('#46667D');
  poe(new THREE.CylinderGeometry(.29, .29, .86, 36), mt, g, [0, .43, 0]);
  for (const y of [.29, .57]) poe(new THREE.TorusGeometry(.292, .017, 8, 40), ma, g, [0, y, 0], [PI / 2, 0, 0]);
  for (const y of [.012, .858]) poe(new THREE.TorusGeometry(.282, .022, 8, 40), ma, g, [0, y, 0], [PI / 2, 0, 0]);
  poe(new THREE.CylinderGeometry(.045, .045, .03, 16), ma, g, [.14, .87, .06]);
  return g;
}
// caçamba pequena (de empilhadeira): corpo em trapézio, boca escura e dois patins
export function cacamba(pai, p) {
  const g = grupo(pai, p), mt = M('#6E7B88');
  const sh = new THREE.Shape(); sh.moveTo(-.42, 0); sh.lineTo(.42, 0); sh.lineTo(.56, .5); sh.lineTo(-.56, .5); sh.closePath();
  const geo = new THREE.ExtrudeGeometry(sh, { depth: .04, bevelEnabled: true, bevelThickness: .012, bevelSize: .012, bevelSegments: 1, curveSegments: 1 });
  geo.translate(0, .08, -.02); for (const z of [-.31, .31]) poe(geo, mt, g, [0, 0, z]);
  const inc = Math.atan2(.14, .5); for (const sx of [-1, 1]) poe(rbox(.045, .53, .66, .015, 1), mt, g, [sx * .49, .33, 0], [0, 0, -sx * inc]);
  poe(rbox(.86, .04, .62, .015, 1), M('#56626F'), g, [0, .1, 0]);
  for (const x of [-.28, .28]) poe(rbox(.13, .07, .72, .02, 1), M(COR.cinzaE), g, [x, .035, 0]);
  return g;
}
// fardo prensado com duas cintas
export function fardo(pai, p, cor = COR.alu) {
  const g = grupo(pai, p); poe(rbox(.5, .42, .46, .035, 2), M(cor), g, [0, .21, 0]);
  for (const x of [-.13, .13]) poe(rbox(.03, .43, .47, .01, 1), M(COR.cinzaE), g, [x, .21, 0]); return g;
}
// palete de madeira (tampo a .115 do chão)
export function palete(pai, p) {
  const g = grupo(pai, p), m = M(COR.madeira), m2 = M(COR.madeiraE);
  for (const z of [-.4, 0, .4]) poe(rbox(1.3, .08, .13, .02, 1), m2, g, [0, .04, z]);
  for (let i = 0; i < 6; i++) poe(rbox(.18, .035, 1.0, .012, 1), m, g, [-.55 + i * .22, .098, 0]); return g;
}
// roda (pneu de perfil arredondado, aro e parafusos; eixo em z): gira em rotation.z
export function roda(pai, p, R, w) {
  const g = grupo(pai, p), k = .3 * w, r0 = R * .6;
  poe(torno([[r0, -w / 2], [R - k, -w / 2], [R - k * .25, -w / 2 + k * .25], [R, -w / 2 + k], [R, w / 2 - k], [R - k * .25, w / 2 - k * .25], [R - k, w / 2], [r0, w / 2]], 26), M(COR.pneu), g, [0, 0, 0], [PI / 2, 0, 0]);
  poe(new THREE.CylinderGeometry(r0, r0, w * .84, 22), M(COR.aro), g, [0, 0, 0], [PI / 2, 0, 0]);
  poe(new THREE.CylinderGeometry(R * .2, R * .2, w * .92, 12), M(COR.cinzaE), g, [0, 0, 0], [PI / 2, 0, 0]);
  for (let i = 0; i < 5; i++) { const a = i * 2 * PI / 5; poe(GEO.pino, M(COR.cinzaE), g, [Math.cos(a) * R * .38, Math.sin(a) * R * .38, 0], [PI / 2, 0, 0], [R * .07, w * .9, R * .07]); }
  return g;
}
// carroça de mão: caixa âmbar, duas rodas, varais de madeira (o fundo da caixa a y .59); userData.rodas, R
export function carroca(pai, p) {
  const g = grupo(pai, p), amb = M(COR.ambar), ambE = M(COR.ambarE), pau = M('#8A5A34'); g.userData.R = .36; g.userData.rodas = [];
  for (const z of [-.62, .62]) { const r = grupo(g, [0, .36, z]); g.userData.rodas.push(r);
    poe(new THREE.TorusGeometry(.28, .08, 10, 30), M(COR.pneu), r);
    poe(new THREE.CylinderGeometry(.2, .2, .09, 24), M(COR.aro), r, [0, 0, 0], [PI / 2, 0, 0]);
    for (let k = 0; k < 3; k++) poe(rbox(.38, .04, .1, .012, 1), M(COR.aco), r, [0, 0, 0], [0, 0, k * PI / 3]); }
  poe(new THREE.CylinderGeometry(.035, .035, 1.26, 10), M(COR.cinzaE), g, [0, .36, 0], [PI / 2, 0, 0]);
  for (const z of [-.38, .38]) poe(rbox(.12, .2, .06, .015, 1), M(COR.cinzaE), g, [0, .46, z]);
  poe(rbox(1.7, .06, 1.1, .02, 1), ambE, g, [0, .56, 0]);
  for (const x of [-.82, .82]) poe(rbox(.06, .42, 1.1, .02, 1), amb, g, [x, .77, 0]);
  for (const z of [-.52, .52]) poe(rbox(1.7, .42, .06, .02, 1), amb, g, [0, .77, z]);
  for (const z of [-.38, .38]) poe(new THREE.CylinderGeometry(.032, .032, 1.22, 10), pau, g, [1.45, .68, z], [0, 0, PI / 2 - .03]);
  poe(new THREE.CylinderGeometry(.034, .034, .9, 10), pau, g, [2.05, .7, 0], [PI / 2, 0, 0]);
  mancha(g, 2.4, 1.6, .3, [.4, 0, 0]); return g;
}
// balança de pátio (plataforma com rampas e o poste do mostrador). o: c (comprimento), l (largura), rampa, poste [x, z],
// hp (altura do poste), rp (raio do poste). userData.topo = ponto (local) para o mostrador; userData.altura(x local) = chão
export function balancaPatio(pai, p, o = {}) {
  const c = o.c ?? 3.8, l = o.l ?? 2.2, rp = o.rampa ?? .7, h = .172, g = grupo(pai, p);
  poe(rbox(c, .16, l, .05, 2), M('#8E98A3'), g, [0, .08, 0]); poe(rbox(c - .14, .02, l - .14, .008, 1), M(COR.cinzaC), g, [0, .163, 0]);
  const n = Math.floor((c - .6) / .4) + 1; for (let i = 0; i < n; i++) poe(rbox(.035, .012, l - .3, .006, 1), M('#A5AEB8'), g, [(i - (n - 1) / 2) * .4, .176, 0]);
  const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(rp, 0); sh.lineTo(rp, h); sh.closePath();
  const rg = new THREE.ExtrudeGeometry(sh, { depth: l - .2, bevelEnabled: false }); rg.translate(0, 0, -(l - .2) / 2);
  poe(rg, M('#C5CCD4'), g, [-c / 2 - rp, 0, 0]); poe(rg, M('#C5CCD4'), g, [c / 2 + rp, 0, 0], [0, 0, 0], [-1, 1, 1]);
  if (o.mancha !== false) mancha(g, c + 2 * rp + 1.2, l + .8, .26);
  const [px, pz] = o.poste ?? [c / 2 + .35, -(l / 2 + .25)], hp = o.hp ?? .96, r = o.rp ?? .045;
  poe(rbox(r * 7.5, .04, r * 7.5, .012, 1), M('#9AA3AD'), g, [px, .02, pz]); poe(new THREE.CylinderGeometry(r, r * 1.1, hp, 14), M('#B9C1C9'), g, [px, hp / 2 + .02, pz]);
  g.userData.topo = [px, hp + .03, pz];
  g.userData.altura = u => u < -c / 2 - rp ? 0 : u < -c / 2 ? h * (u + c / 2 + rp) / rp : u <= c / 2 ? h : u < c / 2 + rp ? h * (c / 2 + rp - u) / rp : 0;
  return g;
}
// latinhas: um lote de latas (lathe) com a cor de cada uma; P = pontos no pai; o.r(i) = giro, o.cores
const LATA = torno([[0, -.1], [.058, -.1], [.07, -.088], [.07, .078], [.06, .095], [.057, .1], [0, .1]], 10);
export const CORES_LATA = ['#C9D1DA', '#AFB9C4', '#DDE3E9', '#BAC3CD', '#C9D1DA', '#AFB9C4', '#DDE3E9', '#BAC3CD', '#9AA6B2', '#C9D1DA', '#50D088', '#F2B63D', '#5B8FD6', '#C8553D'];
export function latinhas(pai, P, o = {}) {
  const im = lote(LATA, M('#ffffff', { r: .6 }), P.length, pai);
  P.forEach((p, i) => { poeInst(im, i, p, o.r ? o.r(i) : [ri(0, 2 * PI), ri(0, 2 * PI), ri(0, 2 * PI)], o.s ?? ri(.9, 1.1)); im.setColorAt(i, _c.set(pega(o.cores ?? CORES_LATA))); });
  return im;
}
// baterias automotivas (caixa escura, tampa, polos): P = [x, y (base), z, giro]
const BAT = rbox(.34, .2, .22, .025, 1), TAMPA = rbox(.35, .035, .23, .012, 1), POLO = new THREE.CylinderGeometry(.026, .026, .045, 8);
export function baterias(pai, P) {
  const b = lote(BAT, M(COR.cinzaE), P.length, pai), tp = lote(TAMPA, M('#4B5563'), P.length, pai), po = lote(POLO, M('#ffffff'), 2 * P.length, pai);
  P.forEach(([x, y, z, r = 0], i) => { poeInst(b, i, [x, y + .1, z], [0, r, 0]); poeInst(tp, i, [x, y + .2175, z], [0, r, 0]);
    [[-.11, '#C8553D'], [.11, COR.pneu]].forEach(([sx, cor], k) => { poeInst(po, 2 * i + k, [x + Math.cos(r) * sx, y + .25, z - Math.sin(r) * sx]); po.setColorAt(2 * i + k, _c.set(cor)); }); });
  return { b, tp, po };
}
// caminhão (frente para +x). o: cor (cabine; padrão verde), c (comprimento), l (largura), R (roda), eixos (2 ou 3), cc/hc
// (cabine), bau ('basculante' | 'grade'), hb, carga ('latinha' | 'bateria' | nada = vazio), n (latas).
// userData: rodas, R, eixos (x de cada eixo), cacamba (pivô da caçamba, gira em z para bascular), carga, bau {cb, hb}.
export function caminhao(pai, p, o = {}) {
  const c = o.c ?? 6.6, Wd = o.l ?? 2.3, R = o.R ?? .46, ww = .34, cc = o.cc ?? 1.85, hc = o.hc ?? 1.7, y0 = 2 * R + .06, bt = .06;
  const g = grupo(pai, p), u = g.userData, mC = M(o.cor ?? COR.verde), mE = M(COR.cinzaE), mV = M(COR.vidro, { r: .45 });
  u.R = R; u.rodas = []; u.eixos = [c / 2 - .95, ...(o.eixos === 2 ? [-c / 2 + 1.15] : [-c / 2 + 1.0, -c / 2 + 2.0])];
  poe(rbox(c - .45, .26, Wd * .44, .04, 1), mE, g, [-.05, R + .2, 0]);                                        // chassi
  for (const x of u.eixos) for (const s of [-1, 1]) u.rodas.push(roda(g, [x, R, s * (Wd / 2 - ww / 2 - .03)], R, ww));
  poe(new THREE.CylinderGeometry(.2, .2, .8, 16), M(COR.cinzaC), g, [c / 2 - cc - .55, R + .1, Wd / 2 - .32], [0, 0, PI / 2]);   // tanque
  poe(rbox(cc - .1, y0 - R - .3, Wd - 2 * ww - .25, .03, 1), mE, g, [c / 2 - cc / 2, (R + .33 + y0) / 2, 0]);        // sob a cabine
  poe(rbox(.2, .3, Wd + .04, .05, 1), mE, g, [c / 2 + .06, R + .32, 0]);                                         // para-choque
  // cabine: perfil com o para-brisa inclinado, extrudado com borda arredondada
  const cab = grupo(g, [c / 2 - cc / 2, y0, 0]);
  const eg = new THREE.ExtrudeGeometry(new THREE.Shape([[0, 0], [cc, 0], [cc, hc * .56], [cc - .3, hc * .93], [cc - .44, hc], [0, hc]].map(v => new THREE.Vector2(...v))),
    { depth: Wd - 2 * bt, bevelEnabled: true, bevelThickness: bt, bevelSize: bt, bevelSegments: 3, curveSegments: 1 });
  eg.translate(-cc / 2, 0, -(Wd - 2 * bt) / 2); poe(eg, mC, cab);
  const th = Math.atan2(.3, .37 * hc), Ls = Math.hypot(.3, .37 * hc);
  poe(rbox(.03, Ls * .8, Wd - .44, .012, 1), mV, cab, [cc / 2 - .15 + Math.cos(th) * (bt + .01), hc * .745 + Math.sin(th) * (bt + .01), 0], [0, 0, th]);   // para-brisa
  poe(rbox(.03, hc * .24, Wd * .46, .01, 1), mE, cab, [cc / 2 + bt + .004, hc * .3, 0]);                         // grade
  for (const s of [-1, 1]) {
    poe(rbox(.7, hc * .29, .02, .01, 1), mV, cab, [cc / 2 - .66, hc * .73, s * (Wd / 2 + .004)]);                // janela
    poe(rbox(.03, .14, .3, .01, 1), M(COR.farol, { r: .5 }), cab, [cc / 2 + bt + .004, hc * .2, s * (Wd / 2 - .34)]);   // farol
    poe(rbox(.03, .12, .12, .01, 1), M(COR.ambar), cab, [cc / 2 + bt + .004, hc * .2, s * (Wd / 2 - .12)]);     // pisca
    poe(rbox(.2, .035, .035, .01, 1), mE, cab, [cc / 2 - .12, hc * .68, s * (Wd / 2 + .1)]);                       // braço do espelho
    poe(rbox(.05, .32, .12, .02, 1), M(COR.escuro), cab, [cc / 2 - .02, hc * .62, s * (Wd / 2 + .2)]);           // espelho
  }
  // caçamba (pivô no fundo de trás): basculante de aço ou carroceria de grade de madeira
  const cb = c - cc - .32, grade = o.bau === 'grade', hb = o.hb ?? (grade ? .55 : .9), x0 = -c / 2 + .04;
  poe(rbox(cb - .3, .15, Wd * .5, .03, 1), mE, g, [x0 + cb / 2, R + .33 + .075, 0]);                           // estrado
  const B = grupo(g, [x0, y0 - .04, 0]); u.cacamba = B; u.bau = { cb, hb, Wd };
  const mB = M(o.corB ?? (grade ? COR.madeira : '#98A2AD')), mR = M(grade ? COR.madeiraE : COR.aco);
  poe(rbox(cb, .1, Wd, .03, 1), grade ? mE : mB, B, [cb / 2, .05, 0]);
  if (grade) {
    for (const y of [.17, .33, .49]) { for (const s of [-1, 1]) poe(rbox(cb, .12, .06, .02, 1), mB, B, [cb / 2, y, s * (Wd / 2 - .03)]);
      for (const x of [.03, cb - .03]) poe(rbox(.06, .12, Wd, .02, 1), mB, B, [x, y, 0]); }
    for (const x of [.05, cb / 3, 2 * cb / 3, cb - .05]) for (const s of [-1, 1]) poe(rbox(.08, hb + .06, .08, .02, 1), mE, B, [x, .1 + (hb + .06) / 2 - .03, s * (Wd / 2 - .03)]);
  } else {
    for (const s of [-1, 1]) { poe(rbox(cb, hb, .07, .02, 1), mB, B, [cb / 2, .1 + hb / 2, s * (Wd / 2 - .035)]);
      poe(rbox(cb + .04, .07, .13, .02, 1), mR, B, [cb / 2, .1 + hb, s * (Wd / 2 - .035)]);
      for (let i = 1; i < 5; i++) poe(rbox(.07, hb - .06, .05, .015, 1), mR, B, [i * cb / 5, .1 + hb / 2, s * (Wd / 2 + .012)]); }
    poe(rbox(.08, hb + .3, Wd, .02, 1), mB, B, [cb - .04, .1 + (hb + .3) / 2, 0]);
    poe(rbox(.08, hb, Wd - .02, .02, 1), mR, B, [.04, .1 + hb / 2, 0]);
    u.pistao = poe(new THREE.CylinderGeometry(.075, .075, 1, 12), M(COR.aco), g); u.pistao.visible = false; u.x0 = x0; u.yb = y0 - .04;
  }
  if (o.carga === 'latinha') { const P = [], rx = cb / 2 - .15, rz = Wd / 2 - .15;
    for (let i = 0; i < (o.n ?? 380); i++) { const x = ri(-1, 1), z = ri(-1, 1); P.push([cb / 2 + x * rx, .1 + hb + .24 * (1 - x ** 4) * (1 - z ** 4) - ri(0, .32), z * rz]); }
    u.carga = latinhas(B, P); }
  if (o.carga === 'bateria') { const P = [], nx = Math.floor((cb - .2) / .38), nz = Math.floor((Wd - .2) / .27);
    for (let k = 0; k < 2; k++) for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) if (k === 0 || rng() < .8)
      P.push([.1 + (i + .5) * (cb - .2) / nx, .1 + k * .235, (j - (nz - 1) / 2) * .27, ri(-.06, .06)]);
    u.carga = baterias(B, P); }
  mancha(g, c + .8, Wd + .9, .3); return g;
}
// põe o veículo no ponto x (chão h(x) no mundo: rampas), com a inclinação entre o eixo da frente e o de trás e as rodas girando
export function anda(v, x, h = () => 0) {
  const u = v.userData, xf = u.eixos[0], xr = u.eixos.length > 2 ? (u.eixos[1] + u.eixos[2]) / 2 : u.eixos[1], yf = h(x + xf), yr = h(x + xr);
  v.position.x = x; v.position.y = (yr * xf - yf * xr) / (xf - xr); v.rotation.z = Math.atan2(yf - yr, xf - xr);
  for (const r of u.rodas) r.rotation.z = -x / u.R;
}
// bascula a caçamba (a em radianos), com o pistão aparecendo por baixo
export function bascula(v, a) {
  const u = v.userData; u.cacamba.rotation.z = a; if (!u.pistao) return; const L = u.bau.cb * .62;
  const bx = u.x0 + L - .25, by = u.R + .5, tx = u.x0 + L * Math.cos(a), ty = u.yb + L * Math.sin(a), dx = tx - bx, dy = ty - by;
  u.pistao.visible = a > .02; u.pistao.position.set((bx + tx) / 2, (by + ty) / 2, 0); u.pistao.scale.set(1, Math.hypot(dx, dy), 1); u.pistao.rotation.z = -Math.atan2(dx, dy);
}
// fardo de latinhas prensadas: bloco de alumínio com os fundos das latas nas faces e duas cintas
const FUNDO = new THREE.CylinderGeometry(.056, .056, .03, 10);
export function fardoLatinhas(pai, p, o = {}) {
  const g = grupo(pai, p), w = o.w ?? 1.0, h = o.h ?? .78, d = o.d ?? .78, P = [], Rr = [], e = .13;
  poe(rbox(w, h, d, .06, 2), M('#B4BDC7'), g, [0, h / 2, 0]);
  const grade = (a, b) => { const n = Math.floor((a - .12) / e), m = Math.floor((b - .12) / e), L = []; for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) L.push([(i - (n - 1) / 2) * e + ri(-.02, .02), (j - (m - 1) / 2) * e + ri(-.02, .02)]); return L; };
  for (const s of [-1, 1]) {
    for (const [x, y] of grade(w, h)) { P.push([x, h / 2 + y, s * (d / 2 + .004)]); Rr.push([PI / 2 + ri(-.3, .3), 0, ri(-.3, .3)]); }
    for (const [z, y] of grade(d, h)) { P.push([s * (w / 2 + .004), h / 2 + y, z]); Rr.push([ri(-.3, .3), 0, PI / 2 + ri(-.3, .3)]); }
  }
  for (const [x, z] of grade(w, d)) { P.push([x, h + .004, z]); Rr.push([ri(-.3, .3), 0, ri(-.3, .3)]); }
  const im = lote(FUNDO, M('#ffffff', { r: .6 }), P.length, g);
  P.forEach((q, i) => { poeInst(im, i, q, Rr[i], [ri(.75, 1.1), 1, ri(.75, 1.1)]); im.setColorAt(i, _c.set(pega(CORES_LATA))); });
  for (const x of [-w * .28, w * .28]) poe(rbox(.035, h + .03, d + .03, .01, 1), M(COR.cinzaE), g, [x, h / 2, 0]);
  mancha(g, w + .7, d + .7, .28); return g;
}
// prensa vertical (câmara âmbar, colunas, cilindro e placa que desce): aperta(g, p) com p de 0 (aberta) a 1 (prensando)
export function prensa(pai, p) {
  const g = grupo(pai, p), mA = M(COR.ambar), mAE = M(COR.ambarE), mE = M(COR.cinzaE), mS = M('#9AA4AE');
  poe(rbox(1.5, .12, 1.3, .03, 1), mE, g, [0, .06, 0]);
  poe(rbox(1.4, 1.45, 1.2, .05, 2), mA, g, [0, .845, 0]);                                                         // câmara
  poe(rbox(1.04, 1.0, .06, .03, 1), mAE, g, [0, .7, .61]); poe(rbox(.06, .42, .08, .02, 1), mE, g, [.4, .72, .66]);  // porta e trinco
  poe(rbox(.9, .2, .04, .02, 1), M(COR.pneu), g, [0, 1.38, .605]);                                                 // boca de carga
  for (const x of [-.6, .6]) poe(rbox(.16, 1.25, .16, .03, 1), mE, g, [x, 2.195, 0]);                              // colunas
  poe(rbox(1.5, .24, .5, .04, 1), mA, g, [0, 2.94, 0]);                                                            // travessa
  poe(new THREE.CylinderGeometry(.13, .13, .5, 18), mS, g, [0, 2.57, 0]);                                         // cilindro
  const haste = poe(new THREE.CylinderGeometry(.055, .055, 1, 12), M(COR.aco), g), placa = poe(rbox(1.04, .1, .96, .03, 1), mS, g);
  poe(rbox(.1, .4, .3, .02, 1), mE, g, [.75, 1.15, .25]);                                                           // comando
  poe(new THREE.CylinderGeometry(.045, .045, .04, 14), M(COR.verde), g, [.81, 1.22, .25], [0, 0, PI / 2]);
  poe(new THREE.CylinderGeometry(.045, .045, .04, 14), M(COR.ambar), g, [.81, 1.08, .25], [0, 0, PI / 2]);
  g.userData.haste = haste; g.userData.placa = placa; mancha(g, 2.2, 2.0, .3); aperta(g, 0); return g;
}
export function aperta(g, p) { const y = lerp(2.22, 1.64, cl(p)), u = g.userData; u.placa.position.set(0, y, 0); u.haste.position.set(0, (2.32 + y) / 2, 0); u.haste.scale.set(1, 2.32 - y, 1); }
// impressora térmica (corpo escuro, tampa, fenda, botão verde); imprime(g, p): o papel sai da fenda (0 a 1)
export function impressora(pai, p) {
  const g = grupo(pai, p);
  poe(rbox(.34, .13, .4, .05, 2), M(COR.cinzaE), g, [0, .065, 0]); poe(rbox(.32, .08, .25, .04, 2), M('#3A414A'), g, [0, .155, -.06]);
  poe(rbox(.26, .012, .014, .004, 1), M(COR.escuro), g, [0, .196, .066]);
  poe(new THREE.CylinderGeometry(.018, .018, .012, 14), M(COR.verde), g, [.12, .133, .15]);
  const pp = grupo(g, [0, .196, .068]); poe(rbox(.22, .32, .004, .002, 1), M(COR.papel), pp, [0, .16, 0]);
  for (let i = 0; i < 4; i++) poe(rbox(.15 - .03 * (i % 2), .008, .002, .001, 1), M('#C9CED4'), pp, [-.02 * (i % 2), .26 - i * .055, .003]);
  g.userData.papel = pp; mancha(g, .6, .6, .25); imprime(g, 0); return g;
}
export function imprime(g, p) { const pp = g.userData.papel; pp.visible = p > .001; pp.scale.set(1, Math.max(1e-4, p), 1); pp.rotation.x = .3 * p; }
// computador (monitor com a tela lisa, sem nada do app; teclado e mouse); userData.tela = a malha da tela
export function computador(pai, p) {
  const g = grupo(pai, p), mC = M(COR.cinzaE), cz = M('#D5DBE1');
  poe(rbox(.26, .02, .17, .01, 1), mC, g, [0, .01, -.06]); poe(rbox(.06, .24, .04, .015, 1), mC, g, [0, .13, -.1]);
  const mon = grupo(g, [0, .4, -.07]); mon.rotation.x = -.08; poe(rbox(.66, .42, .035, .02, 2), M(COR.escuro), mon);
  g.userData.tela = poe(rbox(.61, .36, .01, .005, 1), M(COR.tela, { r: .5 }), mon, [0, .01, .018]);
  poe(rbox(.52, .025, .17, .01, 1), cz, g, [0, .0125, .22]);
  for (let i = 0; i < 4; i++) poe(rbox(.46, .008, .026, .004, 1), M('#BCC4CC'), g, [0, .028, .16 + i * .04]);
  poe(new THREE.SphereGeometry(.035, 14, 10), cz, g, [.36, .02, .23], [0, 0, 0], [1, .55, 1.4]);
  mancha(g, 1.0, .7, .22); return g;
}
// chão do pátio: placa de concreto clara (topo em y 0) com juntas e, se pedir, faixas âmbar (o.faixa = lista de z).
// Com ele, cena(..., {chao: false}) (sem o chão invisível de sombra).
export function chaoPatio(pai, p, o = {}) {
  const c = o.c ?? 16, l = o.l ?? 9, e = o.passo ?? 2.5, g = grupo(pai, p), mJ = M(COR.junta);
  poe(rbox(c, .14, l, .07, 2), M(COR.concreto), g, [0, -.07, 0]).castShadow = false;
  for (let x = -c / 2 + e; x < c / 2 - .2; x += e) poe(rbox(.035, .004, l - .12, .002, 1), mJ, g, [x, .0005, 0]).castShadow = false;
  for (let z = -l / 2 + e; z < l / 2 - .2; z += e) poe(rbox(c - .12, .004, .035, .002, 1), mJ, g, [0, .0005, z]).castShadow = false;
  for (const z of o.faixa ?? []) for (let x = -c / 2 + .6; x < c / 2 - 1; x += 1.6) poe(rbox(.9, .004, .1, .002, 1), M(COR.ambar), g, [x + .45, .001, z]).castShadow = false;
  return g;
}
