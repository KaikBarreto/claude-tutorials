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
  // 1.38.19: metodologia de BDI (20261102160000_quotes_use_bdi / 20261103133000_os_budget_bdi_methodology)
  quotes: { use_bdi: true },
  service_orders: { use_bdi: false, tax_rate: 10, admin_indirect_rate: 12, profit_rate: 10, bdi: 0.68, total_cost: 0, km_cost: 0, distance_km: 0, displacement_cost: 0, commercial_adjustment: 0 },
  service_order_budget_items: { pricing_mode: 'manual', bdi: 0.68, unit_hours: 0, unit_hourly_rate: 0, unit_labor_cost: 0, unit_materials_cost: 0, unit_extras_cost: 0, unit_total_cost: 0, profit_rate: 10 },
  equipment: { status: 'active', attachments_public: true },
  customers: {
    customer_type: 'pf',
    is_deleted: false,
    is_service_customer: true,
    is_store_customer: false,
    whatsapp_notifications_enabled: true,
    public_short_code: (row) => shortCode(row.id || row.name),
    custom_fields: () => ({}), // 1.38.8+: jsonb NOT NULL DEFAULT '{}'
  },
  // 1.38.8+ (etiquetas e campos personalizados de clientes/fornecedores; 1.38.9 acrescenta o escopo equipment):
  // a expressao ALWAYS_TRUE (abaixo) faria todo `show_*` nascer verdadeiro; no banco `show_in_portal` nasce FALSO.
  party_labels: { scope: 'party', show_in_portal: false, color: '#64748B', is_active: true },
  party_field_config: { field_type: 'text', is_visible: true, is_required: false, is_visible_in_portal: false, position: 0 },
  suppliers: { custom_fields: () => ({}) },
  customer_label_assignments: { position: 0 },
  supplier_label_assignments: { position: 0 },
  equipment_label_assignments: { position: 0 },
  equipment_field_config: { is_visible_in_portal: false }, // campo novo nasce privado (migration 20261031194500)
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
