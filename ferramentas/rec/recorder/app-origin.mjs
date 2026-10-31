// APP_ORIGIN: o navegador abre o app num endereço "de produto" (ex.: https://www.dominex.app) e este módulo serve tudo a
// partir do app local (LOCAL_APP_URL, a porta 8080), do mesmo jeito que o gravador desvia o Supabase falso:
// `context.route` responde cada requisição daquela origem com o que o servidor local devolve. A requisição NÃO vai para a
// rede (por isso não há certificado nem servidor https) e o endereço nunca aparece no vídeo (só gravamos a página).
// Desligado por padrão: sem APP_ORIGIN nada aqui roda e o navegador sai idêntico ao de antes.
import { APP_ORIGIN, LOCAL_APP_URL } from './env.mjs';

/** Caminho com extensão de arquivo (chunk, imagem, fonte...): 404 desses é 404 de verdade; o resto é rota da SPA. */
const looksLikeFile = (p) => /\.[a-z0-9]{1,8}$/i.test(p) && !/\.html?$/i.test(p);

/**
 * Argumentos extras do Chromium quando APP_ORIGIN está ligada (a lista de entrada volta igual quando está desligada).
 *  - `--disable-features`: o gravador já passa uma; o Chromium usa só a última ocorrência, então juntamos numa só e
 *    acrescentamos as checagens de rede privada (página "pública" falando com 127.0.0.1 do Supabase falso).
 *  - `--host-resolver-rules`: tudo que não for 127.0.0.1/localhost não resolve (preconnect, prefetch e qualquer coisa que
 *    escape do `context.route` falha alto em vez de sair para a internet).
 *  - `--no-proxy-server`: sem proxy do ambiente no caminho.
 */
export function withAppOriginArgs(args) {
  if (!APP_ORIGIN) return args;
  const FEATURES = ['PrivateNetworkAccessSendPreflights', 'PrivateNetworkAccessRespectPreflightResults', 'BlockInsecurePrivateNetworkRequests', 'LocalNetworkAccessChecks', 'LocalNetworkAccessChecksWebSockets'];
  const out = [];
  let merged = false;
  for (const a of args) {
    const m = /^--disable-features=(.*)$/.exec(a);
    if (m) {
      out.push(`--disable-features=${[...new Set([...m[1].split(',').filter(Boolean), ...FEATURES])].join(',')}`);
      merged = true;
    } else out.push(a);
  }
  if (!merged) out.push(`--disable-features=${FEATURES.join(',')}`);
  out.push('--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1 , EXCLUDE localhost', '--no-proxy-server');
  return out;
}

/**
 * Serve o app local na origem APP_ORIGIN. Chamar DEPOIS de `isolateNetwork` (a última rota registrada vale primeiro).
 * Devolve contadores vivos { served, spaFallback, failed, paths } (null se APP_ORIGIN estiver desligada).
 */
export async function serveAppAtOrigin(context, { verbose = false } = {}) {
  if (!APP_ORIGIN) return null;
  const local = String(LOCAL_APP_URL).replace(/\/$/, '');
  const stats = { served: 0, spaFallback: 0, failed: 0, paths: new Set() };
  await context.route((url) => url.origin === APP_ORIGIN, async (route) => {
    const req = route.request();
    const u = new URL(req.url());
    stats.paths.add(u.pathname);
    try {
      let resp = await route.fetch({ url: local + u.pathname + u.search });
      // fallback de SPA: o servidor local já devolve o index.html nas rotas do app; garantimos o mesmo se vier 404 num documento
      if (resp.status() === 404 && req.isNavigationRequest() && !looksLikeFile(u.pathname)) {
        resp = await route.fetch({ url: local + '/index.html' });
        stats.spaFallback++;
      }
      stats.served++;
      if (verbose) console.log(`[app-origin] ${req.method()} ${u.pathname} -> ${resp.status()}`);
      await route.fulfill({ response: resp });
    } catch (e) {
      stats.failed++;
      if (verbose) console.log(`[app-origin] falhou ${req.method()} ${u.pathname}: ${e?.message || e}`);
      await route.abort().catch(() => {});
    }
  });
  return stats;
}
