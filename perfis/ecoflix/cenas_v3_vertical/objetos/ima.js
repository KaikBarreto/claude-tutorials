// Ímã de separação: ferradura vermelha de pontas claras, pendurada num carrinho que corre num trilho (separa o ferro do resto).
// uso: const im = ima(CENA, [x, y, z]); trilho(CENA, x0, x1, y + im.userData.topo, z); campo(im, a);   // a de 0 a 1: os anéis de atração
// Origem = centro do arco; as pontas ficam em x = ±R e y = -.66 (userData.ponta). O ímã anda em x: im.position.x.
import { PI, mat, caixa, cil, toro, malha, grupo, THREE } from '../motor.js';
export function ima(pai, pos = [0, 0, 0], o = {}) {
  const R = o.R ?? .46, g = grupo(pai, pos), vm = mat('#E5574A', { bri: .3, emi: .32, alt: 6 }), cl = mat('#E6EBF0', { emi: .32, alt: 6 }), esc = mat('#39424A', { bri: .12, emi: .24, alt: 6 });
  malha(toro(R, .15, 30, PI), vm, [0, 0, 0], g);
  for (const s of [-1, 1]) { malha(cil(.15, .42, 22), vm, [s * R, -.21, 0], g); malha(cil(.152, .24, 22), cl, [s * R, -.54, 0], g); }
  malha(cil(.035, .7, 10), esc, [0, R + .48, 0], g); malha(caixa(.2, .12, .2, .04), esc, [0, R + .16, 0], g);
  malha(caixa(.7, .2, .5, .06), esc, [0, R + .92, 0], g); for (const x of [-.24, .24]) malha(cil(.09, .56, 14), mat('#AEB9C5', { emi: .14, alt: 6 }), [x, R + 1.0, 0], g, [PI / 2, 0, 0]);
  const aneis = [-1, 1].flatMap(s => [.24, .4].map((r, i) => { const m = new THREE.MeshBasicMaterial({ color: '#50D088', transparent: true, opacity: 0, depthWrite: false }); const a = malha(toro(r, .014, 40), m, [s * R, -.74 - i * .16, 0], g, [PI / 2, 0, 0]); a.visible = false; return a; }));
  g.userData = { R, ponta: [R, -.66], topo: R + 1.12, campo: aneis }; return g;
}
export function campo(g, a) { g.userData.campo.forEach((t, i) => { t.material.opacity = .85 * a; t.visible = a > .01; t.scale.setScalar(.8 + .2 * a + (i % 2) * .05 * a); }); }
// trilho: duas vigas ao longo de x, de x0 a x1, com a face de baixo em y, e dois postes até o chão
export function trilho(pai, x0, x1, y, z = 0) {
  const g = grupo(pai, [(x0 + x1) / 2, 0, z]), c = x1 - x0, aco = mat('#8F9BAA', { alt: y, emi: .14 });
  for (const s of [-1, 1]) malha(caixa(c, .14, .1, .03), aco, [0, y + .07, s * .3], g);
  for (const s of [-1, 1]) { malha(caixa(.16, y + .14, .16, .04), aco, [s * (c / 2 - .08), (y + .14) / 2, -.55], g); malha(caixa(.14, .12, .95, .03), aco, [s * (c / 2 - .08), y + .07, -.12], g); malha(caixa(.5, .06, .5, .02), mat('#56626F', { emi: .14 }), [s * (c / 2 - .08), .03, -.55], g); }
  return g;
}
