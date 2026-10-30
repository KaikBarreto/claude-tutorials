// Helpers HTTP compartilhados: corpo, JSON, CORS, JWT, registro de handlers por pasta.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { config } from '../core/config.mjs';

export function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

export async function readJson(req) {
  const buf = await readBody(req);
  if (!buf.length) return undefined;
  try {
    return JSON.parse(buf.toString('utf8'));
  } catch {
    return undefined;
  }
}

export function cors(req, res) {
  const origin = req.headers.origin || '*';
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', req.headers['access-control-request-headers'] || '*');
  res.setHeader('Access-Control-Expose-Headers', 'Content-Range,Content-Location,Content-Type,X-Total-Count,Location');
  res.setHeader('Access-Control-Max-Age', '86400');
}

export function send(res, status, body, headers = {}) {
  const isBuf = Buffer.isBuffer(body);
  const payload = body === undefined || body === null ? null : isBuf ? body : typeof body === 'string' ? body : JSON.stringify(body);
  const h = { ...headers };
  if (payload !== null && !h['Content-Type'] && !h['content-type']) h['Content-Type'] = 'application/json; charset=utf-8';
  for (const [k, v] of Object.entries(h)) res.setHeader(k, v);
  res.statusCode = status;
  res.end(payload === null ? undefined : payload);
}

export const sendJson = (res, status, body, headers) => send(res, status, body === undefined ? null : JSON.stringify(body), headers);

// ---- JWT HS256 (assinado de verdade, mas ninguem valida a assinatura: e so para o app decodificar) ----
const b64url = (b) => Buffer.from(b).toString('base64url');

export function signJwt(payload, secret = config.jwtSecret) {
  const head = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = b64url(JSON.stringify(payload));
  const sig = crypto.createHmac('sha256', secret).update(`${head}.${body}`).digest('base64url');
  return `${head}.${body}.${sig}`;
}

export function decodeJwt(token) {
  try {
    const part = token.split('.')[1];
    return JSON.parse(Buffer.from(part, 'base64url').toString('utf8'));
  } catch {
    return null;
  }
}

/** Usuario da requisicao (do Bearer), ou null para anonimo. */
export function userFromRequest(req) {
  const auth = req.headers.authorization || '';
  const m = auth.match(/^Bearer\s+(.+)$/i);
  if (!m) return null;
  const p = decodeJwt(m[1]);
  if (!p || p.role !== 'authenticated' || !p.sub) return null;
  return { id: p.sub, email: p.email || null, claims: p };
}

/**
 * Carrega handlers de uma pasta. Cada arquivo .mjs pode:
 *   - exportar default uma funcao  -> registrada com o nome do arquivo
 *   - exportar `handlers` = { nome: fn, ... } -> varios de uma vez
 */
export async function loadHandlerDir(dir) {
  const map = new Map();
  if (!fs.existsSync(dir)) return map;
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.mjs')).sort()) {
    const mod = await import(pathToFileURL(path.join(dir, f)).href);
    if (mod.handlers) for (const [k, fn] of Object.entries(mod.handlers)) map.set(k, fn);
    if (typeof mod.default === 'function') map.set(f.replace(/\.mjs$/, ''), mod.default);
  }
  return map;
}
