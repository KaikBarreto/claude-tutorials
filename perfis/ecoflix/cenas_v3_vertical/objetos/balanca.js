// Balança rodoviária de pátio (plataforma com rampas nas pontas e poste do visor) no material do kit v3.
// uso: const B = balanca(CENA, [x, 0, z], { c: 8.2, l: 3.1 });  B.userData.altura(xMundo) → altura do piso sob a roda;
//      B.userData.poste = [x, y, z] do topo do poste (prenda ali o plano do visor: htmlVisor + plano)
import { PI, mat, caixa, perfil, cil, malha, grupo, mancha } from '../motor.js';
export function balanca(pai, pos, o = {}) {
  const c = o.c ?? 8.2, l = o.l ?? 3.1, h = o.h ?? .24, rp = o.rampa ?? 1.5, g = grupo(pai, pos), tampo = mat('#D9E0E7', { alt: .5 }), lado = mat('#AEB9C5', { alt: .5 });
  mancha(c + 2 * rp + 2.4, l + 2.6, [0, 0, .25], { pai: g, op: .62 });
  malha(caixa(c, h, l, .035), tampo, [0, h / 2, 0], g);
  for (const s of [-1, 1]) { const r = malha(perfil([[0, 0], [rp, 0], [0, h]], .02, l - .1, .02), lado, [s * c / 2, 0, 0], g); r.scale.x = s; }
  // fio de luz na borda da frente do tampo (branco no claro, verde aceso no escuro) e as células de carga
  malha(caixa(c - .2, .035, .05, .01), mat('#8CF2BC', { emi: .95, emiC: .25 }), [0, h - .02, l / 2 + .012], g);
  for (const x of [-c / 2 + .9, 0, c / 2 - .9]) malha(caixa(.44, .1, .1, .02), mat('#56626F', { emi: .6 }), [x, h * .42, l / 2 + .02], g);
  const px = o.poste?.[0] ?? c / 2 + .55, pz = o.poste?.[1] ?? -l / 2 - .35, hp = o.hp ?? 3.2;
  malha(cil(.07, hp, 16), mat('#9AA6B3', { alt: hp }), [px, hp / 2, pz], g); malha(cil(.32, .09, 28, .26), mat('#7F8B98', { alt: .5 }), [px, .045, pz], g);
  mancha(1.5, 1.1, [px + .1, 0, pz + .1], { pai: g, op: .5 });
  const x0 = pos[0], cl = (v, a, b) => Math.min(b, Math.max(a, v));
  g.userData = { h, c, l, poste: [pos[0] + px, hp, pos[2] + pz],
    altura: x => { const d = Math.abs(x - x0) - c / 2; return d <= 0 ? h : h * (1 - cl(d / rp, 0, 1)); } };
  return g;
}
