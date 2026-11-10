// Mapa de ruas ficticio (SVG) para os iframes/imagens de mapa: nada de logotipo nem tile real.
import { hash01 } from './geo.mjs';

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

/** SVG 960x600 de uma "vizinhanca" deterministica por `seed`, com alfinete vermelho no centro. */
export function fakeMapSvg(seed = 'mapa', label = '') {
  const W = 960;
  const H = 600;
  const r = (k) => hash01(seed, k);
  const angle = (r('ang') - 0.5) * 34;
  const streets = [];
  // ruas verticais e horizontais (em volta do centro, num grupo girado)
  let x = -300 + r('x0') * 60;
  let i = 0;
  while (x < W + 300) {
    streets.push(`<path d="M${x.toFixed(1)} -300V${H + 300}"/>`);
    x += 70 + r('dx' + i++) * 55;
  }
  let y = -300 + r('y0') * 50;
  i = 0;
  while (y < H + 300) {
    streets.push(`<path d="M-300 ${y.toFixed(1)}H${W + 300}"/>`);
    y += 62 + r('dy' + i++) * 48;
  }
  const parks = [0, 1, 2]
    .map((k) => {
      const px = 80 + r('px' + k) * (W - 260);
      const py = 60 + r('py' + k) * (H - 200);
      return `<rect x="${px.toFixed(0)}" y="${py.toFixed(0)}" width="${(90 + r('pw' + k) * 90).toFixed(0)}" height="${(60 + r('ph' + k) * 70).toFixed(0)}" rx="10"/>`;
    })
    .join('');
  const bayX = W * (0.64 + r('bay') * 0.1);
  const water = `M${bayX.toFixed(0)} ${H + 10} C ${(bayX + 40).toFixed(0)} ${(H * 0.7).toFixed(0)}, ${(bayX - 30).toFixed(0)} ${(H * 0.4).toFixed(0)}, ${(bayX + 60).toFixed(0)} -10 L ${W + 10} -10 L ${W + 10} ${H + 10} Z`;
  const main = `<path d="M-300 ${(H * 0.62).toFixed(0)} L ${W + 300} ${(H * 0.38).toFixed(0)}"/>`;
  const name = esc(String(label).split(',')[0].slice(0, 42));
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" width="100%" height="100%">
<rect width="${W}" height="${H}" fill="#ece8df"/>
<g transform="rotate(${angle.toFixed(1)} ${W / 2} ${H / 2})">
  <g fill="none" stroke="#d6d0c2" stroke-width="12" stroke-linecap="round">${streets.join('')}</g>
  <g fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round">${streets.join('')}</g>
  <g fill="#cfe5c4">${parks}</g>
  <g fill="none" stroke="#e5b84f" stroke-width="20" stroke-linecap="round">${main}</g>
  <g fill="none" stroke="#fbe3a0" stroke-width="15" stroke-linecap="round">${main}</g>
</g>
<path d="${water}" fill="#b6d3e8"/>
${name ? `<g font-family="Inter, Arial, sans-serif" font-size="15" fill="#5b5f66" text-anchor="middle"><text x="${W / 2}" y="${H / 2 + 54}" stroke="#fff" stroke-width="4" paint-order="stroke">${name}</text></g>` : ''}
<ellipse cx="${W / 2}" cy="${H / 2 + 2}" rx="12" ry="5" fill="#000" opacity=".22"/>
<path d="M${W / 2} ${H / 2} C ${W / 2 - 26} ${H / 2 - 24}, ${W / 2 - 24} ${H / 2 - 52}, ${W / 2} ${H / 2 - 52} C ${W / 2 + 24} ${H / 2 - 52}, ${W / 2 + 26} ${H / 2 - 24}, ${W / 2} ${H / 2} Z" fill="#e24b3c" stroke="#b83527" stroke-width="2"/>
<circle cx="${W / 2}" cy="${H / 2 - 33}" r="8" fill="#fff"/>
</svg>`;
}

/** Pagina HTML que cabe num iframe e mostra o mapa. */
export function fakeMapHtml(seed, label) {
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>html,body{margin:0;height:100%;overflow:hidden;background:#ece8df}svg{display:block}</style></head><body>${fakeMapSvg(seed, label)}</body></html>`;
}

/** Selo de favicon (a "logo do banco"): circulo neutro com a inicial do dominio. */
export function faviconSvg(domain = '?') {
  const letter = esc((String(domain).replace(/^www\./, '')[0] || '?').toUpperCase());
  const hue = Math.floor(hash01(domain, 'h') * 360);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"><circle cx="32" cy="32" r="30" fill="hsl(${hue},38%,88%)"/><text x="32" y="42" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="600" text-anchor="middle" fill="hsl(${hue},40%,32%)">${letter}</text></svg>`;
}

/** Alfinete e sombra no estilo do Leaflet (usados como <img>, entao SVG serve mesmo com extensao .png). */
export const LEAFLET_MARKER = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25 41" width="25" height="41"><path d="M12.5 0C5.6 0 0 5.6 0 12.5 0 22 12.5 41 12.5 41S25 22 25 12.5C25 5.6 19.4 0 12.5 0z" fill="#2b82cb" stroke="#1d5f98" stroke-width="1"/><circle cx="12.5" cy="12.5" r="5" fill="#fff"/></svg>`;
export const LEAFLET_SHADOW = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 41 41" width="41" height="41"><ellipse cx="13" cy="36" rx="13" ry="4.5" fill="#000" opacity=".28"/></svg>`;
