// Folha de estilos EcoFlix · o que é igual nos 10 painéis: tamanho do quadro, Montserrat, os três rótulos (título, visor
// "9.460 kg" e selo "Carregado") e o sorteio com semente. Cada estiloNN.html só troca o desenho e o CSS dos rótulos.
export const LG = 728, AL = 880;
const FT = new URL('../../../ferramentas/web/fonts/', import.meta.url).href;
const ff = (w, x) => `@font-face{font-family:M;font-weight:${w};src:url(${FT}montserrat-latin${x ? '-ext' : ''}-${w}-normal.woff2) format('woff2')${x ? ';unicode-range:U+0100-024F' : ''}}`;
const CSS = [500, 600, 700, 800].map(w => ff(w) + ff(w, 1)).join('') + `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:${LG}px;height:${AL}px;overflow:hidden}
body{font-family:M,sans-serif;color:#161618;-webkit-font-smoothing:antialiased;position:relative}
#fd,#ov,#gl,#sv{position:absolute;left:0;top:0;width:${LG}px;height:${AL}px}
.ab{position:absolute}
.tit{position:absolute;left:0;top:58px;width:${LG}px;text-align:center}
.kick{font-weight:700;font-size:15px;letter-spacing:.3em;text-transform:uppercase;color:#2E7D57}
.h{margin-top:10px;font-weight:800;font-size:42px;letter-spacing:-.01em;line-height:1.1;white-space:nowrap}
.visor{position:absolute;width:226px;padding:14px 20px 16px;border-radius:16px;background:#161618}
.vl{font-weight:700;font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:#A9E9C6;white-space:nowrap}
.vn{margin-top:5px;font-weight:800;font-size:38px;color:#50D088;font-variant-numeric:tabular-nums;white-space:nowrap;letter-spacing:-.01em}
.chip{position:absolute;display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 17px 0 13px;border-radius:999px;
  font-weight:800;font-size:18px;white-space:nowrap;color:#fff;background:#50D088}
.chip svg{width:21px;height:21px;flex:none}`;
{ const s = document.createElement('style'); s.textContent = CSS; document.head.prepend(s); }

export const CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m8.5 12.3 2.4 2.4 4.6-4.9"/></svg>';
export const TXT = { kick: 'Dupla pesagem', h: 'Entrada na balança', vl: '1ª pesagem', vn: '9.460 kg', chip: 'Carregado' };

// fundo (#fd), desenho (quem chama põe) e rótulos (#ov). Devolve { fd, ov, tit, visor, chip }
export function palco(o = {}) {
  document.body.insertAdjacentHTML('beforeend', `<div id="fd"></div>${o.meio || ''}<div id="ov">
    <div class="tit"><div class="kick">${TXT.kick}</div><div class="h">${TXT.h}</div></div>
    <div class="visor"><div class="vl">${TXT.vl}</div><div class="vn">${TXT.vn}</div></div>
    <div class="chip">${o.icone ?? CHECK}<span>${TXT.chip}</span></div></div>`);
  const q = s => document.querySelector(s);
  return { fd: q('#fd'), ov: q('#ov'), tit: q('.tit'), visor: q('.visor'), chip: q('.chip') };
}
// prende um rótulo num ponto do quadro (ax, ay: que ponto do rótulo cai ali)
export function prende(e, x, y, ax = .5, ay = 1) { e.style.left = (x - e.offsetWidth * ax).toFixed(1) + 'px'; e.style.top = (y - e.offsetHeight * ay).toFixed(1) + 'px'; }
export function sorteio(s = 20261118) { return () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
// avisa a folha (e o renderizador) que o painel está desenhado, com as fontes carregadas
export async function pronto() { await document.fonts.ready; await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); window.PRONTO = true; if (parent !== window) parent.postMessage({ pronto: location.pathname }, '*'); }
export const CORES_LATA = ['#C8553D', '#5B8FD6', '#3FA45B', '#F2B63D', '#E9EEF2', '#D9734A', '#50D088', '#2C5FA8', '#B23A48'];
