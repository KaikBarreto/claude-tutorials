// Utilitarios comuns do Supabase falso: ids, datas "relativas", tokens de seed.
import crypto from 'node:crypto';

export const TZ = 'America/Sao_Paulo';
const BR_OFFSET_MIN = -180; // Brasil sem horario de verao desde 2019

export function uuid() {
  return crypto.randomUUID();
}

/** UUID deterministico a partir de uma chave (mesma chave -> mesmo id, sempre). */
export function stableId(key) {
  const h = crypto.createHash('sha1').update('domiflix-fake:' + key).digest();
  h[6] = (h[6] & 0x0f) | 0x50; // versao 5
  h[8] = (h[8] & 0x3f) | 0x80;
  const x = h.subarray(0, 16).toString('hex');
  return `${x.slice(0, 8)}-${x.slice(8, 12)}-${x.slice(12, 16)}-${x.slice(16, 20)}-${x.slice(20, 32)}`;
}

/** "Agora" do mundo falso. FAKE_NOW=2026-10-29T14:00:00-03:00 congela o relogio do servidor; com FAKE_CLOCK=anda ele
 *  parte de FAKE_NOW e corre, recomecando a cada reset (/__dev/reset, que o robo chama no inicio de cada gravacao), como o
 *  relogio do navegador do robo. */
let ORIGEM = Date.now();
export function reiniciaRelogio() {
  ORIGEM = Date.now();
}
export function now() {
  if (process.env.FAKE_NOW) {
    const d = new Date(process.env.FAKE_NOW);
    if (!Number.isNaN(d.getTime())) return process.env.FAKE_CLOCK === 'anda' ? new Date(d.getTime() + Date.now() - ORIGEM) : d;
  }
  return new Date();
}
// o mesmo relogio para o codigo de um mundo fora de rec/fakebase (handlers que nao importam o nucleo)
globalThis.__fakebaseAgora = () => now().getTime();
export const nowIso = () => now().toISOString();

const pad = (n) => String(n).padStart(2, '0');

/** Data de calendario (YYYY-MM-DD) em Brasilia, deslocada em `days` dias. */
export function dateBR(days = 0, base = now()) {
  const t = new Date(base.getTime() + BR_OFFSET_MIN * 60000 + days * 86400000);
  return `${t.getUTCFullYear()}-${pad(t.getUTCMonth() + 1)}-${pad(t.getUTCDate())}`;
}

/** Instante ISO (UTC) de "dia + offset, HH:MM" em Brasilia. */
export function atBR(days, hhmm, base = now()) {
  const [h, m] = hhmm.split(':').map(Number);
  const day = dateBR(days, base);
  const [Y, M, D] = day.split('-').map(Number);
  return new Date(Date.UTC(Y, M - 1, D, h, m || 0, 0) - BR_OFFSET_MIN * 60000).toISOString();
}

const seqCounters = new Map();
export function resetSeq() {
  seqCounters.clear();
}

/**
 * Tokens de seed (strings dentro dos JSON em seeds/):
 *   "@id:cliente.padaria"   UUID estavel para a chave (use em id e nas FKs)      "@uuid"   UUID novo
 *   "@storage:company-logos/glacial/logo-horizontal.png"   URL publica de um arquivo em rec/fakebase/storage/
 *   "@today" "@today+3d" "@today-10d"      data (YYYY-MM-DD) relativa a hoje
 *   "@now" "@now-2h" "@now+30m" "@now-3d"  instante ISO relativo a agora
 *   "@at:+2d 09:30" "@at:-1d 14:00"        dia relativo + hora local (Brasilia) -> ISO
 *   "@month:+0:05" "@month:-1:20"          dia 05 do mes atual / dia 20 do mes anterior (YYYY-MM-DD)
 *   "@seq:os"                              inteiro sequencial por nome (1, 2, 3...)
 */
export function resolveToken(str) {
  if (typeof str !== 'string' || str[0] !== '@') return str;
  let m;
  if ((m = str.match(/^@id:(.+)$/))) return stableId(m[1]);
  if (str === '@uuid') return uuid(); // novo a cada linha (DEFAULT gen_random_uuid() de coluna que nao e o id)
  if ((m = str.match(/^@storage:(.+)$/))) return `http://${process.env.FAKE_HOST || '127.0.0.1'}:${process.env.FAKE_PORT || 54321}/storage/v1/object/public/${m[1]}`;
  if ((m = str.match(/^@today(?:([+-]\d+)d)?$/))) return dateBR(Number(m[1] || 0));
  if ((m = str.match(/^@now(?:([+-]\d+)([dhm]))?$/))) {
    if (!m[1]) return nowIso();
    const n = Number(m[1]);
    const ms = { d: 86400000, h: 3600000, m: 60000 }[m[2]];
    return new Date(now().getTime() + n * ms).toISOString();
  }
  if ((m = str.match(/^@at:([+-]?\d+)d\s+(\d{1,2}:\d{2})$/))) return atBR(Number(m[1]), m[2]);
  if ((m = str.match(/^@month:([+-]?\d+):(\d{1,2})$/))) {
    const base = dateBR(0).split('-').map(Number);
    const total = base[0] * 12 + (base[1] - 1) + Number(m[1]);
    const y = Math.floor(total / 12);
    const mo = (total % 12) + 1;
    return `${y}-${pad(mo)}-${pad(Number(m[2]))}`;
  }
  if ((m = str.match(/^@seq:(.+)$/))) {
    const n = (seqCounters.get(m[1]) || 0) + 1;
    seqCounters.set(m[1], n);
    return n;
  }
  return str;
}

export function resolveTokens(value) {
  if (typeof value === 'string') return resolveToken(value);
  if (Array.isArray(value)) return value.map(resolveTokens);
  if (value && typeof value === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(value)) out[k] = resolveTokens(v);
    return out;
  }
  return value;
}

export const clone = (v) => (v === undefined ? v : JSON.parse(JSON.stringify(v)));

export function isPlainObject(v) {
  return v !== null && typeof v === 'object' && !Array.isArray(v);
}

/** Codigo curto (public_short_code): 12 caracteres do alfabeto base32 sem 0/o/1/l/i — o app so reconhece esse formato
 *  (utils/prettyLinks.ts SHORT_CODE_RE). Deterministico se `seed` for passado. */
export function shortCode(seed, len = 12) {
  const alphabet = 'abcdefghjkmnpqrstuvwxyz23456789';
  const h = crypto.createHash('sha1').update(String(seed ?? crypto.randomUUID())).digest();
  let out = '';
  for (let i = 0; i < len; i++) out += alphabet[h[i] % alphabet.length];
  return out;
}

/** Corpo de resposta de erro no formato do PostgREST. */
export function pgError(code, message, details = null, hint = null) {
  return { code, details, hint, message };
}
