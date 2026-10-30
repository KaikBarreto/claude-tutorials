// /__ext/<host>/<caminho> — APIs externas falsas (BrasilAPI, ViaCEP, OpenStreetMap...). O gravador desvia as
// chamadas do navegador para ca (rec/recorder/net.mjs). Handlers em handlers/ext/<host>.mjs:
//   export default async (ctx) => objeto                       -> 200 JSON
//                              => { __status: 404, body: {...} } -> JSON com outro status
//                              => { __raw: true, type, body, status?, headers? } -> corpo cru (css, imagem, estilo de mapa)
// ctx: { host, path, query, method, body (JSON ou undefined), raw (Buffer), headers, store, db }.
import { store } from '../core/store.mjs';
import { db } from '../core/db.mjs';
import { unknown } from '../core/log.mjs';
import { readBody, send, sendJson } from './common.mjs';

export const extHandlers = new Map();

export async function handleExt(req, res, url, ctx) {
  const rest = url.pathname.replace(/^\/__ext\//, '');
  const slash = rest.indexOf('/');
  const host = slash < 0 ? rest : rest.slice(0, slash);
  const pathname = slash < 0 ? '/' : rest.slice(slash);
  const handler = extHandlers.get(host);
  if (!handler) {
    unknown('EXTERNO_SEM_HANDLER', `${host}${pathname}`, req.method);
    return sendJson(res, 404, { message: 'sem handler externo para ' + host });
  }
  const raw = await readBody(req);
  let body;
  try {
    body = raw.length ? JSON.parse(raw.toString('utf8')) : undefined;
  } catch {
    body = undefined;
  }
  const out = await handler({
    ...ctx,
    store,
    db,
    host,
    path: pathname,
    query: Object.fromEntries(url.searchParams),
    method: req.method,
    headers: req.headers,
    body,
    raw,
  });
  if (out && typeof out === 'object' && out.__raw) {
    return send(res, out.status || 200, out.body ?? '', { 'Content-Type': out.type || 'application/octet-stream', 'Cache-Control': 'no-store', ...(out.headers || {}) });
  }
  if (out && typeof out === 'object' && '__status' in out) return sendJson(res, out.__status, out.body);
  return sendJson(res, 200, out ?? {});
}
