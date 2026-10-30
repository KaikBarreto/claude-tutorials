// INSERT / UPSERT / UPDATE / DELETE em memoria, com defaults e hooks por tabela (hooks/<tabela>.mjs).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { store } from './store.mjs';
import { applyDefaults, nextSeq } from './defaults.mjs';
import { evalNodes } from './filters.mjs';
import { isKnown, columnsOf } from './schema.mjs';
import { rowsOf, resolveRelated } from './query.mjs';
import { nowIso, uuid, pgError } from './util.mjs';
import { config } from './config.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const hooks = new Map();

export async function loadHooks(dir = path.resolve(here, '../hooks')) {
  hooks.clear();
  if (!fs.existsSync(dir)) return;
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.mjs'))) {
    const mod = await import(pathToFileURL(path.join(dir, f)).href);
    hooks.set(f.replace(/\.mjs$/, ''), mod.default || mod);
  }
}

export class HttpError extends Error {
  constructor(status, body) {
    super(body?.message || 'erro');
    this.status = status;
    this.body = body;
  }
}

const envFor = (table) => ({ table, related: (t, row, name) => resolveRelated(t, name, [], row)?.rows || [] });

function hookCtx(ctx) {
  return { store, companyId: ctx?.companyId || config.companyId, userId: ctx?.userId || config.userId, nextSeq, uuid, nowIso };
}

function pkConflict(table, row) {
  if (row.id === undefined || row.id === null) return false;
  return store.lookup(table, 'id', row.id).length > 0;
}

/** Insere linhas (e faz upsert se `upsert` for passado). Devolve as linhas gravadas/atualizadas. */
export function insertRows(table, body, q, ctx, upsert = null) {
  const list = Array.isArray(body) ? body : [body];
  const h = hooks.get(table);
  const hc = hookCtx(ctx);
  const out = [];
  for (const inputRaw of list) {
    let input = { ...inputRaw };
    if (q.columns) input = Object.fromEntries(Object.entries(input).filter(([k]) => q.columns.includes(k)));
    if (upsert) {
      const keys = q.onConflict || ['id'];
      if (keys.every((k) => input[k] !== undefined && input[k] !== null)) {
        const existing = rowsOf(table).find((r) => keys.every((k) => String(r[k]) === String(input[k])));
        if (existing) {
          if (upsert === 'ignore') continue;
          const patch = { ...input };
          h?.beforeUpdate?.(existing, patch, hc);
          Object.assign(existing, patch);
          if (columnsOf(table).updated_at && inputRaw.updated_at === undefined) existing.updated_at = nowIso();
          store.table(table).touch();
          h?.afterUpdate?.(existing, hc);
          out.push(existing);
          continue;
        }
      }
    }
    const row = applyDefaults(table, input, ctx);
    if (!isKnown(table) && row.id === undefined) row.id = uuid();
    if (pkConflict(table, row)) {
      throw new HttpError(409, pgError('23505', `duplicate key value violates unique constraint "${table}_pkey"`, `Key (id)=(${row.id}) already exists.`));
    }
    h?.beforeInsert?.(row, hc);
    store.insertRaw(table, row);
    h?.afterInsert?.(row, hc);
    out.push(row);
  }
  return out;
}

export function updateRows(table, patchRaw, q, ctx) {
  const h = hooks.get(table);
  const hc = hookCtx(ctx);
  const env = envFor(table);
  const nodes = q.mods.nodes;
  const targets = rowsOf(table).filter((r) => evalNodes(nodes, r, env));
  const patch = { ...patchRaw };
  for (const k of Object.keys(patch)) if (patch[k] === undefined) delete patch[k];
  for (const r of targets) {
    const p = { ...patch };
    h?.beforeUpdate?.(r, p, hc);
    Object.assign(r, p);
    if (columnsOf(table).updated_at && patch.updated_at === undefined) r.updated_at = nowIso();
    h?.afterUpdate?.(r, hc);
  }
  if (targets.length) store.table(table).touch();
  return targets;
}

export function deleteRows(table, q, ctx) {
  const h = hooks.get(table);
  const hc = hookCtx(ctx);
  const env = envFor(table);
  const t = store.table(table);
  const gone = [];
  t.rows = t.rows.filter((r) => {
    if (evalNodes(q.mods.nodes, r, env)) {
      gone.push(r);
      return false;
    }
    return true;
  });
  if (gone.length) {
    t.touch();
    for (const r of gone) h?.afterDelete?.(r, hc);
  }
  return gone;
}
