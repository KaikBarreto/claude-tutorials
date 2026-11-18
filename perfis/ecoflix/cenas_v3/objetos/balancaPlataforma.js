// Balança de plataforma (a de pesar saco, fardo e tambor no chão): base baixa com o tampo de aço, poste e a cabeça do
// indicador. A tela do indicador é escura e LISA: o número é um plano (htmlVisor) preso em userData.topo.
// uso: const b = balancaPlataforma(CENA, [x, 0, z], { c: 1.2, l: 1.0 }); saco(b, [0, b.userData.sup, 0]);
// Frente para +z. userData: sup (altura do tampo), topo (acima da cabeça), tela (centro da tela), saida (de onde sai o cabo).
import { mat, caixa, cil, malha, grupo, mancha } from '../motor.js';
export function balancaPlataforma(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 1.2, l = o.l ?? 1.0, hp = o.hp ?? 1.25, g = grupo(pai, pos), aco = mat('#D9E0E7', { alt: .5, emi: .14 }), cz = mat('#AEB9C5', { alt: .5, emi: .14 }), esc = mat('#56626F', { alt: 1.5, emi: .24 });
  mancha(c + 1.3, l + 1.2, [0, 0, .08], { pai: g, op: .7 });
  malha(caixa(c, .11, l, .03), cz, [0, .065, 0], g); malha(caixa(c - .06, .03, l - .06, .012), aco, [0, .13, 0], g);
  for (let i = 0; i < 5; i++) malha(caixa(c - .2, .008, .03, .003), cz, [0, .147, (i - 2) * l * .17], g);
  for (const x of [-1, 1]) for (const z of [-1, 1]) malha(cil(.05, .03, 12), esc, [x * (c / 2 - .1), .015, z * (l / 2 - .1)], g);
  malha(caixa(c - .04, .03, .04, .01), mat('#8CF2BC', { emi: .47, emiC: .25 }), [0, .1, l / 2 + .005], g);   // o fio de luz da borda, como na rodoviária
  const pz = -l / 2 - .14; malha(caixa(.3, .05, .22, .02), esc, [0, .025, pz], g); malha(cil(.035, hp, 12), mat('#9AA6B3', { alt: hp, emi: .14 }), [0, hp / 2, pz], g);
  const cab = grupo(g, [0, hp + .06, pz + .02]); cab.rotation.x = -.22; malha(caixa(.46, .26, .1, .035), esc, [0, 0, 0], cab);
  malha(caixa(.38, .15, .012, .004), mat('#131514', { bri: .1, emi: .7 }), [0, .025, .051], cab); malha(caixa(.3, .012, .014, .004), mat('#50D088', { emi: 1.32, emiC: .2 }), [0, -.085, .052], cab);
  g.userData = { sup: .147, c, l, topo: [0, hp + .3, pz], tela: [0, hp + .085, pz + .08], saida: [.2, .05, pz] }; return g;
}
