// Calendário de um mês (vencimentos, fechamento, prazo de documento): cabeçalho com o mês, a grade dos dias, dias marcados
// (bolinha verde, ou âmbar para "vence"), o dia de hoje (contorno) e uma faixa de período.
// uso: const c = plano(htmlCalendario({ mes: 'Novembro', ano: 2026, inicio: 0, dias: 30, hoje: 18, marcas: [[20, 'a'], [25, '']], faixa: [9, 13] }), { pos, esc, clima: 'escuro' });
//      calendario(c.e, t, a, b, { tempos: [tMarca1, tMarca2] });   // os dias entram em cascata; cada marca "bate" no seu instante
// inicio = dia da semana do dia 1 (0 = domingo). o: w (364), icone ('calendar').
import { selo, vis, pr, eo, passa, estilo } from '../motor.js';
import { base, pt, quando } from './base.js';
export function htmlCalendario(o = {}) {
  base(); estilo('d-cal', `
.d-cal{padding:18px 20px 16px}.d-cal .top{display:flex;align-items:center;gap:12px;margin-bottom:12px}.d-cal .top .d-s{margin-left:auto;font-weight:700}
.d-cal .gr{display:grid;grid-template-columns:repeat(7,1fr);row-gap:4px}.d-cal .sm{height:24px;text-align:center;font-weight:700;font-size:11px;letter-spacing:.1em;color:var(--mut)}
.d-cal .di{position:relative;height:40px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:var(--tx);font-variant-numeric:tabular-nums}
.d-cal .di.fd{color:var(--tx2)}.d-cal .di.fx{background:var(--fx2)}.d-cal .di.fx.f0{border-radius:12px 0 0 12px}.d-cal .di.fx.f1{border-radius:0 12px 12px 0}
.d-cal .di .mk{position:absolute;left:50%;top:50%;width:36px;height:36px;margin:-18px;border-radius:50%;background:linear-gradient(150deg,#63D99B,#2FB271);box-shadow:0 8px 16px -5px rgba(47,178,113,.6);z-index:-1}
.d-cal .di .mk.a{background:linear-gradient(150deg,#F7CB68,#E59A22);box-shadow:0 8px 16px -5px rgba(229,154,34,.6)}
.d-cal .di.m{color:#fff}.d-cal .di .hj{position:absolute;left:50%;top:50%;width:36px;height:36px;margin:-18px;border-radius:50%;border:2px solid var(--ac)}.d-cal{isolation:isolate}`);
  const mk = new Map((o.marcas ?? []).map(m => Array.isArray(m) ? m : [m, ''])), ini = o.inicio ?? 0, n = o.dias ?? 30, [f0, f1] = o.faixa ?? [0, -1];
  return `<div class="cartao d-cal" style="position:relative;width:${o.w ?? 364}px"><div class="top">${selo(o.icone ?? '', o.cor ?? '', 40)}<div class="d-t">${o.mes ?? ''}</div><div class="d-s">${o.ano ?? ''}</div></div>
    <div class="gr">${['D', 'S', 'T', 'Q', 'Q', 'S', 'S'].map(s => `<div class="sm">${s}</div>`).join('')}${'<div></div>'.repeat(ini)}${[...Array(n)].map((_, i) => { const d = i + 1, col = (ini + i) % 7;
      return `<div class="di ${col === 0 || col === 6 ? 'fd' : ''} ${d >= f0 && d <= f1 ? 'fx' : ''} ${d === f0 || (d > f0 && d <= f1 && col === 0) ? 'f0' : ''} ${d === f1 || (d >= f0 && d < f1 && col === 6) ? 'f1' : ''} ${mk.has(d) ? 'm' : ''}">${mk.has(d) ? `<i class="mk ${mk.get(d)}"></i>` : ''}${d === o.hoje ? '<i class="hj"></i>' : ''}${d}</div>`; }).join('')}</div></div>`;
}
export function calendario(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 24, sc: .96 }); const D = pt(e, '.di'); let k = 0;
  D.forEach((x, i) => { x.style.opacity = eo(pr(t, a + .25 + i * .012, .25)).toFixed(3); const m = x.querySelector('.mk');
    if (m) { const ti = quando(o, a, k++, .3, .9), p = pr(t, ti, .5); m.style.transform = `scale(${(p <= 0 ? 0 : passa(p, 1.8)).toFixed(4)})`; x.style.color = p > .15 ? '#fff' : ''; } });
}
