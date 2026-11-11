// Chaparia: pilha de chapas de aço (retângulos finos de cinza variado, cada uma um pouco fora do prumo), para a carroceria do
// caminhão (grade) ou o chão. p = centro da base. Uso: chaparia(B, [cb / 2, .1, 0], { c: 2.6, l: 1.5, n: 7 }) dentro do pivô da
// caçamba (caminhao(...).userData.cacamba); no 3/4 (c 5,2) o pivô tem cb ≈ 3,2 e o chão da carroceria está em y .1.
import { PI, grupo, poe, rbox, M, ri } from '../kit3d.js';

const CS = ['#A3ACB6', '#8E98A2', '#B5BDC6', '#97A1AB', '#ADB5BE', '#9AA3AD'];
export function chaparia(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 2.6, l = o.l ?? 1.5, n = o.n ?? 7, e = .075;
  for (let i = 0; i < n; i++) {
    const w = c * (.9 + .1 * ((i * 7) % 3) / 2), d = l * (.88 + .12 * ((i * 5) % 3) / 2);
    poe(rbox(w, e, d, .018, 1), M(CS[i % 6]), g, [((i % 2) - .5) * .12, e / 2 + i * (e + .004), ((i % 3) - 1) * .05], [0, (i % 2 ? -1 : 1) * .014 * (1 + i % 3), 0]);
  }
  g.userData.topo = n * (e + .004); return g;
}
