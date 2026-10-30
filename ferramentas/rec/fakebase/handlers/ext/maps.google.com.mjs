// Iframe de mapa do Google (output=embed): devolve um mapa ficticio, sem marca.
import { fakeMapHtml } from '../../lib/fakemap.mjs';

export default async function mapsEmbed({ query }) {
  const q = String(query.q || query.query || 'mapa');
  return { __raw: true, type: 'text/html; charset=utf-8', body: fakeMapHtml(q, q) };
}
