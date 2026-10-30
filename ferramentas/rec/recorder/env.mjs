// Enderecos e chave falsa compartilhados (fonte unica: rec/env.json, lido tambem por rec/run.sh).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
export const REC_DIR = path.resolve(here, '..');
const file = JSON.parse(fs.readFileSync(path.join(REC_DIR, 'env.json'), 'utf8'));

export const FAKE_URL = process.env.FAKE_URL || file.fakeUrl;
/** Endereço do Supabase falso gravado no build do app (o robô desvia para FAKE_URL quando for outra instância). */
export const BAKED_FAKE_URL = file.fakeUrl;
export const APP_URL = process.env.APP_URL || file.appUrl;
export const ANON_KEY = file.anonKey;
export const RUNTIME_DIR = path.join(REC_DIR, '.runtime');
export const USER_EMAIL = process.env.FAKE_USER_EMAIL || 'camila.duarte@glacialcold.example';
fs.mkdirSync(RUNTIME_DIR, { recursive: true });

export const MODES = ['fakebase', 'url'];

/**
 * Modo de gravacao: `fakebase` (Dominex + Supabase falso; padrao) ou `url` (o app de qualquer pessoa, por endereco).
 * Origem, da mais forte para a mais fraca: roteiro (`"mode"`) > variavel de ambiente REC_MODE > env.json (`"mode"`).
 * Devolve { mode, source } (source diz de onde veio, para a mensagem de log); valor desconhecido lanca erro claro.
 */
export function resolveMode(script) {
  const tries = [
    ['roteiro ("mode")', script?.mode],
    ['variavel de ambiente REC_MODE', process.env.REC_MODE],
    ['env.json ("mode")', file.mode],
  ];
  const hit = tries.find(([, v]) => v !== undefined && v !== null && String(v).trim() !== '');
  if (!hit) return { mode: 'fakebase', source: 'padrao' };
  const mode = String(hit[1]).trim().toLowerCase();
  if (!MODES.includes(mode)) throw new Error(`modo "${hit[1]}" desconhecido (vindo de ${hit[0]}); validos: ${MODES.join(', ')}`);
  return { mode, source: hit[0] };
}
