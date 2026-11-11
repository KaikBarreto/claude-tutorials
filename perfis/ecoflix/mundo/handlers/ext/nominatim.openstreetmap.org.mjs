// Nominatim falso do mundo da Recicla Vale Metais (sobrescreve o do núcleo para este host): o /reverse perto do pátio (até ~1,5 km da
// Rua das Oficinas, 1250, Taubaté) devolve o endereço do pátio, que o ponto pelo celular mostra no "Local" e grava na batida
// (utils/reverseGeocode.ts monta "Rua das Oficinas, 1250 - Parque Industrial - Taubaté"; T19 cap09). O resto vai para o do núcleo
// (o mapa sintético de Niterói).
import nucleo from '../../../fakebase/handlers/ext/nominatim.openstreetmap.org.mjs';

const PATIO = { lat: -23.0105, lon: -45.5412 };
const perto = (lat, lon) => Math.hypot((lat - PATIO.lat) * 111, (lon - PATIO.lon) * 102) <= 1.5;

export default async function nominatim(ctx) {
  const q = ctx.query || {};
  if (String(ctx.path || '').startsWith('/reverse') && perto(Number(q.lat), Number(q.lon))) {
    return {
      place_id: 920001, licence: 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', osm_type: 'way', osm_id: 5100001,
      lat: String(q.lat), lon: String(q.lon), class: 'building', type: 'industrial', importance: 0.3,
      display_name: '1250, Rua das Oficinas, Parque Industrial, Taubaté, Região Imediata de Taubaté, São Paulo, 12086-410, Brasil',
      address: { house_number: '1250', road: 'Rua das Oficinas', suburb: 'Parque Industrial', city: 'Taubaté', state: 'São Paulo',
        postcode: '12086-410', country: 'Brasil', country_code: 'br' },
    };
  }
  return nucleo(ctx);
}
