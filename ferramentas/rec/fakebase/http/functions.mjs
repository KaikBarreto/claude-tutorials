// /functions/v1/<nome> — Edge Functions falsas. Handlers em handlers/functions/<nome>.mjs.
import { store } from '../core/store.mjs';
import { db } from '../core/db.mjs';
import { unknown } from '../core/log.mjs';
import { readBody, sendJson } from './common.mjs';

export const fnHandlers = new Map();

/** Erro de negocio de uma edge function: vira { error: mensagem } com o status dado. */
export class FunctionError extends Error {
  constructor(message, status = 400, extra = {}) {
    super(message);
    this.status = status;
    this.extra = extra;
  }
}

export async function handleFunctions(req, res, url, ctx) {
  const name = url.pathname.replace(/^\/functions\/v1\/?/, '').split('/')[0];
  const raw = await readBody(req);
  let body = {};
  const ctype = String(req.headers['content-type'] || '');
  if (raw.length && /json/i.test(ctype)) {
    try {
      body = JSON.parse(raw.toString('utf8'));
    } catch {
      body = {};
    }
  } else if (raw.length) {
    body = { __raw: raw };
  }
  const handler = fnHandlers.get(name);
  if (!handler) {
    unknown('FUNCTION_SEM_HANDLER', name, `${req.method} body=${JSON.stringify(body).slice(0, 160)}`);
    return sendJson(res, 200, {});
  }
  try {
    const out = await handler(body, { ...ctx, store, db, req, url });
    return sendJson(res, 200, out === undefined ? {} : out);
  } catch (e) {
    if (e instanceof FunctionError) return sendJson(res, e.status, { error: e.message, ...e.extra });
    console.error('[functions] erro em', name, e);
    return sendJson(res, 500, { error: String(e?.message || e) });
  }
}
