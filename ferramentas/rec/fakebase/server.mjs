#!/usr/bin/env node
// Supabase falso para gravar tutoriais da Dominex.
//   node rec/fakebase/server.mjs            (porta 54321, 127.0.0.1)
// Ver rec/README.md.
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { config } from './core/config.mjs';
import { store } from './core/store.mjs';
import { startLog, LOG_PATH } from './core/log.mjs';
import { loadHooks } from './core/mutate.mjs';
import { viewProviders } from './core/query.mjs';
import { cors, send, sendJson, loadHandlerDir, userFromRequest } from './http/common.mjs';
import { handleRest, rpcHandlers } from './http/rest.mjs';
import { handleAuth } from './http/auth.mjs';
import { handleStorage } from './http/storage.mjs';
import { handleFunctions, fnHandlers } from './http/functions.mjs';
import { handleExt, extHandlers } from './http/ext.mjs';
import { handleDev } from './http/dev.mjs';
import { handleTiles } from './http/tiles.mjs';
import { attachRealtime } from './http/realtime.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));

async function loadAll() {
  store.loadSeeds();
  await loadHooks();
  const replace = (target, map) => {
    target.clear();
    for (const [k, v] of map) target.set(k, v);
  };
  replace(rpcHandlers, await loadHandlerDir(path.join(here, 'handlers/rpc')));
  replace(fnHandlers, await loadHandlerDir(path.join(here, 'handlers/functions')));
  replace(extHandlers, await loadHandlerDir(path.join(here, 'handlers/ext')));
  const views = await loadHandlerDir(path.join(here, 'handlers/views'));
  viewProviders.clear();
  for (const [k, v] of views) viewProviders.set(k, v);
}

const recent = [];
const LOG_REQ = process.env.FAKE_LOG_REQUESTS === '1';

const server = http.createServer(async (req, res) => {
  const t0 = Date.now();
  cors(req, res);
  if (req.method === 'OPTIONS') return send(res, 204, null);
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const user = userFromRequest(req);
  const ctx = { user, userId: user?.id || config.userId, companyId: config.companyId };

  res.on('finish', () => {
    const line = `${req.method} ${url.pathname}${url.search.length > 200 ? url.search.slice(0, 200) + '...' : url.search} -> ${res.statusCode} (${Date.now() - t0}ms)`;
    recent.push(line);
    if (recent.length > 300) recent.shift();
    if (LOG_REQ) console.log(line);
  });

  try {
    const p = url.pathname;
    if (p.startsWith('/rest/v1')) return await handleRest(req, res, url, ctx);
    if (p.startsWith('/auth/v1')) return await handleAuth(req, res, url, ctx);
    if (p.startsWith('/storage/v1')) return await handleStorage(req, res, url, ctx);
    if (p.startsWith('/functions/v1')) return await handleFunctions(req, res, url, ctx);
    if (p.startsWith('/__ext/')) return await handleExt(req, res, url, ctx);
    if (p.startsWith('/__tiles')) return await handleTiles(req, res, url);
    if (p === '/__dev/requests') return sendJson(res, 200, recent);
    if (p.startsWith('/__dev')) return await handleDev(req, res, url, loadAll);
    if (p.startsWith('/realtime/v1')) return sendJson(res, 200, { ok: true });
    if (p === '/' || p === '/health') return sendJson(res, 200, { fakebase: true, tables: store.tables.size });
    return sendJson(res, 404, { error: 'rota desconhecida', path: p });
  } catch (e) {
    console.error('[server] erro nao tratado', req.method, req.url, e);
    if (!res.headersSent) sendJson(res, 500, { message: String(e?.message || e) });
  }
});

attachRealtime(server);

await loadAll();
startLog();

server.listen(config.port, config.host, () => {
  const seeded = [...store.tables.values()].filter((t) => t.rows.length).length;
  console.log(`fakebase pronto em http://${config.host}:${config.port}  (${seeded} tabelas com seed, ${rpcHandlers.size} rpcs, ${fnHandlers.size} functions, ${extHandlers.size} externos)`);
  console.log(`desconhecidos -> ${LOG_PATH}`);
});

function shutdown() {
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 1500).unref();
}
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
