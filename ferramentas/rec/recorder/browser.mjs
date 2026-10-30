// Navegador pronto para gravar: Chromium headless, viewport 1280x800 CSS a 2x (frames 2560x1600), sessao da Camila
// ja aberta, internet desviada (net.mjs), sem service worker e sem os pop-ups de versao/tarefas do dia.
// (Modo url, o app de qualquer pessoa: openSession({ anonymous: true, isolate: false }) — sem sessao falsa, sem desvio
// de rede e sem as chaves da Dominex; idioma e fuso vem do roteiro.)
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from './pw.mjs';
import { APP_URL, FAKE_URL, ANON_KEY, USER_EMAIL, REC_DIR } from './env.mjs';
import { isolateNetwork } from './net.mjs';
import { Telemetry } from './telemetry.mjs';

export const VIEWPORT = { width: 1280, height: 800 };
export const SCALE = 2;
/** Aparelhos para "device" no roteiro (o VIEWPORT acima muda no início da sessão: um processo grava um capítulo). */
export const DEVICES = {
  phone: {
    width: 390, height: 844, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
    geolocation: { latitude: -22.9035, longitude: -43.1038, accuracy: 15 }, // Niterói (mundo fictício)
  },
};
export const TZ = 'America/Sao_Paulo';
/** "Agora" do mundo falso (FAKE_NOW, o mesmo do backend falso): congela a data do navegador na gravação. */
export const FAKE_NOW_DATE = (() => {
  const v = process.env.FAKE_NOW;
  const d = v ? new Date(v) : null;
  return d && !Number.isNaN(d.getTime()) ? d : null;
})();

/** Chave que o supabase-js usa no localStorage: sb-<primeiro rotulo do host>-auth-token. */
export function authStorageKey(supabaseUrl = FAKE_URL) {
  return `sb-${new URL(supabaseUrl).hostname.split('.')[0]}-auth-token`;
}

/** Entra no Supabase falso (senha qualquer) e devolve a sessao no formato do supabase-js. */
export async function fakeLogin(email = USER_EMAIL) {
  const res = await fetch(`${FAKE_URL}/auth/v1/token?grant_type=password`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', apikey: ANON_KEY },
    body: JSON.stringify({ email, password: 'domiflix' }),
  });
  if (!res.ok) throw new Error(`login falso falhou (${res.status}): ${await res.text()} — o fakebase esta no ar em ${FAKE_URL}?`);
  return res.json();
}

function appVersion() {
  try {
    const src = fs.readFileSync(path.resolve(REC_DIR, '../app/src/config/version.ts'), 'utf8');
    return src.match(/APP_VERSION\s*=\s*["']([^"']+)["']/)?.[1] || '0.0.0';
  } catch {
    return '0.0.0';
  }
}

/** Hoje (AAAA-MM-DD) no fuso da empresa — mesma conta do app para o pop-up de tarefas do dia. */
export function todayBR(date = new Date()) {
  return new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' }).format(date);
}

/** localStorage inicial: sessao + "ja vi" dos avisos que atrapalhariam a gravacao. */
export function buildStorageState(session, extra = {}) {
  const v = appVersion();
  const entries = {
    [authStorageKey()]: JSON.stringify(session),
    app_version: v,
    notification_shown_version: v,
    [`dominex:daily-tasks-shown:${session.user.id}`]: todayBR(FAKE_NOW_DATE || new Date()),
    'pwa-install-dismissed': 'true',
    theme: 'light',
    ...extra,
  };
  return {
    cookies: [],
    origins: [{ origin: new URL(APP_URL).origin, localStorage: Object.entries(entries).map(([name, value]) => ({ name, value })) }],
  };
}

/** Modo url: so o localStorage que o roteiro pediu (`storage`), sem sessao nem chave nenhuma da Dominex. */
export function plainStorageState(entries = {}) {
  const list = Object.entries(entries).map(([name, value]) => ({ name, value: String(value) }));
  if (!list.length) return undefined;
  return { cookies: [], origins: [{ origin: new URL(APP_URL).origin, localStorage: list }] };
}

// Ruido conhecido do app em modo dev (nao e problema do kit nem do backend falso): nao conta como erro.
const NOISE_CONSOLE = [
  /React Router Future Flag Warning/,
  /validateDOMNesting/, // aviso do React so em dev (p dentro de div etc.); producao nao emite
  /Download the React DevTools/,
  /\[vite\] (connecting|connected)/,
  /GL Driver Message/, // aviso de desempenho do WebGL por software
  /Missing `Description` or `aria-describedby/, // aviso de acessibilidade do Radix (janelas sem descricao), do proprio app
];
const NOISE_FAILED = /ERR_ABORTED/; // requisicao cancelada pelo proprio app (troca de tela / AbortController)

// O app registra um service worker (PWA). Aqui ele fica bloqueado (senao ele passa por cima do desvio de rede),
// entao entregamos um registro "de mentira" para o codigo do app nao quebrar.
// "sameTab" no roteiro: o que abriria outra aba (link target=_blank, window.open) abre nesta, porque o vídeo grava uma
// aba só (portal público, link do contrato...). PDF continua fora: vira ilustração na edição.
function sameTabLinks() {
  try {
    const open = window.open;
    window.open = function (url, ...rest) {
      if (url) { location.assign(url); return window; }
      return open.call(this, url, ...rest);
    };
    document.addEventListener('click', (e) => {
      const a = e.target && e.target.closest ? e.target.closest('a[target]') : null;
      if (a && a.target !== '_self' && a.href) a.target = '_self';
    }, true);
  } catch (e) { /* ignora */ }
}

function stubServiceWorker() {
  try {
    const sw = navigator.serviceWorker;
    if (!sw) return;
    const reg = {
      scope: location.origin + '/', installing: null, waiting: null, active: null,
      addEventListener() {}, removeEventListener() {}, update: () => Promise.resolve(), unregister: () => Promise.resolve(true),
    };
    sw.register = () => Promise.resolve(reg);
    sw.getRegistration = () => Promise.resolve(undefined);
    sw.getRegistrations = () => Promise.resolve([]);
  } catch (e) { /* ignora */ }
}

export async function launchBrowser({ headed = false, args = [] } = {}) {
  return chromium.launch({
    headless: !headed,
    args: [
      // sem esta flag o screencast do Chrome entrega quadros de 1280x800 (CSS px) mesmo com deviceScaleFactor 2;
      // com ela os quadros saem em pixels fisicos: 2560x1600
      `--force-device-scale-factor=${SCALE}`,
      '--force-color-profile=srgb',
      '--font-render-hinting=none',
      '--enable-unsafe-swiftshader', // WebGL por software (mapa) no headless
      '--disable-features=Translate,MediaRouter,OptimizationHints',
      '--disable-background-networking',
      '--autoplay-policy=no-user-gesture-required',
      '--no-first-run',
      ...args,
    ],
  });
}

/**
 * Abre contexto + pagina. Opcoes:
 *   email         usuario do fakebase (padrao Camila)
 *   storage       localStorage extra { chave: valor } (anonimo: so estas chaves, nenhuma da Dominex)
 *   anonymous     true = sem sessao (para gravar a tela de login; e o modo url)
 *   isolate       true (padrao, fakebase) desvia tudo que nao e localhost (net.mjs); false (modo url) deixa a rede passar
 *   locale        idioma do navegador (padrao pt-BR)      timezone   fuso do navegador (padrao America/Sao_Paulo)
 * Devolve { browser, context, page, session, diag } — diag acumula erros de console, falhas e respostas >= 400.
 */
export async function openSession({
  browser, headed = false, email = USER_EMAIL, storage = {}, anonymous = false, verboseNet = false,
  sameTab = false, // links e window.open que abririam outra aba abrem nesta (o vídeo grava uma aba só)
  device = null, // "phone": tela de celular (390x844 @2x, toque, localização); padrão: computador 1280x800
  telemetry = true, // observa mouse/teclado reais da pagina (nao desenha nada)
  cursorOverlay = false, // SO depuracao: desenha um cursor sintetico na pagina (o video final NAO leva cursor)
  isolate = true,
  locale = 'pt-BR',
  timezone = TZ,
} = {}) {
  const own = !browser;
  browser = browser || (await launchBrowser({ headed }));
  const session = anonymous ? null : await fakeLogin(email);
  const dev = device ? DEVICES[device] : null;
  if (device && !dev) throw new Error(`device desconhecido: ${device} (validos: ${Object.keys(DEVICES).join(', ')})`);
  if (dev) Object.assign(VIEWPORT, { width: dev.width, height: dev.height });
  const context = await browser.newContext({
    viewport: VIEWPORT,
    screen: VIEWPORT,
    ...(dev ? { isMobile: dev.isMobile, hasTouch: dev.hasTouch, userAgent: dev.userAgent, geolocation: dev.geolocation } : {}),
    deviceScaleFactor: SCALE,
    locale,
    timezoneId: timezone,
    colorScheme: 'light',
    serviceWorkers: 'block',
    acceptDownloads: false,
    // "Copiar link" (formulario de captacao, QR do equipamento) usa navigator.clipboard.writeText: sem esta permissao o
    // headless recusa e o app mostra o aviso de contingencia ("Link gerado" + URL) em vez de "Link gerado e copiado!"
    permissions: ['clipboard-read', 'clipboard-write', ...(dev ? ['geolocation'] : [])],
    storageState: session ? buildStorageState(session, storage) : plainStorageState(storage),
  });
  // Relógio do navegador no "agora" do mundo falso: datas do mundo fictício (visitas do PMOC, vencimentos) não
  // envelhecem entre o planejamento e a gravação. O tempo continua correndo normalmente a partir dali.
  if (FAKE_NOW_DATE) await context.clock.install({ time: FAKE_NOW_DATE });
  await context.addInitScript(stubServiceWorker);
  if (sameTab) await context.addInitScript(sameTabLinks);
  const tel = new Telemetry({ dsf: SCALE });
  if (telemetry || cursorOverlay) await tel.install(context, { overlay: cursorOverlay });
  const externos = isolate ? await isolateNetwork(context, { verbose: verboseNet }) : [];
  const page = await context.newPage();

  const diag = { console: [], pageErrors: [], failed: [], bad: [], externos, inflight: new Set(), lastNet: Date.now() };
  page.on('request', (r) => {
    diag.inflight.add(r);
    diag.lastNet = Date.now();
  });
  const done = (r) => {
    diag.inflight.delete(r);
    diag.lastNet = Date.now();
  };
  page.on('requestfinished', done);
  page.on('requestfailed', done);
  // Navegacao de documento (recarregar a pagina): o navegador nao avisa o fim das requisicoes que o documento antigo
  // deixou pendentes, e elas ficariam "em voo" para sempre (o `settle` nunca assentaria). Descartamos ao confirmar o novo.
  let docNav = false;
  page.on('request', (r) => {
    try {
      if (r.isNavigationRequest() && r.frame() === page.mainFrame()) docNav = true;
    } catch (e) {}
  });
  page.on('framenavigated', (f) => {
    if (docNav && f === page.mainFrame()) {
      docNav = false;
      diag.inflight.clear();
    }
  });
  diag.ignored = 0;
  diag.staleDropped = 0;
  page.on('console', (m) => {
    if (m.type() !== 'error' && m.type() !== 'warning') return;
    const text = m.text().slice(0, 600);
    if (NOISE_CONSOLE.some((re) => re.test(text))) {
      diag.ignored++;
      return;
    }
    diag.console.push({ type: m.type(), text, url: m.location()?.url || '' });
  });
  page.on('pageerror', (e) => diag.pageErrors.push(String(e?.stack || e).slice(0, 800)));
  page.on('requestfailed', (r) => {
    const why = r.failure()?.errorText || '';
    if (NOISE_FAILED.test(why)) {
      diag.ignored++;
      return;
    }
    diag.failed.push(`${r.method()} ${r.url().slice(0, 200)} :: ${why}`);
  });
  page.on('response', (r) => {
    if (r.status() >= 400) diag.bad.push(`${r.status()} ${r.request().method()} ${r.url().slice(0, 220)}`);
  });
  return { browser, context, page, session, diag, tel, ownsBrowser: own };
}

/**
 * Espera a tela "assentar": nada em voo e nenhuma requisicao nova por quietMs (ou estoura timeoutMs sem erro).
 * Rede de seguranca: requisicao "em voo" sem NENHUM evento de rede ha staleMs foi perdida pelo navegador (o app nao tem
 * long-poll; websocket nao conta) — e descartada e contada em diag.staleDropped, em vez de travar ate o timeout.
 */
export async function settle(s, { quietMs = 600, timeoutMs = 20000, staleMs = 8000 } = {}) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    const quiet = Date.now() - s.diag.lastNet;
    if (s.diag.inflight.size === 0 && quiet >= quietMs) return true;
    if (s.diag.inflight.size > 0 && quiet >= Math.max(staleMs, quietMs)) {
      s.diag.staleDropped += s.diag.inflight.size;
      s.diag.inflight.clear();
      return true;
    }
    await new Promise((r) => setTimeout(r, 100));
  }
  return false;
}

export async function closeSession(s) {
  try {
    await s.context.close();
  } finally {
    if (s.ownsBrowser) await s.browser.close();
  }
}
