// /rest/v1 — imita o PostgREST: select/embeds/filtros, insert/upsert/update/delete, rpc.
import { URL } from 'node:url';
import { store } from '../core/store.mjs';
import { db } from '../core/db.mjs';
import * as S from '../core/schema.mjs';
import { parseQuery, newMods } from '../core/filters.mjs';
import { runSelect, projectRows, runOnArray, viewProviders } from '../core/query.mjs';
import { insertRows, updateRows, deleteRows, HttpError } from '../core/mutate.mjs';
import { unknown } from '../core/log.mjs';
import { pgError, clone } from '../core/util.mjs';
import { readBody, send, sendJson } from './common.mjs';

export const rpcHandlers = new Map();

/** Erro de negocio levantado por um handler de RPC (vira 400 com code P0001, como RAISE EXCEPTION). */
export class RpcError extends Error {
  constructor(message, code = 'P0001', status = 400, details = null) {
    super(message);
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

function parsePrefer(req) {
  const out = {};
  const raw = req.headers.prefer;
  if (!raw) return out;
  for (const part of String(raw).split(',')) {
    const [k, v] = part.trim().split('=');
    if (k) out[k.trim()] = v === undefined ? true : v.trim();
  }
  return out;
}

function wantsObject(req) {
  return String(req.headers.accept || '').includes('application/vnd.pgrst.object+json');
}

function parseRange(req) {
  const r = req.headers.range;
  if (!r) return {};
  const m = String(r).match(/^(\d+)-(\d*)$/);
  if (!m) return {};
  return { rangeFrom: Number(m[1]), rangeTo: m[2] === '' ? undefined : Number(m[2]) };
}

function contentRange(offset, count, total) {
  const t = total === undefined || total === null ? '*' : total;
  if (!count) return `*/${t}`;
  return `${offset}-${offset + count - 1}/${t}`;
}

function singleOrError(rows, extra = {}) {
  if (rows.length !== 1) {
    throw new HttpError(406, pgError('PGRST116', 'JSON object requested, multiple (or no) rows returned', `The result contains ${rows.length} rows`));
  }
  return rows[0];
}

const OBJ_CT = 'application/vnd.pgrst.object+json; charset=utf-8';

export async function handleRest(req, res, url, ctx) {
  const rest = decodeURIComponent(url.pathname.replace(/^\/rest\/v1\/?/, ''));
  if (!rest) return sendJson(res, 200, { swagger: '2.0', info: { title: 'fakebase' }, paths: {} });

  try {
    if (rest.startsWith('rpc/')) return await handleRpc(req, res, url, ctx, rest.slice(4));
    return await handleTable(req, res, url, ctx, rest.split('/')[0]);
  } catch (e) {
    if (e instanceof HttpError) return sendJson(res, e.status, e.body);
    if (e instanceof RpcError) return sendJson(res, e.status, pgError(e.code, e.message, e.details));
    console.error('[rest] erro interno', req.method, url.pathname, e);
    return sendJson(res, 500, pgError('XX000', String(e?.message || e)));
  }
}

async function handleTable(req, res, url, ctx, table) {
  const method = req.method;
  const prefer = parsePrefer(req);
  const q = parseQuery(url.searchParams);
  const known = S.isKnown(table) || store.peek(table) || viewProviders.has(table);

  if (method === 'GET' || method === 'HEAD') {
    if (!known) {
      unknown('TABELA_DESCONHECIDA', table, `${method} ?${url.searchParams.toString().slice(0, 160)}`);
      if (wantsObject(req)) return sendJson(res, 406, pgError('PGRST116', 'JSON object requested, multiple (or no) rows returned', 'The result contains 0 rows'));
      return sendJson(res, 200, method === 'HEAD' ? undefined : [], { 'Content-Range': '*/0' });
    }
    const t = store.peek(table);
    if (!t || (!t.rows.length && !t.seeded && !viewProviders.has(table))) {
      unknown('TABELA_SEM_SEED', table, `GET ?${url.searchParams.toString().slice(0, 160)}`);
    }
    const { rows, total, offset } = runSelect(table, q, parseRange(req));
    const headers = { 'Content-Range': contentRange(offset, rows.length, prefer.count ? total : undefined) };
    if (method === 'HEAD') return send(res, 200, null, headers);
    if (wantsObject(req)) {
      const one = singleOrError(rows);
      return send(res, 200, JSON.stringify(one), { ...headers, 'Content-Type': OBJ_CT });
    }
    return sendJson(res, 200, rows, headers);
  }

  // ---- escritas ----
  if (!known) {
    unknown('TABELA_DESCONHECIDA', table, `${method} (tabela dinamica criada em memoria)`);
    store.table(table);
  }
  const raw = await readBody(req);
  let body;
  if (raw.length) {
    try {
      body = JSON.parse(raw.toString('utf8'));
    } catch {
      throw new HttpError(400, pgError('PGRST102', 'Empty or invalid json'));
    }
  }
  const returnRep = prefer.return === 'representation';
  const returnHeaders = prefer.return === 'headers-only';

  let affected;
  let status;
  if (method === 'POST') {
    if (body === undefined) throw new HttpError(400, pgError('PGRST102', 'Empty or invalid json'));
    const upsert = prefer.resolution === 'merge-duplicates' ? 'merge' : prefer.resolution === 'ignore-duplicates' ? 'ignore' : null;
    affected = insertRows(table, body, q, ctx, upsert);
    status = 201;
  } else if (method === 'PATCH') {
    if (body === undefined) throw new HttpError(400, pgError('PGRST102', 'Empty or invalid json'));
    affected = updateRows(table, body, q, ctx);
    status = returnRep ? 200 : 204;
  } else if (method === 'DELETE') {
    affected = deleteRows(table, q, ctx);
    status = returnRep ? 200 : 204;
  } else {
    return sendJson(res, 405, pgError('PGRST117', 'Unsupported HTTP method: ' + method));
  }

  const headers = {};
  if (prefer.count) headers['Content-Range'] = `*/${affected.length}`;
  if (returnRep) {
    const rows = projectRows(table, affected, q.select, q.mods);
    if (wantsObject(req)) {
      const one = singleOrError(rows);
      return send(res, status, JSON.stringify(one), { ...headers, 'Content-Type': OBJ_CT });
    }
    return sendJson(res, status, rows, headers);
  }
  if (returnHeaders && affected[0]?.id) headers['Location'] = `/${table}?id=eq.${affected[0].id}`;
  return send(res, status === 200 ? 204 : status, null, headers);
}

async function handleRpc(req, res, url, ctx, name) {
  const prefer = parsePrefer(req);
  let args = {};
  if (req.method === 'GET' || req.method === 'HEAD') {
    const known = new Set(S.rpcInfo(name)?.args || []);
    for (const [k, v] of url.searchParams.entries()) if (known.has(k)) args[k] = v;
  } else {
    const raw = await readBody(req);
    if (raw.length) {
      try {
        args = JSON.parse(raw.toString('utf8'));
      } catch {
        throw new HttpError(400, pgError('PGRST102', 'Empty or invalid json'));
      }
    }
  }
  const info = S.rpcInfo(name);
  const handler = rpcHandlers.get(name);
  let result;
  if (handler) {
    result = await handler(args ?? {}, { ...ctx, store, db, url, req });
  } else {
    unknown('RPC_SEM_HANDLER', name, `args=${JSON.stringify(args).slice(0, 160)}${info ? '' : ' (fora do schema)'}`);
    result = S.emptyRpcResult(name);
  }

  if (result === undefined && info?.returns === 'void') return send(res, 204, null);
  if (result === undefined) result = null;

  if (Array.isArray(result)) {
    const q = parseQuery(url.searchParams);
    const { rows, total } = runOnArray(result, q);
    const headers = { 'Content-Range': contentRange(0, rows.length, prefer.count ? total : undefined) };
    if (req.method === 'HEAD') return send(res, 200, null, headers);
    if (wantsObject(req)) {
      const one = singleOrError(rows);
      return send(res, 200, JSON.stringify(one), { ...headers, 'Content-Type': OBJ_CT });
    }
    return sendJson(res, 200, rows, headers);
  }
  if (req.method === 'HEAD') return send(res, 200, null);
  return sendJson(res, 200, result === undefined ? null : clone(result));
}
