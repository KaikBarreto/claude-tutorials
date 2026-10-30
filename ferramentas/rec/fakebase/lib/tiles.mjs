// Mapa base ficticio de Niteroi para o MapLibre (no lugar do OpenFreeMap): baia, oceano, parques e ruas geradas
// por uma semente fixa. Sem texto (nao precisa de fontes). O app pede /__tiles/styles/{positron|dark}.
import { HOODS, hash01 } from './geo.mjs';

const BAY = [
  [-43.4, -22.7], [-43.14, -22.7], [-43.14, -22.87], [-43.1385, -22.89], [-43.1345, -22.9035], [-43.13, -22.9135],
  [-43.121, -22.9255], [-43.109, -22.9365], [-43.099, -22.947], [-43.1075, -22.956], [-43.125, -22.962],
  [-43.15, -22.97], [-43.18, -23.0], [-43.4, -23.05],
];
const OCEAN = [
  [-43.16, -22.985], [-43.1, -22.972], [-43.06, -22.9745], [-43.03, -22.978], [-42.99, -22.976], [-42.9, -22.98],
  [-42.9, -23.1], [-43.16, -23.1],
];

const ring = (pts) => [[...pts, pts[0]]];
const poly = (kind, pts) => ({ type: 'Feature', properties: { kind }, geometry: { type: 'Polygon', coordinates: ring(pts) } });
const line = (kind, pts) => ({ type: 'Feature', properties: { kind }, geometry: { type: 'LineString', coordinates: pts } });

function rounded(cx, cy, w, h, n = 8) {
  const pts = [];
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2;
    pts.push([cx + Math.cos(a) * w * (0.85 + 0.15 * Math.abs(Math.cos(2 * a))), cy + Math.sin(a) * h * (0.85 + 0.15 * Math.abs(Math.sin(2 * a)))]);
  }
  return pts;
}

let cache = null;
export function cityGeoJson() {
  if (cache) return cache;
  const feats = [];
  const hoods = Object.entries(HOODS);
  // ruas locais: grade levemente girada em torno de cada bairro
  hoods.forEach(([name, [lat, lon]], hi) => {
    const ang = ((hash01(name, 'ang') - 0.5) * 30 * Math.PI) / 180;
    const cos = Math.cos(ang);
    const sin = Math.sin(ang);
    const step = 0.00115;
    const span = 11;
    const rot = (u, v) => [lon + (u * cos - v * sin) / 0.93, lat + u * sin + v * cos]; // 0.93 ~ cos(lat) para manter ruas quadradas
    for (let k = -span; k <= span; k++) {
      const jitter = (hash01(name, 'g' + k) - 0.5) * 0.0004;
      feats.push(line('road', [rot(-span * step, k * step + jitter), rot(span * step, k * step + jitter)]));
      feats.push(line('road', [rot(k * step + jitter, -span * step), rot(k * step + jitter, span * step)]));
    }
    // um parque por bairro, perto do centro
    feats.push(poly('park', rounded(lon + (hash01(name, 'px') - 0.5) * 0.008, lat + (hash01(name, 'py') - 0.5) * 0.008, 0.0016 + hash01(name, 'pw') * 0.0012, 0.0011 + hash01(name, 'ph') * 0.0008)));
    void hi;
  });
  // avenidas principais ligando os bairros (de oeste para leste, com curvas)
  const sorted = hoods.map(([n, [la, lo]]) => [lo, la, n]).sort((a, b) => a[0] - b[0]);
  const major = sorted.map(([lo, la], i) => [lo + (hash01('maj', 'x' + i) - 0.5) * 0.002, la + (hash01('maj', 'y' + i) - 0.5) * 0.002]);
  feats.push(line('road_major', major));
  feats.push(line('road_major', [major[0], [major[0][0] + 0.012, major[0][1] + 0.02], [major[0][0] + 0.03, major[0][1] + 0.05]]));
  feats.push(line('road_major', [major[major.length - 1], [major[major.length - 1][0] + 0.03, major[major.length - 1][1] - 0.008]]));
  feats.push(poly('water', BAY));
  feats.push(poly('water', OCEAN));
  cache = { type: 'FeatureCollection', features: feats };
  return cache;
}

const PALETTES = {
  positron: { land: '#f4f2ec', park: '#dcebd3', roadCasing: '#e1ddd2', road: '#ffffff', majorCasing: '#e6c26b', major: '#fbe7ae', water: '#c6ddee' },
  dark: { land: '#20242a', park: '#25332b', roadCasing: '#15181c', road: '#30353c', majorCasing: '#15181c', major: '#454b55', water: '#0e1722' },
};

export function styleFor(name, base) {
  const p = PALETTES[name] || PALETTES.positron;
  const f = (kind) => ['==', ['get', 'kind'], kind];
  const w = (a, b, c) => ['interpolate', ['linear'], ['zoom'], 9, a, 14, b, 18, c];
  return {
    version: 8,
    name: `dominex-fake-${name}`,
    sources: { city: { type: 'geojson', data: `${base}/data/city.geojson`, maxzoom: 14 } },
    layers: [
      { id: 'bg', type: 'background', paint: { 'background-color': p.land } },
      { id: 'park', type: 'fill', source: 'city', filter: f('park'), paint: { 'fill-color': p.park } },
      { id: 'road-casing', type: 'line', source: 'city', filter: f('road'), layout: { 'line-cap': 'round' }, paint: { 'line-color': p.roadCasing, 'line-width': w(0.5, 3.2, 12) } },
      { id: 'road', type: 'line', source: 'city', filter: f('road'), layout: { 'line-cap': 'round' }, paint: { 'line-color': p.road, 'line-width': w(0.3, 2, 9) } },
      { id: 'major-casing', type: 'line', source: 'city', filter: f('road_major'), layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': p.majorCasing, 'line-width': w(1.4, 6, 20) } },
      { id: 'major', type: 'line', source: 'city', filter: f('road_major'), layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': p.major, 'line-width': w(0.9, 4.2, 15) } },
      { id: 'water', type: 'fill', source: 'city', filter: f('water'), paint: { 'fill-color': p.water } },
    ],
  };
}
