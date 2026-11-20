// Tiles do mapa do Rastreamento (T12): um quadrado SVG 256x256 de ruas fictícias, claras, determinístico por z/x/y (nada de tile real).
import { hash01 } from '../../../fakebase/lib/geo.mjs';

export default async function tile({ path: p }) {
  const m = p.match(/tile\/(\d+)\/(\d+)\/(\d+)/);
  const seed = m ? `${m[1]}/${m[2]}/${m[3]}` : 'x';
  const r = (k) => hash01(seed, k);
  const ruas = [];
  let x = r('x0') * 40;
  for (let i = 0; x < 256; i++) { ruas.push(`<path d="M${x.toFixed(0)} 0V256"/>`); x += 46 + r('dx' + i) * 52; }
  let y = r('y0') * 40;
  for (let i = 0; y < 256; i++) { ruas.push(`<path d="M0 ${y.toFixed(0)}H256"/>`); y += 40 + r('dy' + i) * 48; }
  const verde = `<rect x="${(20 + r('px') * 120).toFixed(0)}" y="${(20 + r('py') * 120).toFixed(0)}" width="${(50 + r('pw') * 60).toFixed(0)}" height="${(34 + r('ph') * 50).toFixed(0)}" rx="6" fill="#dfe8dc"/>`;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><rect width="256" height="256" fill="#eef0f2"/>${verde}<g stroke="#ffffff" stroke-width="6" fill="none">${ruas.join('')}</g><g stroke="#d7dbe0" stroke-width="1" fill="none">${ruas.join('')}</g></svg>`;
  return { __raw: true, type: 'image/svg+xml', body: svg };
}
