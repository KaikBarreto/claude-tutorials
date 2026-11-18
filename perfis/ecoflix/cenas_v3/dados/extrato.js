// Extrato ou lista com linhas (movimentos do caixa, contas a pagar, tickets do dia, estoque por material): cabeçalho, linhas
// com ícone, descrição, legenda e valor (entrada verde, saída vermelha), e o rodapé com o total que conta.
// uso: const x = plano(htmlExtrato({ icone: 'wallet', titulo: 'Caixa do dia', sub: '18 de novembro',
//        linhas: [['truck', 'Compra · latinha', '3.018 kg', -21126], ['banknote', 'Venda · fardo', '1.200 kg', 9480]], total: ['Saldo', 4354] }), { pos, esc, clima: 'escuro' });
//      extrato(x.e, t, a, b, { tempos: [t1, t2, ...], tTotal });   ·   marca(x.e, i, t, a) acende a linha i (a que a fala cita)
// O valor numérico é formatado em reais com sinal; um texto vai como está (ex.: '3.018 kg'). o: w (400), fmt, cor do selo.
import { ic, selo, vis, pr, eo, eo5, lerp, estilo } from '../motor.js';
import { base, pt, entra, quando, reais } from './base.js';
const val = (v, fmt) => typeof v === 'number' ? (v < 0 ? '− ' : '+ ') + fmt(Math.abs(v)) : (v ?? '');
export function htmlExtrato(o = {}) {
  base(); estilo('d-ext', `
.d-ext{padding:20px 22px 18px;isolation:isolate}.d-ext .top{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.d-ext .ln{position:relative;display:grid;grid-template-columns:34px 1fr auto;gap:12px;align-items:center;height:52px;border-top:1px solid var(--ln)}
.d-ext .ln .bx{width:34px;height:34px;border-radius:11px;background:var(--fx);color:var(--tx2);display:flex;align-items:center;justify-content:center}
.d-ext .ln .d-v{font-size:15.5px}.d-ext .ln .d-s{font-size:12.5px}.d-ext .ln .d-n{font-size:16px;color:var(--tx)}
.d-ext .ln .hl{position:absolute;inset:3px -10px;border-radius:12px;background:var(--fx2);opacity:0;z-index:-1}
.d-ext .tot{display:flex;align-items:baseline;justify-content:space-between;border-top:1.5px solid var(--tr);padding-top:13px;margin-top:2px}.d-ext .tot .num{font-size:30px}`);
  const fmt = o.fmt ?? reais;
  return `<div class="cartao d-ext" style="position:relative;width:${o.w ?? 400}px">
    <div class="top">${selo(o.icone ?? '', o.cor ?? '', 44)}<div><div class="d-t">${o.titulo ?? ''}</div><div class="d-s">${o.sub ?? ''}</div></div></div>
    ${(o.linhas ?? []).map(([i, r, s, v]) => `<div class="ln"><i class="hl"></i><div class="bx">${ic(i, 18)}</div><div><div class="d-v">${r}</div><div class="d-s">${s ?? ''}</div></div><div class="d-n ${typeof v === 'number' ? (v < 0 ? 'd-neg' : 'd-pos') : ''}">${val(v, fmt)}</div></div>`).join('')}
    ${o.total ? `<div class="tot"><span class="d-k">${o.total[0]}</span><span class="num r" data-v="${typeof o.total[1] === 'number' ? o.total[1] : ''}">${typeof o.total[1] === 'number' ? fmt(o.total[1]) : o.total[1]}</span></div>` : ''}</div>`;
}
export function extrato(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 24, sc: .96 }); const L = pt(e, '.ln'); L.forEach((x, i) => entra(x, t, quando(o, a, i, .13, .3), { dx: -14, dy: 0 }));
  const tt = o.tTotal ?? quando(o, a, L.length, .13, .4);
  for (const x of pt(e, '.tot')) { entra(x, t, tt, { dy: 8 }); const n = x.querySelector('.num'), v = parseFloat(n.dataset.v); if (!isNaN(v)) { const s = (o.fmt ?? reais)(lerp(0, v, eo5(pr(t, tt, .8)))); if (n.textContent !== s) n.textContent = s; } }
}
export function marca(e, i, t, a, b = 1e9) { const h = pt(e, '.hl')[i]; if (h) h.style.opacity = Math.min(eo(pr(t, a, .3)), 1 - eo(pr(t, b, .3))).toFixed(3); }
