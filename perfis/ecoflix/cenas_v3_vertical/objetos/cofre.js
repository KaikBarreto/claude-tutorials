// Cofre genérico, sem marca: caixa de aço escura com pés, porta mais clara com o volante de três raios, o painel da senha
// com a luz verde e as dobradiças à esquerda. A porta abre para fora e mostra as prateleiras com os maços de cédulas.
// Frente para +z, base em y 0. Tamanho de ilustração: s = 1 → 1,3 m de largura e 1,7 m de altura.
// uso: const c = cofre(CENA, [x, 0, z], { s: 1.2 }); c.userData.abre(eo(pr(t, a, .9)));   // 0 fechado, 1 aberto
// o: s (escala), cor (corpo), macos (quantos maços dentro: padrão 6; 0 = vazio).
// userData: abre(p), dentro (ponto no meio da prateleira de cima, de onde sai e aonde volta o dinheiro), boca (ponto na
//   frente da porta aberta), topo (acima do cofre: prenda ali o chip), macos (os grupos dos maços, para esconder um). Pontos locais.
import { mat, caixa, cil, toro, malha, grupo, mancha, PI } from '../motor.js';
import { maco } from './cedula.js';
export function cofre(pai, pos = [0, 0, 0], o = {}) {
  const s = o.s ?? 1, G = grupo(pai, pos), g = grupo(G), u = G.userData, A = { alt: 2 * s, bri: .2 };
  const corpo = mat(o.cor ?? '#56626F', { ...A, emi: .3 }), esc = mat('#39424A', { ...A, emi: .24 }), porta = mat('#8F9BAA', { ...A, emi: .28 }), aco = mat('#DCE3EA', { ...A, emi: .3, bri: .3 }),
    fundo = mat('#2B323B', { bri: .08, emi: .18 }), vd = mat('#50D088', { emi: .95, emiC: .08, alt: 2 * s });
  const W = 1.3, H = 1.6, D = 1.0, E = .09, Y = .1;
  g.scale.setScalar(s); mancha(2.7 * s, 2.2 * s, [0, 0, .12 * s], { pai: G, op: .78 });
  for (const x of [-.47, .47]) for (const z of [-.33, .33]) malha(caixa(.2, .12, .2, .03), esc, [x, .06, z], g);
  // casco aberto na frente: fundo, laterais, teto e piso; por dentro, o painel escuro e a prateleira
  malha(caixa(W, H, E, .03), corpo, [0, Y + H / 2, -D / 2 + E / 2], g);
  for (const x of [-1, 1]) malha(caixa(E, H, D, .03), corpo, [x * (W / 2 - E / 2), Y + H / 2, 0], g);
  for (const y of [E / 2, H - E / 2]) malha(caixa(W, E, D, .03), corpo, [0, Y + y, 0], g);
  malha(caixa(W - 2 * E, H - 2 * E, .02, .005), fundo, [0, Y + H / 2, -D / 2 + E + .01], g);
  const YP = Y + H * .52; malha(caixa(W - 2 * E + .02, .045, D - E - .12, .012), aco, [0, YP, -.03], g);
  u.macos = []; const n = o.macos ?? 6;
  for (let i = 0; i < n; i++) { const cima = i < 3, m = maco(g, [-.32 + (i % 3) * .32, (cima ? YP + .03 : Y + E + .012), .02 + (i % 2) * .06], 4 + (i * 7) % 3, { w: .27 }); m.rotation.y = PI / 2 + (i % 3 - 1) * .08; u.macos.push(m); }
  // dobradiças no corpo e a porta, que gira na aresta esquerda da frente
  for (const y of [.3, .7]) malha(cil(.035, .2, 14), aco, [-W / 2 - .012, Y + H * y, D / 2 + .03], g);
  const pv = grupo(g, [-W / 2 + .03, Y, D / 2 + .02]), pt = grupo(pv, [W / 2 - .03, 0, 0]);
  malha(caixa(W - .04, H - .04, .1, .035), porta, [0, H / 2, .03], pt); malha(caixa(W - .3, H - .3, .03, .012), mat('#A3AEBB', { ...A, emi: .28 }), [0, H / 2, .085], pt);
  malha(caixa(W - .22, H - .22, .07, .02), esc, [0, H / 2, -.05], pt);   // o miolo grosso da porta, que entra no casco
  const vol = grupo(pt, [.14, H * .5, .12]); malha(toro(.17, .026, 40), aco, [0, 0, .05], vol); malha(cil(.06, .09, 20), aco, [0, 0, .035], vol, [PI / 2, 0, 0]); malha(cil(.035, .03, 16), vd, [0, 0, .09], vol, [PI / 2, 0, 0]);
  for (let k = 0; k < 3; k++) malha(caixa(.33, .034, .03, .012), aco, [0, 0, .05], vol, [0, 0, k * PI / 3]);
  malha(caixa(.2, .27, .03, .012), esc, [-.33, H * .5, .1], pt); malha(caixa(.14, .05, .012, .005), vd, [-.33, H * .5 + .075, .118], pt);
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) malha(caixa(.034, .034, .012, .004), aco, [-.375 + c * .045, H * .5 + .015 - r * .045, .118], pt);
  u.abre = p => { p = Math.min(1, Math.max(0, p)); pv.rotation.y = -1.95 * p; vol.rotation.z = -2.6 * Math.min(1, p * 3); };
  u.dentro = [0, (YP + .16) * s, .1 * s]; u.boca = [.1 * s, (YP + .2) * s, (D / 2 + .5) * s]; u.topo = [0, (Y + H + .42) * s, 0]; u.abre(0); return G;
}
