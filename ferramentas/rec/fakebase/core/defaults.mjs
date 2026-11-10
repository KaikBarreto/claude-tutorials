// Valores padrao ao inserir linhas (o que o Postgres faria com DEFAULTs e triggers).
// O schema (types.ts) diz QUAIS colunas tem default (o:1), mas nao o valor; aqui chutamos
// pelo tipo e pelo nome, e cada tabela pode sobrescrever em TABLE_DEFAULTS.
import { columnsOf, enums } from './schema.mjs';
import { config } from './config.mjs';
import { uuid, nowIso, shortCode, resolveTokens } from './util.mjs';
import { mundo } from './mundo.mjs';

/**
 * Defaults por tabela: { coluna: valor | (row, ctx) => valor }.
 * Acrescente aqui quando uma tabela precisar de default especifico (ex.: sequencias do banco).
 */
export const TABLE_DEFAULTS = {
  equipment: { status: 'active', attachments_public: true },
  customers: {
    customer_type: 'pf',
    is_deleted: false,
    is_service_customer: true,
    is_store_customer: false,
    whatsapp_notifications_enabled: true,
    public_short_code: (row) => shortCode(row.id || row.name),
  },
};

const ALWAYS_TRUE = /^(is_active|active|ativo|enabled|is_enabled|visible|is_visible|show_.+)$/;
const SEQ = new Map();
/** Numeracao sequencial por tabela+coluna (ex.: numero da OS), comecando acima do que ja existe. */
export function nextSeq(table, col, rows) {
  const key = `${table}.${col}`;
  let n = SEQ.get(key);
  if (n === undefined) n = rows.reduce((mx, r) => (typeof r[col] === 'number' && r[col] > mx ? r[col] : mx), 0);
  n += 1;
  SEQ.set(key, n);
  return n;
}
export function resetSeqs() {
  SEQ.clear();
}

/** Preenche o que faltar numa linha nova e normaliza para ter TODAS as colunas do schema. */
export function applyDefaults(table, input, ctx = {}) {
  const cols = columnsOf(table);
  const row = { ...input };
  const has = (k) => Object.prototype.hasOwnProperty.call(cols, k);
  const absent = (k) => row[k] === undefined;

  if (has('id') && absent('id')) row.id = uuid();
  const stamp = nowIso();
  if (has('created_at') && absent('created_at')) row.created_at = stamp;
  if (has('updated_at') && absent('updated_at')) row.updated_at = stamp;
  if (has('company_id') && absent('company_id')) row.company_id = ctx.companyId || config.companyId;

  const specific = (mundo.defaults ? mundo.defaults[table] : TABLE_DEFAULTS[table]) || {}; // FAKE_MUNDO: os do mundo.json
  for (const [k, v] of Object.entries(specific)) {
    if (absent(k)) row[k] = typeof v === 'function' ? v(row, ctx) : resolveTokens(v);
  }

  for (const [k, def] of Object.entries(cols)) {
    if (!absent(k)) continue;
    // links amigaveis: o banco gera o public_short_code (12 caracteres base32) num trigger
    if (/(^|_)short_code$/.test(k) && def.t === 'string') {
      row[k] = shortCode(row.id || uuid());
      continue;
    }
    if (def.o === 1) {
      // coluna com DEFAULT no banco: valor plausivel pelo tipo
      if (def.t === 'boolean') row[k] = ALWAYS_TRUE.test(k);
      else if (def.t === 'number') row[k] = 0;
      else if (def.t === 'array') row[k] = [];
      else if (def.t.startsWith('enum:')) row[k] = enums[def.t.slice(5)]?.[0] ?? null;
      else row[k] = null;
    } else {
      row[k] = null;
    }
  }
  return row;
}
