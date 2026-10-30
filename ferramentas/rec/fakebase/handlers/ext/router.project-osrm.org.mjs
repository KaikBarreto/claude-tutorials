// OSRM falso: /route/v1/driving/<lon1>,<lat1>;<lon2>,<lat2> -> rota sintetica "em L" com curvas suaves
import { km } from '../../lib/geo.mjs';

export default async function osrm({ path }) {
  const m = path.match(/^\/route\/v1\/[a-z]+\/(-?\d+\.?\d*),(-?\d+\.?\d*);(-?\d+\.?\d*),(-?\d+\.?\d*)/);
  if (!m) return { code: 'InvalidUrl', message: 'URL sem coordenadas' };
  const [lon1, lat1, lon2, lat2] = m.slice(1).map(Number);
  // sai pela latitude, vira na esquina e chega pela longitude; subdivide para parecer uma rota de ruas
  const corner = [lon1, lat2];
  const seg = (a, b, n) => Array.from({ length: n }, (_, i) => [a[0] + ((b[0] - a[0]) * i) / n, a[1] + ((b[1] - a[1]) * i) / n]);
  const coords = [...seg([lon1, lat1], corner, 6), ...seg(corner, [lon2, lat2], 6), [lon2, lat2]];
  const dist = km([lat1, lon1], [lat2, lon2]) * 1.38 * 1000; // metros
  return {
    code: 'Ok',
    routes: [{ geometry: { type: 'LineString', coordinates: coords }, legs: [], weight_name: 'routability', weight: dist / 9, duration: dist / 8.3, distance: dist }],
    waypoints: [
      { hint: '', distance: 4, name: '', location: [lon1, lat1] },
      { hint: '', distance: 4, name: '', location: [lon2, lat2] },
    ],
  };
}
