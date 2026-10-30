// Isola o navegador da internet: tudo que NAO for 127.0.0.1/localhost e desviado.
//   1) tenta o handler externo do Supabase falso (rec/fakebase/handlers/ext/<host>.mjs) via /__ext/<host>/<caminho>;
//   2) sem handler, devolve um corpo vazio do tipo certo (css/js/png...) para nao gerar erro no console;
//   3) registra tudo em .runtime/externos.log (e o fakebase anota os sem handler em desconhecidos.log).
import fs from 'node:fs';
import path from 'node:path';
import { FAKE_URL, RUNTIME_DIR } from './env.mjs';

const LOCAL_HOSTS = new Set(['127.0.0.1', 'localhost', '[::1]', '::1']);
const PNG_1PX = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==', 'base64');
const LOG = path.join(RUNTIME_DIR, 'externos.log');
const seen = new Set();

// Hosts que o app chama mas que nao importam para o video (metricas, fontes): stub vazio, sem registrar como lacuna.
const SILENT_HOSTS = /(^|\.)(googletagmanager|google-analytics|googleadservices|doubleclick|googlesyndication|facebook|clarity|hotjar|sentry|segment|mixpanel|fonts\.googleapis|fonts\.gstatic)\.(com|net|ms|io)$|^connect\.facebook\.net$/;

export const isLocalUrl = (url) => {
  try {
    return LOCAL_HOSTS.has(new URL(url).hostname);
  } catch {
    return true;
  }
};

function stubFor(resourceType, url) {
  switch (resourceType) {
    case 'stylesheet':
      return { status: 200, contentType: 'text/css', body: '/* externo bloqueado */' };
    case 'script':
      return { status: 200, contentType: 'application/javascript', body: '/* externo bloqueado */' };
    case 'image':
      return { status: 200, contentType: 'image/png', body: PNG_1PX };
    case 'document':
    case 'iframe':
      return { status: 200, contentType: 'text/html', body: '<!doctype html><html><body style="margin:0;background:#f4f4f5"></body></html>' };
    case 'xhr':
    case 'fetch':
      return { status: 200, contentType: 'application/json', body: '{}' };
    default:
      return { status: 204, contentType: 'text/plain', body: '' };
  }
}

/** Instala o desvio no contexto do Playwright. Retorna a lista (viva) de externos vistos. */
export async function isolateNetwork(context, { verbose = false } = {}) {
  const hits = [];
  await context.route((url) => !isLocalUrl(url.toString()), async (route) => {
    const req = route.request();
    const u = new URL(req.url());
    const key = `${req.method()} ${u.hostname}${u.pathname}`;
    if (!seen.has(key)) {
      seen.add(key);
      try {
        fs.appendFileSync(LOG, `${new Date().toISOString()}\t${req.resourceType()}\t${key}\n`);
      } catch {}
    }
    hits.push({ method: req.method(), url: req.url(), type: req.resourceType() });
    if (verbose) console.log(`[externo] ${req.method()} ${req.url()}`);

    if (SILENT_HOSTS.test(u.hostname)) {
      const s = stubFor(req.resourceType(), req.url());
      return route.fulfill({ status: s.status, headers: { 'content-type': s.contentType, 'access-control-allow-origin': '*' }, body: s.body });
    }
    // 1) handler do fakebase
    try {
      const body = req.postDataBuffer();
      const res = await fetch(`${FAKE_URL}/__ext/${u.hostname}${u.pathname}${u.search}`, {
        method: req.method(),
        headers: body ? { 'content-type': req.headers()['content-type'] || 'application/json' } : undefined,
        body: body && req.method() !== 'GET' && req.method() !== 'HEAD' ? body : undefined,
      });
      if (res.ok) {
        const buf = Buffer.from(await res.arrayBuffer());
        return route.fulfill({
          status: res.status,
          headers: { 'content-type': res.headers.get('content-type') || 'application/json', 'access-control-allow-origin': '*', 'cache-control': 'no-store' },
          body: buf,
        });
      }
    } catch {
      /* fakebase fora do ar: cai no stub */
    }
    // 2) stub vazio
    const s = stubFor(req.resourceType(), req.url());
    return route.fulfill({ status: s.status, headers: { 'content-type': s.contentType, 'access-control-allow-origin': '*' }, body: s.body });
  });
  return hits;
}
