// fardoPapelao(pai, p, o): fardo de papelão prensado (bloco kraft com as camadas de onduleira nas faces e três cintas de aço).
// Origem no centro da base (como `fardo` do kit); o: w (comprimento em x, 1.1), h (altura, .8), d (profundidade, .9), mancha (false
// desliga a sombra de contato). Uso (T04 cap08): import { fardoPapelao } from '../../../../perfis/ecoflix/cenas3d/objetos/fardoPapelao.js';
import { M, COR, rbox, poe, grupo, mancha } from '../kit3d.js';

export function fardoPapelao(pai, p = [0, 0, 0], o = {}) {
  const w = o.w ?? 1.1, h = o.h ?? .8, d = o.d ?? .9, g = grupo(pai, p);
  poe(rbox(w, h, d, .05, 2), M('#B98A58'), g, [0, h / 2, 0]);
  // camadas do papelão prensado: faixas finas, alternando dois tons, nas faces da frente, de trás e nos lados
  const n = Math.round(h / .075);
  for (let i = 0; i < n; i++) {
    const y = .06 + i * (h - .12) / (n - 1), m = M(i % 2 ? '#A87848' : '#C9A06E');
    for (const s of [-1, 1]) {
      poe(rbox(w - .1, .028, .012, .005, 1), m, g, [0, y, s * (d / 2 + .002)]).castShadow = false;
      poe(rbox(.012, .028, d - .1, .005, 1), m, g, [s * (w / 2 + .002), y, 0]).castShadow = false;
    }
  }
  for (const x of [-w * .3, 0, w * .3]) poe(rbox(.032, h + .03, d + .03, .01, 1), M(COR.cinzaE), g, [x, h / 2, 0]);
  if (o.mancha !== false) mancha(g, w + .7, d + .7, .26);
  return g;
}
