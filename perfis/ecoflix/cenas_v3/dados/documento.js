// Documento fiscal genérico (nota, manifesto, MTR, ticket, contrato): cabeçalho com selo e sigla, campos, itens, total, a
// chave em barrinhas e o carimbo de situação. Layout próprio do kit: não copia DANFE, MDF-e nem formulário oficial, sem brasão.
// uso: const d = plano(htmlDocumento({ icone: 'file-text', tipo: 'Nota fiscal', sigla: 'NF-e', numero: 'Nº 000.482 · Série 1',
//        campos: [['Emitente', 'Recicla Vale'], ['Destino', 'Fundição Aurora']], itens: [['Alumínio latinha', '3.018 kg', 'R$ 21.126,00']],
//        total: ['Total', 'R$ 21.126,00'], status: 'Autorizada' }), { pos, esc: .011, clima: 'escuro' });
//      documento(d.e, t, a, b, { tempos: [tCampos, tItens, tTotal, tCarimbo] });   // sem tempos: tudo escalonado a partir de a
// o: w (420), cor ('' verde | 'a' âmbar | 'n' neutro: o selo), status + statusCor ('' | 'a' pendente | 'v' rejeitada), chave (false tira).
import { selo, vis, pr, eo, golpe, mola, estilo } from '../motor.js';
import { base, pt, entra, quando } from './base.js';
export function htmlDocumento(o = {}) {
  base(); estilo('d-doc', `
.d-doc{padding:20px 22px 20px}.d-doc .top{display:flex;align-items:center;gap:12px}
.d-doc .sig{margin-left:auto;padding:5px 12px;border-radius:9px;font-weight:800;font-size:15px;letter-spacing:.06em;color:var(--ac);background:var(--fx2);white-space:nowrap}
.d-doc .gr{display:grid;grid-template-columns:1fr 1fr;gap:12px 18px;margin-top:16px;padding-top:15px;border-top:1px solid var(--ln)}
.d-doc .cp{display:flex;flex-direction:column;gap:3px;min-width:0}
.d-doc .its{margin-top:15px;border-radius:12px;background:var(--fx);padding:4px 13px}
.d-doc .it{display:grid;grid-template-columns:1fr auto auto;gap:14px;align-items:center;height:36px;border-top:1px solid var(--ln)}.d-doc .it:first-child{border-top:0}
.d-doc .it .d-s{color:var(--tx)}.d-doc .it .q{font-weight:600;font-size:13.5px;color:var(--tx2);white-space:nowrap}.d-doc .it .d-n{font-size:15px;color:var(--tx)}
.d-doc .tot{display:flex;align-items:baseline;justify-content:space-between;margin-top:14px}.d-doc .tot .num{font-size:28px}
.d-doc .ch{display:flex;gap:3px;align-items:flex-end;height:22px;margin-top:14px;opacity:.9}.d-doc .ch i{display:block;flex:none;border-radius:1.5px;background:var(--mut)}
.d-doc .car{position:absolute;right:20px;bottom:18px;display:flex;align-items:center;gap:7px;padding:6px 13px 6px 10px;border-radius:10px;border:2px solid var(--ac);color:var(--ac);
  font-weight:800;font-size:14px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;rotate:-7deg;background:var(--fx2)}
.d-doc .car.a{border-color:var(--am);color:var(--am);background:rgba(242,182,61,.14)}.d-doc .car.v{border-color:var(--vm);color:var(--vm);background:rgba(229,87,74,.13)}`);
  const ch = o.chave === false ? '' : `<div class="ch">${[...Array(30)].map((_, i) => `<i style="width:${[2, 4, 2, 3, 5, 2][(i * 7 + (i >> 2)) % 6]}px;height:${i % 9 === 0 ? 22 : 17}px"></i>`).join('')}</div>`;
  return `<div class="cartao d-doc" style="position:relative;width:${o.w ?? 420}px">
    <div class="top">${selo(o.icone ?? '', o.cor ?? '', 44)}<div><div class="d-t">${o.tipo ?? 'Documento'}</div><div class="d-s">${o.numero ?? ''}</div></div>${o.sigla ? `<div class="sig">${o.sigla}</div>` : ''}</div>
    ${o.campos?.length ? `<div class="gr">${o.campos.map(([k, v]) => `<div class="cp"><span class="d-k">${k}</span><span class="d-v">${v}</span></div>`).join('')}</div>` : ''}
    ${o.itens?.length ? `<div class="its">${o.itens.map(([d, q, v]) => `<div class="it"><span class="d-s">${d}</span><span class="q">${q ?? ''}</span><span class="d-n">${v ?? ''}</span></div>`).join('')}</div>` : ''}
    ${o.total ? `<div class="tot"><span class="d-k">${o.total[0]}</span><span class="num r">${o.total[1]}</span></div>` : ''}${ch}
    ${o.status ? `<div class="car ${o.statusCor ?? ''}"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5l3.2 3.2L13 5"/></svg>${o.status}</div>` : ''}</div>`;
}
export function documento(e, t, a, b = 1e9, o = {}) {
  vis(e, t, a, b, { dy: 24, sc: .96 }); const T = i => o.tempos?.[i] ?? a + [.3, .65, .95, 1.35][i];
  pt(e, '.cp').forEach((x, i) => entra(x, t, T(0) + i * .08, { dy: 8 })); pt(e, '.it').forEach((x, i) => entra(x, t, T(1) + i * .1, { dx: -12, dy: 0 }));
  for (const x of pt(e, '.tot')) entra(x, t, T(2), { dy: 8 });
  pt(e, '.ch i').forEach((x, i) => { x.style.transform = `scaleY(${eo(pr(t, T(2) + .1 + i * .008, .25)).toFixed(3)})`; x.style.transformOrigin = '50% 100%'; });
  for (const c of pt(e, '.car')) { const p = pr(t, T(3), .5); c.style.opacity = eo(pr(t, T(3), .14)).toFixed(3); c.style.scale = (1.7 - .7 * mola(p, .55)).toFixed(4); }   // o carimbo bate
}
