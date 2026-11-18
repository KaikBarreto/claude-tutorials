// Cancela de pátio: caixa-base e o braço listrado de âmbar e branco. O braço fecha ao longo de +z (atravessa a pista) e sobe.
// uso: const cn = cancela(CENA, [x, 0, z], { l: 4.5 }); ergue(cn, eio(pr(t, a, .7)));   // 0 = fechada, 1 = aberta
// Origem no pé da base. userData: pv (o pivô do braço), topo, luz (a lâmpada: verde quando abre).
import { PI, cl, mat, caixa, cil, malha, grupo, mancha } from '../motor.js';
export function cancela(pai, pos = [0, 0, 0], o = {}) {
  const l = o.l ?? 4.5, g = grupo(pai, pos), cz = mat('#CBD3DC', { alt: 1.3, emi: .14 }), esc = mat('#56626F', { alt: 1.3, emi: .24 });
  mancha(1.6, 1.5, [0, 0, .05], { pai: g, op: .7 });
  malha(caixa(.46, 1.1, .46, .07), cz, [0, .55, 0], g); malha(caixa(.5, .08, .5, .03), esc, [0, .04, 0], g); malha(caixa(.48, .07, .48, .03), mat('#50D088', { emi: .6, alt: 1.3 }), [0, 1.1, 0], g);
  const pv = grupo(g, [.27, .92, 0]); malha(cil(.11, .1, 18), esc, [0, 0, 0], pv, [0, 0, PI / 2]);
  const n = Math.round(l / .5); for (let i = 0; i < n; i++) malha(caixa(.07, .11, l / n + .012, i === n - 1 ? .03 : .008), mat(i % 2 ? '#F4F6F8' : '#F2B63D', { emi: .36, alt: 5 }), [.02, 0, .1 + (i + .5) * l / n], pv);
  malha(caixa(.09, .16, .5, .03), esc, [.02, 0, -.2], pv);
  g.userData = { pv, l, topo: [0, 1.7, 0] }; ergue(g, 0); return g;
}
export function ergue(g, a) { g.userData.pv.rotation.x = -cl(a) * (PI / 2 - .05); }
