// Caçamba estacionária (a de entulho e sucata que fica parada no cliente): corpo âmbar de pontas inclinadas, boca aberta,
// nervuras, pinos de içar e dois patins. Comprimento em x. É a que o poliguindaste.js leva e traz.
// uso: const k = cacambaEstacionaria(CENA, [x, 0, z], { c: 3.4, l: 1.7, h: 1.1 });  pecas(k, 'ferro', pontos)  ·  userData: c, l, h, boca, pinos, topo
import { mat, caixa, perfil, cil, malha, grupo, mancha, PI } from '../motor.js';
export function cacambaEstacionaria(pai, pos = [0, 0, 0], o = {}) {
  const c = o.c ?? 3.4, l = o.l ?? 1.7, h = o.h ?? 1.1, g = grupo(pai, pos), m = mat(o.cor ?? '#F2B63D', { alt: 1.4, bri: .22, emi: .3 }), e = mat('#D99A2B', { alt: 1.4, emi: .3 }), esc = mat('#3B444E', { bri: .08, emi: .14 });
  const sm = mancha(c + 2, l + 1.8, [0, 0, .08], { pai: g, op: .8 }), rec = .55, y0 = .1;
  for (const z of [-l / 2, l / 2]) { malha(perfil([[-c / 2 + rec, y0], [c / 2 - rec, y0], [c / 2, h], [-c / 2, h]], .04, .06, .015), m, [0, 0, z], g);
    for (const x of [-c * .22, 0, c * .22]) malha(caixa(.09, h - y0 - .12, .05, .02), e, [x, (h + y0) / 2 - .02, z + Math.sign(z) * .05], g);
    malha(cil(.06, .16, 14), esc, [-c * .34, h - .22, z + Math.sign(z) * .1], g, [PI / 2, 0, 0]); malha(cil(.06, .16, 14), esc, [c * .34, h - .22, z + Math.sign(z) * .1], g, [PI / 2, 0, 0]); }
  const inc = Math.atan2(rec, h - y0), L = Math.hypot(rec, h - y0);
  for (const sx of [-1, 1]) malha(caixa(.06, L, l, .02), m, [sx * (c / 2 - rec / 2), (h + y0) / 2, 0], g, [0, 0, -sx * inc]);
  malha(caixa(c - 2 * rec, .06, l, .02), e, [0, y0 + .03, 0], g);
  for (const z of [-l / 2, l / 2]) malha(caixa(c + .06, .09, .11, .03), e, [0, h, z], g); for (const x of [-c / 2, c / 2]) malha(caixa(.11, .09, l + .1, .03), e, [x, h, 0], g);
  malha(caixa(c - .1, .04, l - .08, .015), mat('#8A6A22', { bri: .04, emi: .08 }), [0, h - .08, 0], g);   // o fundo escuro da boca (fica sob a carga)
  for (const z of [-l * .3, l * .3]) malha(caixa(c - 2 * rec - .2, .1, .14, .03), esc, [0, .05, z], g);
  g.userData = { c, l, h, boca: h, sombra: sm, pinos: [[-c * .34, h - .22], [c * .34, h - .22]], topo: [0, h + .8, 0] }; return g;
}
