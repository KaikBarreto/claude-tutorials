// /__tiles/* — no lugar do servidor de tiles (VITE_MAP_TILES_URL): estilos do MapLibre e a geometria da cidade.
import { unknown } from '../core/log.mjs';
import { send, sendJson } from './common.mjs';
import { cityGeoJson, styleFor } from '../lib/tiles.mjs';

export async function handleTiles(req, res, url) {
  const p = url.pathname.replace(/^\/__tiles\/?/, '');
  const base = `http://${req.headers.host || '127.0.0.1:54321'}/__tiles`;
  const m = p.match(/^styles\/([a-z-]+)$/);
  if (m) return sendJson(res, 200, styleFor(m[1] === 'dark' ? 'dark' : 'positron', base), { 'Cache-Control': 'max-age=300' });
  if (p === 'data/city.geojson') return send(res, 200, JSON.stringify(cityGeoJson()), { 'Content-Type': 'application/geo+json', 'Cache-Control': 'max-age=3600' });
  unknown('TILES_SEM_HANDLER', p || '/');
  return sendJson(res, 404, { error: 'tiles: rota desconhecida', path: p });
}
