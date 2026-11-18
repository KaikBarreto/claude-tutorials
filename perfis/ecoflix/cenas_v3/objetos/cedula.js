// Cédula genérica (retângulo verde-claro com a borda e o oval do meio mais escuros), sem número nem marca, deitada (face
// para +y), pivô no centro. Tamanho de ilustração. Para voar, mexa em position/rotation.
// uso: const n = cedula(CENA, [x, y, z], { w: .5 });   maco(CENA, [x, y, z], 6) = um maço empilhado com a cinta
import { mat, caixa, cil, malha, grupo } from '../motor.js';
export function cedula(pai, pos = [0, 0, 0], o = {}) {
  const w = o.w ?? .16, d = o.d ?? w * .47, g = grupo(pai, pos), c = o.cor ?? '#A6E3BF', e = mat('#3FA873', { emi: .5, bri: .1 });
  malha(caixa(w, w * .02, d, w * .008), mat(c, { emi: .36, bri: .15 }), [0, 0, 0], g); malha(caixa(w * .9, w * .008, d * .8, w * .003), mat('#C9F1DA', { emi: .36 }), [0, w * .0085, 0], g);
  const oval = malha(cil(d * .27, w * .008, 22), e, [0, w * .011, 0], g); oval.scale.set(1.25, 1, 1);
  for (const s of [-1, 1]) malha(caixa(w * .1, w * .008, d * .5, w * .003), e, [s * w * .36, w * .011, 0], g);
  g.userData = { w, d }; return g;
}
export function maco(pai, pos = [0, 0, 0], n = 6, o = {}) {
  const w = o.w ?? .16, g = grupo(pai, pos); for (let i = 0; i < n; i++) cedula(g, [(i % 2 ? 1 : -1) * w * .01, i * w * .022, 0], o).rotation.y = (i % 3 - 1) * .03;
  malha(caixa(w * .16, n * w * .022 + w * .012, w * .5, w * .004), mat('#F4F6F8', { emi: .5 }), [0, (n - 1) * w * .011, 0], g); g.userData = { w, h: n * w * .022 }; return g;
}
