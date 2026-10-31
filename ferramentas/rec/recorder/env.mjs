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
/** Endereço do app LOCAL de verdade (servidor estático do build; por padrão http://127.0.0.1:8080). */
export const LOCAL_APP_URL = process.env.APP_URL || file.appUrl;

/**
 * APP_ORIGIN (opcional; DESLIGADO por padrão): origem "de produto" que o navegador mostra para o app, ex.:
 *   APP_ORIGIN=https://www.dominex.app node rec/record.mjs rec/tNN/capMM.json ...
 * Com ela, o navegador abre o app nesse endereço e o gravador serve tudo a partir do app local (LOCAL_APP_URL) por
 * `context.route`, como já faz com o Supabase falso: a requisição não vai para a rede (sem certificado nem servidor https).
 * Serve para os links que aparecem na tela (Link do portal, QR de equipamento, link do contrato...) saírem com o domínio
 * do produto em vez de 127.0.0.1:8080. Sem a variável nada muda. Só vale no modo fakebase. Ver docs/04-gravacao.md.
 */
export const APP_ORIGIN = resolveAppOrigin(process.env.APP_ORIGIN);

/** Endereço que o NAVEGADOR usa para abrir o app (goto, localStorage da sessão): APP_ORIGIN quando ligada, senão o local. */
export const APP_URL = APP_ORIGIN || LOCAL_APP_URL;

function resolveAppOrigin(raw) {
  const v = String(raw ?? '').trim();
  if (!v) return '';
  let u;
  try {
    u = new URL(v);
  } catch (e) {
    throw new Error(`APP_ORIGIN invalida: "${v}" (ex.: APP_ORIGIN=https://www.dominex.app)`);
  }
  if (!/^https?:$/.test(u.protocol)) throw new Error(`APP_ORIGIN precisa começar com http:// ou https:// (veio "${v}")`);
  if ((u.pathname !== '/' && u.pathname !== '') || u.search || u.hash || u.username || u.password) {
    throw new Error(`APP_ORIGIN deve ser só a origem (esquema + domínio), sem caminho nem usuário:senha (veio "${v}")`);
  }
  if (['127.0.0.1', 'localhost', '[::1]', '::1'].includes(u.hostname)) {
    throw new Error('APP_ORIGIN precisa ser um endereço de produto, não local (o app local já é o padrão)');
  }
  return u.origin;
}
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
