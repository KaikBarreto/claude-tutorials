// /__dev/* — utilidades do kit de gravacao (nao fazem parte do Supabase).
import { store } from '../core/store.mjs';
import { unknownSummary, unknown, clearUnknown, LOG_PATH } from '../core/log.mjs';
import { readJson, sendJson } from './common.mjs';

export async function handleDev(req, res, url, reloadAll) {
  const route = url.pathname.replace(/^\/__dev\/?/, '');
  if (route === 'health') return sendJson(res, 200, { ok: true });
  if (route === 'unknowns') return sendJson(res, 200, { log: LOG_PATH, items: unknownSummary() });
  if (route === 'unknowns/clear' && req.method === 'POST') {
    clearUnknown();
    return sendJson(res, 200, { ok: true });
  }
  if (route === 'reset' && req.method === 'POST') {
    await reloadAll();
    return sendJson(res, 200, { ok: true, tables: store.tables.size });
  }
  if (route === 'seed' && req.method === 'POST') {
    // aplica seeds extras (rec/fakebase/seeds-extra/<nome>.json) por cima do estado atual: { files: ["t3/apos-cap02"] }
    const b = (await readJson(req)) || {};
    const files = [].concat(b.files ?? b.file ?? []).filter(Boolean);
    try {
      const applied = store.applyExtra(files);
      return sendJson(res, 200, { ok: true, applied });
    } catch (e) {
      return sendJson(res, 400, { ok: false, error: String(e?.message || e) });
    }
  }
  if (route === 'log-unknown' && req.method === 'POST') {
    const b = (await readJson(req)) || {};
    unknown(b.kind || 'EXTERNO_SEM_HANDLER', b.name || '?', b.detail || '');
    return sendJson(res, 200, { ok: true });
  }
  if (route === 'state') {
    const table = url.searchParams.get('table');
    if (table) return sendJson(res, 200, store.rows(table));
    const counts = {};
    for (const [n, t] of store.tables) counts[n] = t.rows.length;
    return sendJson(res, 200, counts);
  }
  return sendJson(res, 404, { error: 'rota /__dev desconhecida' });
}
