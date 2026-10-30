// Registro do que o Supabase falso nao sabe responder -> desconhecidos.log.
// E assim que se descobre o que falta semear ou implementar.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
export const LOG_PATH = process.env.FAKE_UNKNOWN_LOG || path.resolve(here, '../desconhecidos.log');

const seen = new Map(); // "KIND\tnome" -> { count, first, sample }
let started = false;

export function startLog() {
  if (started) return;
  started = true;
  const header = `# servidor iniciado em ${new Date().toISOString()}\n# formato: instante<TAB>TIPO<TAB>nome<TAB>detalhe\n`;
  if (process.env.FAKE_KEEP_LOG === '1') fs.appendFileSync(LOG_PATH, header);
  else fs.writeFileSync(LOG_PATH, header);
}

/**
 * Registra um item desconhecido (uma linha por TIPO+nome; repeticoes so incrementam o contador).
 * Tipos usados: TABELA_DESCONHECIDA, TABELA_SEM_SEED, RPC_SEM_HANDLER, FUNCTION_SEM_HANDLER,
 * COLUNA_FORA_DO_SCHEMA, EMBED_SEM_RELACIONAMENTO, STORAGE_ARQUIVO_AUSENTE, AUTH_SEM_HANDLER,
 * EXTERNO_SEM_HANDLER, ROTA_DESCONHECIDA.
 */
export function unknown(kind, name, detail = '') {
  startLog();
  const key = `${kind}\t${name}`;
  const hit = seen.get(key);
  if (hit) {
    hit.count++;
    return;
  }
  const entry = { count: 1, first: new Date().toISOString(), detail: String(detail).slice(0, 300) };
  seen.set(key, entry);
  const line = `${entry.first}\t${kind}\t${name}\t${entry.detail.replace(/\s+/g, ' ')}\n`;
  fs.appendFileSync(LOG_PATH, line);
  if (process.env.FAKE_VERBOSE !== '0') console.log(`[desconhecido] ${kind} ${name} ${entry.detail ? '(' + entry.detail.slice(0, 120) + ')' : ''}`);
}

export function unknownSummary() {
  return [...seen.entries()].map(([k, v]) => {
    const [kind, name] = k.split('\t');
    return { kind, name, count: v.count, first: v.first, detail: v.detail };
  });
}

export function clearUnknown() {
  seen.clear();
  started = false;
  startLog();
}
