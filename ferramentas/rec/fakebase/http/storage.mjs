// /storage/v1 — Storage falso. Arquivos: (1) enviados em memoria, (2) pasta rec/fakebase/storage/<bucket>/<caminho>,
// (3) se for imagem e nao existir, um placeholder SVG deterministico (para nao aparecer imagem quebrada no video).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { unknown } from '../core/log.mjs';
import { uuid, nowIso } from '../core/util.mjs';
import { readBody, readJson, send, sendJson } from './common.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
export const STORAGE_DIR = process.env.FAKE_STORAGE_DIR || path.resolve(here, '../storage');

const uploaded = new Map(); // "bucket/caminho" -> { buf, type, updated_at, id }
const KNOWN_BUCKETS = [
  'company-logos', 'equipment-files', 'customer-photos', 'team-photos', 'employee-photos', 'domiflix-thumbnails',
  'blog-images', 'os-media', 'avatars', 'pdv-order-attachments', 'customer-documents', 'attachments',
];

const MIME = {
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.svg': 'image/svg+xml', '.pdf': 'application/pdf', '.mp4': 'video/mp4', '.webm': 'video/webm', '.txt': 'text/plain',
  '.json': 'application/json', '.ico': 'image/x-icon', '.mp3': 'audio/mpeg', '.csv': 'text/csv',
};
const IMAGE_EXT = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico']);

function safeJoin(base, rel) {
  const full = path.resolve(base, rel);
  return full.startsWith(path.resolve(base)) ? full : null;
}

function placeholderSvg(key) {
  const h = crypto.createHash('sha1').update(key).digest();
  const hue = (h[0] * 360) / 256;
  const hue2 = (hue + 35) % 360;
  const label = path.basename(key).replace(/\.[^.]+$/, '').slice(0, 2).toUpperCase();
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="hsl(${hue.toFixed(0)},45%,82%)"/><stop offset="1" stop-color="hsl(${hue2.toFixed(0)},50%,70%)"/></linearGradient></defs>
<rect width="400" height="400" fill="url(#g)"/>
<g fill="none" stroke="rgba(255,255,255,.55)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"><rect x="120" y="140" width="160" height="110" rx="18"/><path d="M150 270h100"/><path d="M165 185h70M165 210h40"/></g>
</svg>`;
}

function locate(bucket, objPath) {
  const key = `${bucket}/${objPath}`;
  const up = uploaded.get(key);
  if (up) return { buf: up.buf, type: up.type, key };
  const file = safeJoin(STORAGE_DIR, key);
  if (file && fs.existsSync(file) && fs.statSync(file).isFile()) {
    return { buf: fs.readFileSync(file), type: MIME[path.extname(file).toLowerCase()] || 'application/octet-stream', key };
  }
  return null;
}

function serve(res, bucket, objPath, method) {
  const found = locate(bucket, objPath);
  if (found) {
    return send(res, 200, method === 'HEAD' ? null : found.buf, {
      'Content-Type': found.type,
      'Cache-Control': 'max-age=3600',
      'Content-Length': found.buf.length,
    });
  }
  const ext = path.extname(objPath).toLowerCase();
  unknown('STORAGE_ARQUIVO_AUSENTE', `${bucket}/${objPath}`, IMAGE_EXT.has(ext) ? 'servido placeholder' : '404');
  if (IMAGE_EXT.has(ext)) {
    return send(res, 200, method === 'HEAD' ? null : placeholderSvg(`${bucket}/${objPath}`), {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'max-age=60',
    });
  }
  return sendJson(res, 404, { statusCode: '404', error: 'not_found', message: 'Object not found' });
}

/** Extrai o arquivo de um corpo multipart/form-data (storage-js envia { cacheControl, '': file }). */
function parseMultipart(buf, contentType) {
  const m = String(contentType).match(/boundary=(?:"([^"]+)"|([^;]+))/i);
  if (!m) return null;
  const boundary = Buffer.from('--' + (m[1] || m[2]));
  let pos = buf.indexOf(boundary);
  while (pos !== -1) {
    const next = buf.indexOf(boundary, pos + boundary.length);
    if (next === -1) break;
    const part = buf.subarray(pos + boundary.length + 2, next - 2); // tira \r\n inicial e final
    const sep = part.indexOf('\r\n\r\n');
    if (sep > -1) {
      const headers = part.subarray(0, sep).toString('utf8');
      const body = part.subarray(sep + 4);
      if (/filename=/i.test(headers) || /name=""/i.test(headers)) {
        const ct = headers.match(/content-type:\s*([^\r\n]+)/i);
        return { buf: body, type: ct ? ct[1].trim() : 'application/octet-stream' };
      }
    }
    pos = next;
  }
  return null;
}

function listEntries(bucket, prefix) {
  const names = new Map(); // nome imediato -> { isFolder, ... }
  const pre = prefix ? prefix.replace(/\/+$/, '') + '/' : '';
  const consider = (full, meta) => {
    if (!full.startsWith(pre)) return;
    const rest = full.slice(pre.length);
    const first = rest.split('/')[0];
    if (!first) return;
    if (rest.includes('/')) names.set(first, { name: first, id: null, updated_at: null, created_at: null, last_accessed_at: null, metadata: null });
    else names.set(first, { name: first, id: meta.id, updated_at: meta.updated_at, created_at: meta.updated_at, last_accessed_at: meta.updated_at, metadata: { size: meta.size, mimetype: meta.type, cacheControl: 'max-age=3600' } });
  };
  for (const [key, v] of uploaded) if (key.startsWith(bucket + '/')) consider(key.slice(bucket.length + 1), { id: v.id, updated_at: v.updated_at, size: v.buf.length, type: v.type });
  const base = safeJoin(STORAGE_DIR, bucket);
  if (base && fs.existsSync(base)) {
    const walk = (dir, rel) => {
      for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
        const r = rel ? rel + '/' + f.name : f.name;
        if (f.isDirectory()) walk(path.join(dir, f.name), r);
        else {
          const st = fs.statSync(path.join(dir, f.name));
          consider(r, { id: crypto.createHash('md5').update(bucket + r).digest('hex'), updated_at: st.mtime.toISOString(), size: st.size, type: MIME[path.extname(f.name).toLowerCase()] || 'application/octet-stream' });
        }
      }
    };
    walk(base, '');
  }
  return [...names.values()];
}

export async function handleStorage(req, res, url) {
  const route = url.pathname.replace(/^\/storage\/v1\/?/, '');
  const method = req.method;
  const parts = route.split('/').map(decodeURIComponent);

  // ---- buckets ----
  if (parts[0] === 'bucket') {
    const mk = (id) => ({ id, name: id, public: true, file_size_limit: null, allowed_mime_types: null, created_at: nowIso(), updated_at: nowIso(), owner: null });
    if (parts.length === 1) return sendJson(res, 200, KNOWN_BUCKETS.map(mk));
    return sendJson(res, 200, mk(parts[1]));
  }

  if (parts[0] !== 'object' && parts[0] !== 'render') {
    unknown('STORAGE_SEM_HANDLER', `${method} /storage/v1/${route}`);
    return sendJson(res, 200, {});
  }

  // ---- leitura publica / autenticada / assinada / imagem transformada ----
  if (method === 'GET' || method === 'HEAD') {
    let i = 1;
    if (parts[0] === 'render') i = 3; // render/image/public/<bucket>/...
    const mode = parts[i];
    if (['public', 'authenticated', 'sign', 'info'].includes(mode)) i++;
    const bucket = parts[i];
    const objPath = parts.slice(i + 1).join('/');
    return serve(res, bucket, objPath, method);
  }

  // ---- URLs assinadas ----
  if (method === 'POST' && parts[1] === 'sign') {
    const body = (await readJson(req)) || {};
    const bucket = parts[2];
    const sign = (p) => `/object/sign/${bucket}/${p}?token=${crypto.randomBytes(12).toString('hex')}`;
    if (parts.length > 3) {
      const p = parts.slice(3).join('/');
      return sendJson(res, 200, { signedURL: sign(p) });
    }
    return sendJson(res, 200, (body.paths || []).map((p) => ({ error: null, path: p, signedURL: sign(p) })));
  }
  if (method === 'POST' && parts[1] === 'upload' && parts[2] === 'sign') {
    return sendJson(res, 200, { url: `/object/upload/sign/${parts.slice(3).join('/')}?token=x`, token: 'x' });
  }

  // ---- listar ----
  if (method === 'POST' && parts[1] === 'list') {
    const body = (await readJson(req)) || {};
    const bucket = parts[2];
    let entries = listEntries(bucket, body.prefix || '');
    if (body.search) entries = entries.filter((e) => e.name.toLowerCase().includes(String(body.search).toLowerCase()));
    const off = body.offset || 0;
    return sendJson(res, 200, entries.slice(off, body.limit ? off + body.limit : undefined));
  }

  // ---- mover / copiar ----
  if (method === 'POST' && (parts[1] === 'move' || parts[1] === 'copy')) {
    const b = (await readJson(req)) || {};
    const src = `${b.bucketId}/${b.sourceKey}`;
    const dst = `${b.destinationBucket || b.bucketId}/${b.destinationKey}`;
    const found = locate(b.bucketId, b.sourceKey);
    if (found) {
      uploaded.set(dst, { buf: found.buf, type: found.type, updated_at: nowIso(), id: uuid() });
      if (parts[1] === 'move') uploaded.delete(src);
    }
    return sendJson(res, 200, { message: parts[1] === 'move' ? 'Successfully moved' : 'Successfully copied', Key: dst });
  }

  // ---- remover ----
  if (method === 'DELETE') {
    const bucket = parts[1];
    if (parts.length > 2) {
      uploaded.delete(`${bucket}/${parts.slice(2).join('/')}`);
      return sendJson(res, 200, { message: 'Successfully deleted' });
    }
    const body = (await readJson(req)) || {};
    const removed = [];
    for (const p of body.prefixes || []) {
      if (uploaded.delete(`${bucket}/${p}`)) removed.push({ name: p, bucket_id: bucket, id: uuid() });
    }
    return sendJson(res, 200, removed);
  }

  // ---- upload (POST novo, PUT substitui) ----
  if (method === 'POST' || method === 'PUT') {
    const bucket = parts[1];
    const objPath = parts.slice(2).join('/');
    const raw = await readBody(req);
    const ctype = req.headers['content-type'] || '';
    let file;
    if (/multipart\/form-data/i.test(ctype)) file = parseMultipart(raw, ctype);
    else file = { buf: raw, type: ctype || MIME[path.extname(objPath).toLowerCase()] || 'application/octet-stream' };
    if (!file) file = { buf: raw, type: 'application/octet-stream' };
    const id = uuid();
    uploaded.set(`${bucket}/${objPath}`, { buf: file.buf, type: file.type, updated_at: nowIso(), id });
    return sendJson(res, 200, { Id: id, Key: `${bucket}/${objPath}` });
  }

  unknown('STORAGE_SEM_HANDLER', `${method} /storage/v1/${route}`);
  return sendJson(res, 200, {});
}
