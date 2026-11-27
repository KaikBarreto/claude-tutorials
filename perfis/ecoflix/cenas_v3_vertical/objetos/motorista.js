// Motorista: a pessoa do kit de boné e camisa verdes, com o braço direito à frente para entregar ou segurar um papel.
// uso: const m = motorista(CENA, [x, 0, z]); m.rotation.y = PI / 2;  folha(m.userData.mao, [.06, .12, 0], { w: .3 })
// userData (além dos da pessoa): mao = grupo na mão que segura (use mundo(m.userData.mao) para o ponto no mundo); estende(a) = ângulo do braço.
import { pessoa } from './pessoa.js';
export function motorista(pai, pos = [0, 0, 0], o = {}) {
  const g = pessoa(pai, pos, { camisa: '#50D088', bone: '#2E7D57', calca: '#39424A', ...o }), u = g.userData, maos = u.mao;
  u.estende = a => { u.bracos[1].rotation.z = a; }; u.estende(o.braco ?? 1.15); u.maos = maos; u.mao = maos[1]; return g;
}
