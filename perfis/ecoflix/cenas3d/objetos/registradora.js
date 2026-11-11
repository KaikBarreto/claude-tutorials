// registradora(pai, p, o): caixa registradora genérica, sem marca (Kaik, 11/11: no lugar da gaveta vista de cima). Gaveta embaixo
// (abre para a frente, com cédulas e moedas), teclado inclinado (tecla verde do total), visor escuro com o valor em verde (textura:
// "R$" pequeno e o número; vazio até visor(txt)) e a impressora atrás, à direita, de onde sai o cupom (cupom.js, tipo genérico).
// Frente (teclado e gaveta) para +z, base em y 0, ~.46 x .44 x .42 m.
// userData: abre(p) gaveta de 0 (fechada) a 1 (aberta); visor(txt) escreve no visor (ex.: '235,60'); cupom (o grupo do cupom.js:
//   cupom.userData.sai(q)); prende() acerta o corte do cupom na altura da fenda (chamar depois de posicionar a registradora);
//   fenda, gaveta (meio da gaveta aberta) e topo = pontos locais (use mundo(reg, ponto)).
// Uso (T00): const reg = registradora(CENA, [x, yBalcao, z]); reg.userData.prende(); reg.userData.visor('235,60'); reg.userData.abre(.8).
import { PI, THREE, grupo, poe, rbox, M, COR, mancha, mundo } from '../kit3d.js';
import { cedula } from './cedula.js';
import { cupom } from './cupom.js';

export function registradora(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), u = g.userData, mCx = M('#3F4750'), mCorpo = M('#5E6670'), mTec = M('#E3E8EC'), mEsc = M(COR.escuro);
  poe(rbox(.46, .13, .42, .025, 2), mCx, g, [0, .065, 0]);                                                  // caixa da gaveta
  // gaveta (desliza para +z): frente, puxador, bandeja com as cédulas atrás e as moedas na frente
  const gav = grupo(g);
  poe(rbox(.44, .105, .022, .012, 1), M('#7E8994'), gav, [0, .062, .216]);
  poe(rbox(.14, .022, .02, .008, 1), M('#4F5861'), gav, [0, .07, .232]);
  poe(new THREE.CylinderGeometry(.012, .012, .012, 14), M('#4F5861'), gav, [.17, .07, .229], [PI / 2, 0, 0]);
  poe(rbox(.42, .016, .38, .006, 1), M('#DDE3E8'), gav, [0, .022, .02]);
  for (const x of [-.205, .205]) poe(rbox(.012, .05, .38, .004, 1), M('#C4CCD4'), gav, [x, .045, .02]);
  poe(rbox(.42, .03, .01, .004, 1), M('#C4CCD4'), gav, [0, .04, .085]);
  ['#9ED9B5', '#7CC69B', '#B7E4C7', '#8FCFA8'].forEach((c, i) => { const n = cedula(gav, [-.15 + i * .1, .033, .0], { cor: c, w: .15, d: .08 }); n.rotation.y = PI / 2; });
  [['#C9A44C', -.16], ['#AEB8C2', -.08], ['#C9A44C', 0], ['#AEB8C2', .08], ['#C9A44C', .16]].forEach(([c, x]) =>
    poe(new THREE.CylinderGeometry(.024, .024, .01, 18), M(c), gav, [x, .035, .15]));
  // corpo com o teclado inclinado (perfil em z, y extrudado ao longo de x)
  const perfil = new THREE.Shape([[.19, .13], [.19, .17], [-.02, .265], [-.19, .265], [-.19, .13]].map(v => new THREE.Vector2(...v)));
  const eg = new THREE.ExtrudeGeometry(perfil, { depth: .41, bevelEnabled: true, bevelThickness: .015, bevelSize: .015, bevelSegments: 2, curveSegments: 1 });
  eg.rotateY(-PI / 2); eg.translate(.205, 0, 0); poe(eg, mCorpo, g);
  const tec = grupo(g, [0, .233, .085]); tec.rotation.x = Math.atan2(.095, .21);
  for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) poe(rbox(.046, .02, .036, .008, 1), mTec, tec, [-.175 + c * .058, 0, -.075 + r * .05]);
  poe(rbox(.07, .022, .086, .01, 1), M(COR.verde), tec, [.15, .001, .05]); poe(rbox(.07, .02, .036, .008, 1), M(COR.ambar), tec, [.15, 0, -.05]);
  // visor (painel escuro inclinado para quem está na frente) e a impressora com a fenda
  poe(rbox(.06, .07, .05, .015, 1), mCx, g, [-.075, .3, -.12]);
  const vis = grupo(g, [-.075, .37, -.11]); vis.rotation.x = -.35; poe(rbox(.28, .11, .03, .014, 2), mEsc, vis);
  const cv = document.createElement('canvas'); cv.width = 420; cv.height = 140; const cx = cv.getContext('2d');
  const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  const tela = new THREE.Mesh(new THREE.PlaneGeometry(.255, .085), new THREE.MeshBasicMaterial({ map: tx, toneMapped: false }));
  tela.position.z = .0156; vis.add(tela);
  let ult = null;
  u.visor = txt => { txt = String(txt ?? ''); if (txt === ult) return; ult = txt;
    cx.fillStyle = '#121212'; cx.fillRect(0, 0, 420, 140); if (!txt) { tx.needsUpdate = true; return; }
    cx.textBaseline = 'alphabetic'; cx.textAlign = 'right'; cx.font = '800 84px M, Montserrat, sans-serif'; cx.fillStyle = '#50D088';
    const w = cx.measureText(txt).width; cx.fillText(txt, 400, 102);
    cx.font = '800 42px M, Montserrat, sans-serif'; cx.fillStyle = '#A9E9C6'; cx.fillText('R$', 400 - w - 14, 102); tx.needsUpdate = true; };
  u.visor('');
  poe(rbox(.13, .07, .12, .02, 1), mCx, g, [.14, .3, -.12]); poe(rbox(.1, .006, .014, .003, 1), mEsc, g, [.14, .336, -.1]);
  u.fenda = [.14, .337, -.1]; u.gaveta = [0, .07, .42]; u.topo = [0, .5, 0];
  if (o.cupom !== false) { u.cupom = cupom(g, u.fenda, { papel: 58, desenho: 58, alt: 76, esc: .1 / 58, tipo: 'generico' });
    u.prende = () => u.cupom.userData.corteEm(mundo(g, u.fenda)[1]); }
  else u.prende = () => {};
  u.abre = q => { gav.position.z = .27 * Math.min(1, Math.max(0, q)); };
  mancha(g, .8, .72, .25); u.abre(0); return g;
}
