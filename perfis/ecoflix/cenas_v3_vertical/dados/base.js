// Base dos componentes de DADOS do kit v3 (dados/*.js): variáveis de clima que faltam no motor e os movimentos internos.
// Convenção de todo componente: htmlNome(o) devolve o HTML (vai num plano(): o clima vem da classe do plano) e
// nome(e, t, a, b, o) anima: entra em a, sai em b (padrão: fica), função pura de t. `e` = plano.e. Depois dele valem foco() e pulso().
// Feitos para o clima escuro (o mundo dos dados); no claro viram papel branco (documento impresso, quadro na parede).
import { estilo, pr, eo, eo5, ei, passa, cl } from '../motor.js';
export function base() { estilo('d-base', `
.claro{--ln:rgba(23,25,26,.09);--fx:rgba(23,25,26,.045);--fx2:rgba(47,178,113,.12);--mut:#98A2A0;--ac:#2FB271;--am:#D9921E;--vm:#D9544A;--tr:rgba(23,25,26,.10)}
.escuro{--ln:rgba(255,255,255,.13);--fx:rgba(255,255,255,.06);--fx2:rgba(80,208,136,.16);--mut:rgba(255,255,255,.42);--ac:#6CF0A8;--am:#F7C55A;--vm:#FF8D7E;--tr:rgba(255,255,255,.14)}
.d-k{font-weight:700;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);white-space:nowrap}
.d-v{font-weight:700;font-size:16px;color:var(--tx);white-space:nowrap}
.d-t{font-weight:800;font-size:19px;line-height:1.15;color:var(--tx);white-space:nowrap}
.d-s{font-weight:600;font-size:14px;line-height:1.25;color:var(--tx2);white-space:nowrap}
.d-n{font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.01em;white-space:nowrap}
.d-pos{color:var(--ac)}.d-neg{color:var(--vm)}.d-amb{color:var(--am)}`); }
// partes de um componente, achadas uma vez só
export const pt = (e, s) => ((e._pt ??= {})[s] ??= [...e.querySelectorAll(s)]);
// entra: uma parte interna aparece em a (a opacidade chega antes da posição). o: dy, dx, d, sc (< .9 passa e volta)
export function entra(x, t, a, o = {}) {
  const d = o.d ?? .45, p = eo5(pr(t, a, d * 1.3)), op = eo(pr(t, a, d * .6)), dy = o.dy ?? 10, dx = o.dx ?? 0, sc = o.sc ?? 1, s = sc < .9 ? sc + (1 - sc) * passa(pr(t, a, d * 1.1), 1.6) : sc + (1 - sc) * p;
  x.style.opacity = op.toFixed(4); x.style.transform = `translate(${((1 - p) * dx).toFixed(2)}px,${((1 - p) * dy).toFixed(2)}px) scale(${s.toFixed(4)})`; return op;
}
// tempos: o instante de cada parte. o.tempos = lista explícita (âncoras da fala, W()), senão escalonado a partir de a
export const quando = (o, a, i, passo = .12, atraso = .25) => o.tempos?.[i] ?? a + atraso + i * passo;
export const NF2 = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
export const reais = v => 'R$ ' + NF2.format(v);
export { cl };
