// Caixa registradora genérica, sem marca (é registradora, não gaveta vista de cima): gaveta embaixo que abre para a frente
// com cédulas e moedas, teclado inclinado com a tecla verde do total, visor escuro com o valor em verde e a impressora
// atrás, de onde sai o cupom. Frente para +z, base em y 0.
// uso: const reg = registradora(CENA, [x, y, z], { s: 2.2 }); reg.userData.visor('235,60'); reg.userData.abre(eo(pr(t, a, .5))); reg.userData.cupom.userData.sai(p);
// o: s (escala; 1 = 46 cm de largura: no balcão do guichê use 1.6; sozinha na cena, 2 a 3), cupom (false tira).
// userData: abre(p) (0 fechada, 1 aberta), visor(txt) ('' = apagado), cupom, fenda, gaveta (meio da gaveta aberta), topo (pontos locais).
import { PI, mat, caixa, perfil, cil, malha, grupo, mancha, pintura, lote, poeInst, THREE } from '../motor.js';
import { cedula } from './cedula.js';
import { cupom } from './cupom.js';
export function registradora(pai, pos = [0, 0, 0], o = {}) {
  const s = o.s ?? 1, G = grupo(pai, pos), g = grupo(G), u = G.userData, A = { alt: .5 * s, bri: .2 }, cx = mat('#4B5661', { ...A, emi: .36 }), corpo = mat('#DCE3EA', { ...A, emi: .13 }), esc = mat('#17191A', { bri: .08, emi: .5 });
  g.scale.setScalar(s); mancha(1.0 * s, .95 * s, [0, 0, .05 * s], { pai: G, op: .75 });
  malha(caixa(.46, .13, .42, .028), cx, [0, .065, 0], g);
  // gaveta (desliza para +z): frente, puxador, bandeja com as cédulas atrás e as moedas na frente
  const gav = grupo(g); malha(caixa(.44, .105, .024, .012), mat('#8F9BAA', { ...A, emi: .28 }), [0, .062, .216], gav); malha(caixa(.14, .024, .022, .008), mat('#50D088', { emi: .88 }), [0, .07, .232], gav);
  malha(caixa(.42, .016, .38, .006), mat('#EEF2F5', { emi: .14 }), [0, .022, .02], gav); for (const x of [-.205, .205]) malha(caixa(.012, .05, .38, .004), mat('#CBD3DC', { emi: .14 }), [x, .045, .02], gav);
  malha(caixa(.42, .03, .01, .004), mat('#CBD3DC', { emi: .14 }), [0, .04, .085], gav);
  ['#A6E3BF', '#8FD7AD', '#BDEBD0', '#9BDDB6'].forEach((c, i) => { cedula(gav, [-.15 + i * .1, .034, 0], { cor: c, w: .15, d: .08 }).rotation.y = PI / 2; });
  const mo = lote(cil(.024, .012, 18), mat('#FFFFFF', { emi: .36, bri: .35 }), 5, gav); ['#E3B94F', '#C9D1DA', '#E3B94F', '#C9D1DA', '#E3B94F'].forEach((c, i) => poeInst(mo, i, [-.16 + i * .08, .036, .15], [0, 0, 0], 1, c));
  // corpo com o teclado inclinado
  const pf = perfil([[.19, .13], [.19, .17], [-.02, .265], [-.19, .265], [-.19, .13]], .012, .43, .014); pf.rotateY(-PI / 2); malha(pf, corpo, [0, 0, 0], g);
  const tec = grupo(g, [0, .233, .085]); tec.rotation.x = Math.atan2(.095, .21);
  const tk = lote(caixa(.046, .02, .036, .008), mat('#FFFFFF', { emi: .32, bri: .15 }), 20, tec); for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) poeInst(tk, r * 5 + c, [-.175 + c * .058, 0, -.075 + r * .05], [0, 0, 0], 1, c === 4 ? '#B8C2CC' : '#F4F6F8');
  malha(caixa(.07, .024, .086, .01), mat('#50D088', { emi: .99, emiC: .1 }), [.15, .001, .05], tec); malha(caixa(.07, .022, .036, .008), mat('#F2B63D', { emi: .7 }), [.15, 0, -.05], tec);
  // visor (painel escuro inclinado para quem está na frente) e a impressora com a fenda
  malha(caixa(.06, .07, .05, .015), cx, [-.075, .3, -.12], g); const vs = grupo(g, [-.075, .37, -.11]); vs.rotation.x = -.3; malha(caixa(.29, .12, .03, .014), esc, [0, 0, 0], vs);
  let ult = null; const mv = pintura(420, 140, () => {}, { emi: 1 });
  malha(new THREE.PlaneGeometry(.262, .087), mv, [0, 0, .0156], vs);
  u.visor = txt => { txt = String(txt ?? ''); if (txt === ult) return; ult = txt; mv.userData.refaz((x, W, H) => { x.fillStyle = '#131514'; x.fillRect(0, 0, W, H); if (!txt) return;
    x.textBaseline = 'alphabetic'; x.textAlign = 'right'; x.font = '800 84px M, Montserrat, sans-serif'; x.fillStyle = '#6CF0A8'; const w = x.measureText(txt).width; x.fillText(txt, 400, 102);
    x.font = '800 42px M, Montserrat, sans-serif'; x.fillStyle = '#A9E9C6'; x.fillText('R$', 400 - w - 14, 102); }); };
  u.visor(o.valor ?? '');
  malha(caixa(.14, .08, .13, .022), cx, [.14, .305, -.12], g); malha(caixa(.105, .006, .016, .003), esc, [.14, .3455, -.1], g);
  u.fenda = [.14 * s, .346 * s, -.1 * s]; u.gaveta = [0, .07 * s, .42 * s]; u.topo = [0, .62 * s, 0];
  if (o.cupom !== false) { u.cupom = cupom(g, [.14, .346, -.098], { w: .1, h: .17, dobra: -.25 }); u.cupom.userData.sai(0); }
  u.abre = q => { gav.position.z = .27 * Math.min(1, Math.max(0, q)); }; u.abre(0); return G;
}
