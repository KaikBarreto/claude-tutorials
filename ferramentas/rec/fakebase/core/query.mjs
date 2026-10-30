// Execucao de SELECT: filtros, embeds (via Relationships), ordenacao, paginacao e projecao.
import { store } from './store.mjs';
import * as S from './schema.mjs';
import { parseSelect } from './select.mjs';
import { evalNodes, sortRows, getValue, newMods } from './filters.mjs';
import { unknown } from './log.mjs';
import { config } from './config.mjs';

/** Providers de views calculadas: nome -> (store) => linhas. Registrados por handlers/views/*.mjs. */
export const viewProviders = new Map();

export function rowsOf(name) {
  const provider = viewProviders.get(name);
  if (provider) return provider(store);
  return store.rows(name);
}

/** Linhas de `target` relacionadas a `row` (de `source`). null = sem relacionamento conhecido. */
export function resolveRelated(source, target, hints, row) {
  const e = S.findEmbed(source, target, hints);
  if (!e) return null;
  if (e.via === 'forward') {
    const { cols, toCols } = e.rel;
    const vals = cols.map((c) => row[c]);
    if (vals.some((v) => v === null || v === undefined)) return { rows: [], card: 'one' };
    const rows =
      cols.length === 1
        ? lookup(target, toCols[0], vals[0])
        : rowsOf(target).filter((r) => toCols.every((c, i) => r[c] === vals[i]));
    return { rows, card: 'one' };
  }
  if (e.via === 'reverse') {
    const { cols, toCols } = e.rel;
    const vals = toCols.map((c) => row[c]);
    if (vals.some((v) => v === null || v === undefined)) return { rows: [], card: e.cardinality };
    const rows =
      cols.length === 1
        ? lookup(target, cols[0], vals[0])
        : rowsOf(target).filter((r) => cols.every((c, i) => r[c] === vals[i]));
    return { rows, card: e.cardinality };
  }
  // muitos-para-muitos
  const { junction, toSource, toTarget } = e;
  const key = row[toSource.toCols[0]];
  const jrows = lookup(junction, toSource.cols[0], key);
  const out = [];
  for (const j of jrows) out.push(...lookup(target, toTarget.toCols[0], j[toTarget.cols[0]]));
  return { rows: out, card: 'many' };
}

function lookup(table, col, value) {
  if (viewProviders.has(table)) return rowsOf(table).filter((r) => String(r[col]) === String(value));
  return store.lookup(table, col, value);
}

const envFor = (table) => ({
  table,
  related: (t, row, embedName) => resolveRelated(t, embedName, [], row)?.rows || [],
});

function modsFor(mods, item) {
  if (!mods) return null;
  return mods.children.get(item.alias) || mods.children.get(item.name) || null;
}

/** Linhas do embed ja filtradas/ordenadas/limitadas segundo os modificadores. */
function embedRows(sourceTable, item, row, mods) {
  const res = resolveRelated(sourceTable, item.name, item.hints, row);
  if (!res) return null;
  const m = modsFor(mods, item);
  let rows = res.rows;
  if (m) {
    if (m.nodes.length) rows = rows.filter((r) => evalNodes(m.nodes, r, envFor(item.name)));
  }
  // embeds internos "inner" tambem filtram as linhas do embed
  const innerKids = item.children.filter((c) => c.kind === 'embed' && c.inner);
  if (innerKids.length) rows = rows.filter((r) => innerKids.every((k) => hasInner(item.name, k, r, m)));
  if (m) {
    if (m.order.length) rows = sortRows(rows, m.order);
    const off = m.offset || 0;
    if (off || m.limit !== null) rows = rows.slice(off, m.limit === null ? undefined : off + m.limit);
  }
  return { rows, card: res.card };
}

function hasInner(table, item, row, mods) {
  const r = embedRows(table, item, row, mods);
  return !r || r.rows.length > 0 || false;
}

function cast(v, type) {
  if (!type || v === null || v === undefined) return v;
  const t = type.toLowerCase();
  if (/^(text|varchar|char)/.test(t)) return String(v);
  if (/^(int|bigint|smallint|numeric|float|double|real|decimal)/.test(t)) return Number(v);
  if (t === 'date') return String(v).slice(0, 10);
  if (t === 'boolean' || t === 'bool') return v === true || v === 'true' || v === 't';
  return v;
}

/** Projeta uma linha segundo os itens do select (colunas, aliases, embeds). */
export function project(table, row, items, mods) {
  const out = {};
  for (const it of items) {
    if (it.kind === 'star') {
      for (const k of Object.keys(row)) out[k] = row[k];
    } else if (it.kind === 'field') {
      if (it.agg) continue; // agregados tratados em runSelect
      const v = getValue(row, it.name, it.json);
      const key = it.alias || (it.json.length ? it.json[it.json.length - 1].key : it.name);
      if (S.isKnown(table) && !it.json.length && !(it.name in S.columnsOf(table)) && row[it.name] === undefined) {
        unknown('COLUNA_FORA_DO_SCHEMA', `${table}.${it.name}`, 'select');
      }
      out[key] = cast(v, it.cast);
    } else if (it.kind === 'embed') {
      const key = it.alias || it.name;
      const res = embedRows(table, it, row, mods);
      if (!res) {
        unknown('EMBED_SEM_RELACIONAMENTO', `${table}->${it.name}`, `hints=${it.hints.join(',')}`);
        if (it.spread) continue;
        out[key] = [];
        continue;
      }
      const m = modsFor(mods, it);
      const agg = it.children.length === 1 && it.children[0].kind === 'field' && it.children[0].agg === 'count';
      if (agg) {
        out[key] = res.card === 'one' ? { count: res.rows.length } : [{ count: res.rows.length }];
        continue;
      }
      const projected = res.rows.map((r) => project(it.name, r, it.children, m));
      if (it.spread) {
        Object.assign(out, projected[0] || {});
      } else {
        out[key] = res.card === 'one' ? projected[0] ?? null : projected;
      }
    }
  }
  return out;
}

function aggregate(rows, items) {
  const groupFields = items.filter((i) => i.kind === 'field' && !i.agg);
  const aggFields = items.filter((i) => i.kind === 'field' && i.agg);
  const groups = new Map();
  for (const r of rows) {
    const gk = JSON.stringify(groupFields.map((f) => getValue(r, f.name, f.json)));
    if (!groups.has(gk)) groups.set(gk, []);
    groups.get(gk).push(r);
  }
  if (!rows.length && !groupFields.length) groups.set('[]', []);
  const out = [];
  for (const [, grp] of groups) {
    const o = {};
    for (const f of groupFields) o[f.alias || f.name] = grp.length ? getValue(grp[0], f.name, f.json) : null;
    for (const f of aggFields) {
      const vals = f.name ? grp.map((r) => getValue(r, f.name, f.json)).filter((v) => v !== null && v !== undefined) : grp;
      const nums = f.name ? vals.map(Number).filter((n) => !Number.isNaN(n)) : [];
      let v;
      switch (f.agg) {
        case 'count': v = f.name ? vals.length : grp.length; break;
        case 'sum': v = nums.length ? nums.reduce((a, b) => a + b, 0) : null; break;
        case 'avg': v = nums.length ? nums.reduce((a, b) => a + b, 0) / nums.length : null; break;
        case 'min': v = vals.length ? vals.reduce((a, b) => (a <= b ? a : b)) : null; break;
        case 'max': v = vals.length ? vals.reduce((a, b) => (a >= b ? a : b)) : null; break;
      }
      o[f.alias || f.agg] = v;
    }
    out.push(o);
  }
  return out;
}

/**
 * SELECT completo.
 * @param {string} table
 * @param {{select?:string, mods:object}} q  resultado de parseQuery
 * @param {{rangeFrom?:number, rangeTo?:number}} [opts]  cabecalho Range (alem de offset/limit)
 * @returns {{rows:object[], total:number, offset:number, raw:object[]}}
 */
export function runSelect(table, q, opts = {}) {
  const mods = q.mods || newMods();
  const items = parseSelect(q.select);
  const env = envFor(table);
  const innerItems = items.filter((i) => i.kind === 'embed' && i.inner);

  let matched = rowsOf(table);
  if (mods.nodes.length) matched = matched.filter((r) => evalNodes(mods.nodes, r, env));
  if (innerItems.length) matched = matched.filter((r) => innerItems.every((it) => hasInner(table, it, r, mods)));

  if (items.some((i) => i.kind === 'field' && i.agg)) {
    const rows = aggregate(matched, items);
    return { rows, total: rows.length, offset: 0, raw: matched };
  }

  const total = matched.length;
  if (mods.order.length) matched = sortRows(matched, mods.order);

  let offset = mods.offset || 0;
  let limit = mods.limit;
  if (opts.rangeFrom !== undefined) {
    offset = opts.rangeFrom;
    if (opts.rangeTo !== undefined) limit = limit === null ? opts.rangeTo - opts.rangeFrom + 1 : Math.min(limit, opts.rangeTo - opts.rangeFrom + 1);
  }
  const cap = config.maxRows;
  limit = limit === null || limit === undefined ? cap : Math.min(limit, cap);
  const page = matched.slice(offset, offset + limit);
  const rows = page.map((r) => project(table, r, items, mods));
  return { rows, total, offset, raw: page };
}

/** Projecao de linhas ja materializadas (resposta de insert/update/delete com return=representation). */
export function projectRows(table, rows, selectStr, mods) {
  const items = parseSelect(selectStr);
  return rows.map((r) => project(table, r, items, mods || newMods()));
}

/** Aplica select/filtros/ordem/paginacao a um array qualquer (resultado de RPC que devolve tabela). */
export function runOnArray(rows, q) {
  const mods = q.mods || newMods();
  const items = parseSelect(q.select);
  let m = rows;
  if (mods.nodes.length) m = m.filter((r) => evalNodes(mods.nodes, r, { table: null, related: () => [] }));
  const total = m.length;
  if (mods.order.length) m = sortRows(m, mods.order);
  const off = mods.offset || 0;
  m = m.slice(off, mods.limit === null ? undefined : off + mods.limit);
  const hasProjection = !(items.length === 1 && items[0].kind === 'star');
  const out = hasProjection ? m.map((r) => project('__array__', r, items, mods)) : m;
  return { rows: out, total };
}
