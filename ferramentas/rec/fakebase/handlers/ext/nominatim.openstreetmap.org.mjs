// Nominatim falso: /search (autocompletar e geocodificacao) e /reverse
import { CITY, HOODS, fmtCep, gazetteer, hash01, houseNumber, norm, onlyDigits, pointNear, searchStreets, km } from '../../lib/geo.mjs';

const item = (g, number, i) => ({
  place_id: 910000 + i,
  licence: 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
  osm_type: 'way',
  osm_id: 5000000 + i,
  lat: String(g.lat),
  lon: String(g.lon),
  class: 'highway',
  type: 'residential',
  importance: 0.6 - i * 0.05,
  display_name: [number ? `${g.road}` : g.road, number, g.hood, g.city || CITY.name, 'Região Geográfica Imediata do Rio de Janeiro', CITY.state, fmtCep(onlyDigits(g.cep)) || '24000-000', 'Brasil'].filter(Boolean).join(', '),
  address: {
    road: g.road,
    ...(number ? { house_number: number } : {}),
    suburb: g.hood,
    city: g.city || CITY.name,
    state: CITY.state,
    postcode: fmtCep(onlyDigits(g.cep)) || '24000-000',
    country: 'Brasil',
    country_code: 'br',
  },
});

export default async function nominatim({ path, query }) {
  if (path.startsWith('/search')) {
    const q = String(query.q || '');
    const limit = Math.max(1, Math.min(10, Number(query.limit) || 5));
    const number = houseNumber(q);
    let found = searchStreets(q, limit);
    if (!found.length && norm(q).length >= 4) {
      // rua desconhecida: devolve um ponto generico em Niteroi para a demonstracao nao travar
      const road = q.split(',')[0].trim() || 'Rua Exemplo';
      const hood = Object.keys(HOODS)[Math.floor(norm(road).length) % Object.keys(HOODS).length];
      const [lat, lon] = pointNear(hood, road);
      found = [{ road, hood, cep: '', lat, lon, city: CITY.name }];
    }
    return found.map((g, i) => {
      // com numero de casa, desloca de leve (~30 m) para cada numero cair num ponto diferente da rua
      const lat = number ? g.lat + (hash01(g.road, number) - 0.5) * 0.0006 : g.lat;
      const lon = number ? g.lon + (hash01(g.road, number + 'x') - 0.5) * 0.0006 : g.lon;
      return item({ ...g, lat, lon }, number, i);
    });
  }
  if (path.startsWith('/reverse')) {
    const lat = Number(query.lat);
    const lon = Number(query.lon);
    const all = gazetteer();
    let best = all[0];
    let bd = Infinity;
    for (const g of all) {
      const d = km([lat, lon], [g.lat, g.lon]);
      if (d < bd) {
        bd = d;
        best = g;
      }
    }
    return { ...item(best, '', 0), lat: String(lat), lon: String(lon) };
  }
  return [];
}
