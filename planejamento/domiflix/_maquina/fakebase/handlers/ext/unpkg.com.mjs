// unpkg: so os icones do Leaflet (mapa do painel). Qualquer outra coisa vira vazio.
import { LEAFLET_MARKER, LEAFLET_SHADOW } from '../../lib/fakemap.mjs';

export default async function unpkg({ path }) {
  if (/marker-shadow\.png$/.test(path)) return { __raw: true, type: 'image/svg+xml', body: LEAFLET_SHADOW };
  if (/marker-icon(-2x)?\.png$/.test(path)) return { __raw: true, type: 'image/svg+xml', body: LEAFLET_MARKER };
  return { __raw: true, type: 'text/plain', body: '' };
}
