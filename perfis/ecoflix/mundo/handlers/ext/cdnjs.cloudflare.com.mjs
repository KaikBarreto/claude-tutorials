// cdnjs: só o Leaflet 1.9.4 do mapa do Rastreamento (T12), servido de storage/ecoflix/leaflet; o resto vira vazio.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'storage', 'ecoflix', 'leaflet');
export default async function cdnjs({ path: p }) {
  if (/leaflet\/1\.9\.4\/leaflet(\.min)?\.js$/.test(p)) return { __raw: true, type: 'application/javascript', body: fs.readFileSync(path.join(DIR, 'leaflet.js')) };
  if (/leaflet\/1\.9\.4\/leaflet(\.min)?\.css$/.test(p)) return { __raw: true, type: 'text/css', body: fs.readFileSync(path.join(DIR, 'leaflet.css')) };
  return { __raw: true, type: 'text/plain', body: '' };
}
