// Filtros, ordenacao e paginacao do PostgREST (query string -> AST -> avaliacao em memoria).
//
// Operadores: eq neq gt gte lt lte like ilike match imatch in is isdistinct cs cd ov fts plfts phfts wfts
//             (todos aceitam o prefixo `not.`); like(any|all)/ilike(any|all); sl sr nxl nxr adj (so aproximados).
// Logica: or=(a.eq.1,and(b.gt.2,c.lt.3))  and=(...)  not.or=(...)  e versoes por embed: `tabela.or=(...)`.
// Embeds: `tabela.col=eq.x`, `tabela.order=col.asc`, `tabela.limit=3`, `tabela.offset=1`.
import { splitTop } from './select.mjs';

const OPS = new Set([
  'eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'like', 'ilike', 'match', 'imatch', 'in', 'is', 'isdistinct',
  'cs', 'cd', 'ov', 'sl', 'sr', 'nxl', 'nxr', 'adj', 'fts', 'plfts', 'phfts', 'wfts',
]);
const OP_RE = /^(like|ilike)\((any|all)\)$/;
const FTS_RE = /^(fts|plfts|phfts|wfts)(?:\([^)]*\))?$/;

export function newMods() {
  return { nodes: [], order: [], limit: null, offset: null, children: new Map() };
}

function childMods(mods, path) {
  let m = mods;
  for (const seg of path) {
    if (!m.children.has(seg)) m.children.set(seg, newMods());
    m = m.children.get(seg);
  }
  return m;
}

function parseColumnRef(ref) {
  // "customers.name" | "data->>x" | "customers.data->k->>x"
  const arrow = ref.indexOf('->');
  const head = arrow >= 0 ? ref.slice(0, arrow) : ref;
  const tail = arrow >= 0 ? ref.slice(arrow) : '';
  const segs = head.split('.');
  const col = segs.pop();
  const json = [];
  let p = 0;
  while (p < tail.length) {
    const op = tail.startsWith('->>', p) ? '->>' : '->';
    const start = p + op.length;
    let next = tail.indexOf('->', start);
    if (next < 0) next = tail.length;
    json.push({ op, key: tail.slice(start, next).replace(/^"|"$/g, '') });
    p = next;
  }
  return { path: segs, col, json };
}

/** "op.valor" | "not.op.valor" -> { op, not, value, quant } */
function parseOpValue(s) {
  let not = false;
  let rest = s;
  if (rest.startsWith('not.')) {
    not = true;
    rest = rest.slice(4);
  }
  const dot = rest.indexOf('.');
  if (dot < 0) return null;
  let opWord = rest.slice(0, dot);
  const value = rest.slice(dot + 1);
  let quant = null;
  const q = opWord.match(OP_RE);
  if (q) {
    opWord = q[1];
    quant = q[2];
  }
  const f = opWord.match(FTS_RE);
  if (f) opWord = f[1];
  if (!OPS.has(opWord)) return null;
  return { op: opWord, not, value, quant };
}

/** Termo dentro de or=(...)/and=(...): `col.op.valor` | `and(...)` | `or(...)` | `not.and(...)` */
function parseLogicTerm(term) {
  const t = term.trim();
  let m = t.match(/^(not\.)?(and|or)\((.*)\)$/s);
  if (m) {
    return { t: m[2], not: !!m[1], path: [], items: splitTop(m[3]).map(parseLogicTerm).filter(Boolean) };
  }
  // descobre onde esta o operador: primeiro segmento que seja operador (ou `not` + operador)
  const parts = t.split('.');
  for (let i = 1; i < parts.length; i++) {
    const w = parts[i];
    const isNot = w === 'not' && i + 1 < parts.length;
    const opw = (isNot ? parts[i + 1] : w).replace(OP_RE, '$1').replace(FTS_RE, '$1');
    if (OPS.has(opw)) {
      const ref = parseColumnRef(parts.slice(0, i).join('.'));
      const ov = parseOpValue(parts.slice(i).join('.'));
      if (!ov) return null;
      // valor entre aspas dentro de or=(...) (PostgREST: `name.ilike."%x%"`, usePartnerSearch do app): tira as aspas (T13, 11/11)
      if (typeof ov.value === 'string' && ov.value.length >= 2 && ov.value[0] === '"' && ov.value.endsWith('"')) ov.value = ov.value.slice(1, -1).replace(/\\(["\\])/g, '$1');
      return { t: 'cond', ...ref, ...ov };
    }
  }
  return null;
}

function parseLogic(kind, notFlag, value, path) {
  const inner = value.trim().replace(/^\((.*)\)$/s, '$1');
  const items = splitTop(inner).map(parseLogicTerm).filter(Boolean);
  return { t: kind, not: notFlag, path, items };
}

export function parseOrder(str) {
  return splitTop(str)
    .map((term) => {
      const parts = term.trim().split('.');
      const ref = parts[0];
      let desc = false;
      let nulls = null;
      for (const p of parts.slice(1)) {
        if (p === 'desc') desc = true;
        else if (p === 'nullsfirst') nulls = 'first';
        else if (p === 'nullslast') nulls = 'last';
      }
      const { col, json } = parseColumnRef(ref);
      return { col, json, desc, nulls };
    })
    .filter((o) => o.col);
}

/**
 * URLSearchParams -> consulta estruturada.
 * Retorna { select, order, limit, offset, onConflict, columns, mods } onde `mods` e a arvore
 * de filtros/ordem/limite (raiz + um no por embed).
 */
export function parseQuery(sp) {
  const q = { select: undefined, onConflict: null, columns: null, mods: newMods() };
  for (const [key, value] of sp.entries()) {
    if (key === 'select') {
      q.select = value;
      continue;
    }
    if (key === 'on_conflict') {
      q.onConflict = value.split(',').map((s) => s.trim());
      continue;
    }
    if (key === 'columns') {
      q.columns = splitTop(value).map((s) => s.replace(/^"|"$/g, ''));
      continue;
    }
    if (key === 'order') {
      q.mods.order = parseOrder(value);
      continue;
    }
    if (key === 'limit') {
      q.mods.limit = Number(value);
      continue;
    }
    if (key === 'offset') {
      q.mods.offset = Number(value);
      continue;
    }
    if (key === 'returning' || key === 'apikey') continue;
    // and / or (raiz ou por embed)
    let m = key.match(/^(?:(.+)\.)?(not\.)?(and|or)$/);
    if (m && value.trim().startsWith('(')) {
      const path = m[1] ? m[1].split('.') : [];
      const node = parseLogic(m[3], !!m[2], value, []);
      childMods(q.mods, path).nodes.push(node);
      continue;
    }
    // modificadores de embed
    m = key.match(/^(.+)\.(order|limit|offset)$/);
    if (m) {
      const mods = childMods(q.mods, m[1].split('.'));
      if (m[2] === 'order') mods.order = parseOrder(value);
      else mods[m[2]] = Number(value);
      continue;
    }
    // filtro de coluna (possivelmente de embed)
    const ov = parseOpValue(value);
    if (!ov) continue;
    const ref = parseColumnRef(key);
    const node = { t: 'cond', path: [], col: ref.col, json: ref.json, ...ov };
    childMods(q.mods, ref.path).nodes.push(node);
  }
  return q;
}

// ---------------------------------------------------------------------------------------------
// Avaliacao
// ---------------------------------------------------------------------------------------------

const ISO_DT = /^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?)?([zZ]|[+-]\d{2}(:?\d{2})?)?$/;

function asTime(s) {
  if (typeof s !== 'string' || !ISO_DT.test(s)) return null;
  const t = Date.parse(s.length === 10 ? s + 'T00:00:00Z' : s.replace(' ', 'T'));
  return Number.isNaN(t) ? null : t;
}

function jsonStep(v, step) {
  if (v === null || v === undefined) return null;
  const key = /^\d+$/.test(step.key) && Array.isArray(v) ? Number(step.key) : step.key;
  const out = v[key];
  return out === undefined ? null : out;
}

export function getValue(row, col, json = []) {
  let v = row[col];
  if (v === undefined) v = null;
  for (let i = 0; i < json.length; i++) {
    v = jsonStep(v, json[i]);
    if (i === json.length - 1 && json[i].op === '->>' && v !== null) v = typeof v === 'object' ? JSON.stringify(v) : String(v);
  }
  return v;
}

/** Converte o literal da query para o tipo do valor da linha (numero, booleano, data...). */
function coerce(literal, actual) {
  if (typeof actual === 'number') {
    const n = Number(literal);
    return Number.isNaN(n) ? literal : n;
  }
  if (typeof actual === 'boolean') return literal === 'true' || literal === 't' || literal === '1';
  return literal;
}

function cmp(a, b) {
  // retorna -1/0/1 ou null se incomparavel
  if (typeof a === 'number' && typeof b === 'number') return a < b ? -1 : a > b ? 1 : 0;
  if (typeof a === 'string' && typeof b === 'string') {
    const ta = asTime(a);
    const tb = asTime(b);
    if (ta !== null && tb !== null) return ta < tb ? -1 : ta > tb ? 1 : 0;
    return a < b ? -1 : a > b ? 1 : 0;
  }
  if (typeof a === 'boolean' && typeof b === 'boolean') return a === b ? 0 : a ? 1 : -1;
  return String(a) < String(b) ? -1 : String(a) > String(b) ? 1 : 0;
}

export function likeToRegex(pattern, ci) {
  let re = '';
  for (let i = 0; i < pattern.length; i++) {
    const c = pattern[i];
    if (c === '\\' && i + 1 < pattern.length) {
      re += pattern[++i].replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    } else if (c === '*' || c === '%') re += '.*';
    else if (c === '_') re += '.';
    else re += c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  return new RegExp('^' + re + '$', ci ? 'is' : 's');
}

/** `(a,b,"c d")` -> ['a','b','c d'] */
export function parseListValue(v) {
  const inner = v.trim().replace(/^[({](.*)[)}]$/s, '$1');
  if (inner === '') return [];
  return splitTop(inner).map((s) => {
    const t = s.trim();
    if (t.length >= 2 && t[0] === '"' && t[t.length - 1] === '"') return t.slice(1, -1).replace(/\\(["\\])/g, '$1');
    return t;
  });
}

function sameScalar(a, b) {
  if (a === null || a === undefined) return false;
  if (typeof a === 'number') return a === Number(b);
  if (typeof a === 'boolean') return a === (b === 'true' || b === 't');
  return String(a) === String(b);
}

function isSubset(sub, sup) {
  if (sub === null || typeof sub !== 'object') return sub === sup;
  if (Array.isArray(sub)) {
    if (!Array.isArray(sup)) return false;
    return sub.every((s) => sup.some((p) => isSubset(s, p)));
  }
  if (sup === null || typeof sup !== 'object' || Array.isArray(sup)) return false;
  return Object.entries(sub).every(([k, v]) => isSubset(v, sup[k]));
}

function tokenize(s) {
  return String(s)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .split(/[^a-z0-9]+/)
    .filter(Boolean);
}

/** Aplica o operador. Retorna true/false/null (null = desconhecido, como o NULL do SQL). */
function testOp(node, actual) {
  const { op, value, quant } = node;
  if (op === 'is') {
    const v = value.toLowerCase();
    if (v === 'null') return actual === null || actual === undefined;
    if (v === 'true') return actual === true;
    if (v === 'false') return actual === false;
    if (v === 'unknown') return actual === null || actual === undefined;
    return false;
  }
  if (op === 'isdistinct') {
    if (actual === null || actual === undefined) return value !== 'null';
    return !sameScalar(actual, value);
  }
  if (actual === null || actual === undefined) return null;

  switch (op) {
    case 'eq':
      if (typeof actual === 'object') return JSON.stringify(actual) === value;
      if (typeof actual === 'string') {
        const ta = asTime(actual);
        const tb = asTime(value);
        if (ta !== null && tb !== null && (actual.length > 10 || value.length > 10)) return ta === tb;
      }
      return sameScalar(actual, value);
    case 'neq': {
      if (typeof actual === 'object') return JSON.stringify(actual) !== value;
      if (typeof actual === 'string') {
        const ta = asTime(actual);
        const tb = asTime(value);
        if (ta !== null && tb !== null && (actual.length > 10 || value.length > 10)) return ta !== tb;
      }
      return !sameScalar(actual, value);
    }
    case 'gt':
      return cmp(actual, coerce(value, actual)) > 0;
    case 'gte':
      return cmp(actual, coerce(value, actual)) >= 0;
    case 'lt':
      return cmp(actual, coerce(value, actual)) < 0;
    case 'lte':
      return cmp(actual, coerce(value, actual)) <= 0;
    case 'like':
    case 'ilike': {
      const ci = op === 'ilike';
      const text = typeof actual === 'string' ? actual : String(actual);
      if (quant) {
        const pats = parseListValue(value);
        const tests = pats.map((p) => likeToRegex(p, ci).test(text));
        return quant === 'any' ? tests.some(Boolean) : tests.every(Boolean);
      }
      return likeToRegex(value, ci).test(text);
    }
    case 'match':
    case 'imatch':
      try {
        return new RegExp(value, op === 'imatch' ? 'i' : '').test(String(actual));
      } catch {
        return false;
      }
    case 'in':
      return parseListValue(value).some((v) => sameScalar(actual, v));
    case 'cs': {
      if (Array.isArray(actual)) {
        const want = parseListValue(value);
        return want.every((w) => actual.some((a) => sameScalar(a, w)));
      }
      if (typeof actual === 'object') {
        try {
          return isSubset(JSON.parse(value), actual);
        } catch {
          return false;
        }
      }
      return false;
    }
    case 'cd': {
      if (Array.isArray(actual)) {
        const have = parseListValue(value);
        return actual.every((a) => have.some((h) => sameScalar(a, h)));
      }
      if (typeof actual === 'object') {
        try {
          return isSubset(actual, JSON.parse(value));
        } catch {
          return false;
        }
      }
      return false;
    }
    case 'ov': {
      if (!Array.isArray(actual)) return false;
      const other = parseListValue(value);
      return actual.some((a) => other.some((o) => sameScalar(a, o)));
    }
    case 'fts':
    case 'plfts':
    case 'phfts':
    case 'wfts': {
      const hay = tokenize(actual);
      const needles = tokenize(value);
      return needles.length > 0 && needles.every((n) => hay.some((h) => h.startsWith(n)));
    }
    default:
      return false; // sl sr nxl nxr adj: intervalos nao suportados
  }
}

/**
 * Avalia uma lista de nos (AND) contra a linha.
 * env.related(table, row, nomeDoEmbed) -> linhas relacionadas (para filtros com caminho dentro de or/and).
 */
export function evalNodes(nodes, row, env) {
  for (const n of nodes) if (evalNode(n, row, env) !== true) return false;
  return true;
}

function evalNode(node, row, env) {
  let r;
  if (node.t === 'cond') {
    if (node.path.length) {
      const rel = env?.related ? env.related(env.table, row, node.path[0]) : [];
      const sub = { ...node, path: node.path.slice(1) };
      r = rel.some((x) => evalNode(sub, x, { ...env, table: null }) === true);
    } else {
      r = testOp(node, getValue(row, node.col, node.json));
    }
  } else if (node.t === 'and') {
    let unknown = false;
    r = true;
    for (const it of node.items) {
      const v = evalNode(it, row, env);
      if (v === false) {
        r = false;
        break;
      }
      if (v === null) unknown = true;
    }
    if (r === true && unknown) r = null;
  } else {
    // or
    let unknown = false;
    r = false;
    for (const it of node.items) {
      const v = evalNode(it, row, env);
      if (v === true) {
        r = true;
        break;
      }
      if (v === null) unknown = true;
    }
    if (r === false && unknown) r = null;
  }
  if (node.not) return r === null ? null : !r;
  return r;
}

// ---------------------------------------------------------------------------------------------
// Ordenacao
// ---------------------------------------------------------------------------------------------

const collator = new Intl.Collator('pt-BR', { ignorePunctuation: true });

export function compareValues(a, b) {
  if (typeof a === 'number' && typeof b === 'number') return a - b;
  if (typeof a === 'boolean' && typeof b === 'boolean') return Number(a) - Number(b);
  if (typeof a === 'string' && typeof b === 'string') {
    const ta = asTime(a);
    const tb = asTime(b);
    if (ta !== null && tb !== null && a.length >= 10 && b.length >= 10) return ta - tb;
    return collator.compare(a, b);
  }
  return collator.compare(String(a), String(b));
}

/** Ordena `rows` in-place-copy conforme `order` ([{col,json,desc,nulls}]). */
export function sortRows(rows, order) {
  if (!order || !order.length) return rows;
  const arr = rows.slice();
  arr.sort((ra, rb) => {
    for (const o of order) {
      const a = getValue(ra, o.col, o.json);
      const b = getValue(rb, o.col, o.json);
      const an = a === null || a === undefined;
      const bn = b === null || b === undefined;
      if (an || bn) {
        if (an && bn) continue;
        // Postgres: ASC => NULLS LAST; DESC => NULLS FIRST (padrao)
        const nullsFirst = o.nulls ? o.nulls === 'first' : o.desc;
        return an ? (nullsFirst ? -1 : 1) : nullsFirst ? 1 : -1;
      }
      const c = compareValues(a, b);
      if (c !== 0) return o.desc ? -c : c;
    }
    return 0;
  });
  return arr;
}
