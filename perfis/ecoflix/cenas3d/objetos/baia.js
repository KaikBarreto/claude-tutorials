// baia(pai, p, o): baia de estoque do pátio (três muretas de concreto: fundo e laterais; aberta para +z), com a borda de cima mais
// escura. A carga (latinhas, fardos...) vai dentro, por conta da cena. Base em y 0, centro do chão da baia em x/z.
// o: c (largura livre em x, 3.0), l (fundo em z, 2.2), h (altura da mureta, 1.0), e (espessura, .2).
// userData.dentro = centro do chão (local); userData.topo = ponto acima do meio do fundo.
// Uso (T00): const b = baia(CENA, [x, 0, z]); latinhas(grupo(b), domo(...)).
import { grupo, poe, rbox, M, mancha } from '../kit3d.js';

export function baia(pai, p = [0, 0, 0], o = {}) {
  const g = grupo(pai, p), c = o.c ?? 3.0, l = o.l ?? 2.2, h = o.h ?? 1.0, e = o.e ?? .2, mP = M('#C9D1DA'), mB = M('#AEB7C1');
  poe(rbox(c + 2 * e, h, e, .04, 2), mP, g, [0, h / 2, -l / 2 - e / 2]);
  poe(rbox(c + 2 * e + .04, .06, e + .04, .02, 1), mB, g, [0, h + .03, -l / 2 - e / 2]);
  for (const s of [-1, 1]) { poe(rbox(e, h, l, .04, 2), mP, g, [s * (c / 2 + e / 2), h / 2, 0]);
    poe(rbox(e + .04, .06, l + .04, .02, 1), mB, g, [s * (c / 2 + e / 2), h + .03, 0]); }
  mancha(g, c + 1.4, l + 1.2, .26);
  g.userData.dentro = [0, 0, 0]; g.userData.topo = [0, h + .2, -l / 2]; return g;
}
