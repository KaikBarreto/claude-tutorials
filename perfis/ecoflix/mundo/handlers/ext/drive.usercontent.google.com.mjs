// drive.usercontent.google.com/download?id=...: o player da EcoFlix toca o vídeo "do Drive"; no mundo falso é um arquivo local, mudo
// (storage/ecoflix/aula-ficticia*.webm: fundo verde-escuro, sem imagem de terceiros, 12 min). IDs com "vertical" servem o 9:16.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'storage', 'ecoflix');
export default async function drive({ query }) {
  const arq = path.join(DIR, /vertical/i.test(String(query.id || '')) ? 'aula-ficticia-vertical.webm' : 'aula-ficticia.webm');
  if (!fs.existsSync(arq)) return { __status: 404, body: { message: 'vídeo fictício ainda não gerado' } };
  return { __raw: true, type: 'video/webm', body: fs.readFileSync(arq) };
}
