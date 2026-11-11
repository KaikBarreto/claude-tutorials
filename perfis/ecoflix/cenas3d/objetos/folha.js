// Folha de documento genérica (papel claro, faixa colorida no alto e linhas cinza), sem texto: o rótulo (sigla, "MDF-e",
// "NF-e"...) é um chip HTML preso à folha com ancora(). Pivô no centro, face para +z (vire com rotation).
// Uso: const f = folha(CENA, [x, y, z], { cor: COR.verde, w: .5, h: .66, linhas: 4 }); f.rotation.y = -.3;
// Para a folha voar de um lugar a outro, mexa em f.position; f.userData.topo = ponto de cima (para o chip).
import { PI, grupo, poe, rbox, M, COR, mancha } from '../kit3d.js';

export function folha(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), w = o.w ?? .5, h = o.h ?? .66, n = o.linhas ?? 4;
  poe(rbox(w, h, .022, .018, 2), M(COR.papel), g);
  poe(rbox(w * .84, h * .15, .01, .008, 1), M(o.cor ?? COR.verde), g, [0, h * .32, .014]);
  for (let i = 0; i < n; i++) poe(rbox(w * (i % 2 ? .5 : .66), h * .035, .008, .004, 1), M('#C9CED4'), g, [-w * (i % 2 ? .17 : .09), h * .12 - i * h * .115, .013]);
  g.userData.topo = [0, h / 2, 0];
  if (o.mancha) mancha(g, w + .3, .6, .25);
  return g;
}
