// Roda DENTRO da pagina (injetado em todo documento). Nao desenha nada: so observa os eventos reais de mouse e
// teclado que o robo dispara e os entrega ao Node pelo binding window.__recTel.
// Coordenadas saem em pixels do VIDEO (CSS px x devicePixelRatio); o tempo sai em ms de relogio (epoch).
(() => {
  if (window.__recTelInstalled) return;
  window.__recTelInstalled = true;
  try {
    if (window.top !== window) return; // iframes (ex.: mapa embutido) ficam de fora; o Node completa os passos do mouse
  } catch (e) {
    return;
  }
  const send = (ev) => {
    try {
      if (typeof window.__recTel === 'function') window.__recTel(ev);
    } catch (e) {}
  };
  const ORIGIN = performance.timeOrigin;
  const k = () => window.devicePixelRatio || 1;
  const r1 = (v) => Math.round(v * 10) / 10;
  const INTERACTIVE =
    'button,a[href],[role="button"],[role="tab"],[role="menuitem"],[role="menuitemcheckbox"],[role="menuitemradio"],[role="option"],[role="checkbox"],[role="radio"],[role="switch"],[role="combobox"],[role="link"],input,textarea,select,label,summary,[tabindex]:not([tabindex="-1"])';

  let lastX = 0;
  let lastY = 0;
  // Ultima posicao do ponteiro em px CSS, FRACIONARIA (pointer events). mousedown/mouseup/click/wheel chegam com
  // coordenadas inteiras; quando batem com ela (erro de arredondamento <= 1 px) usamos a fracionaria.
  let fx = null;
  let fy = null;
  const trackPointer = (e) => {
    fx = e.clientX;
    fy = e.clientY;
  };
  const snap = (e) => (fx !== null && Math.abs(e.clientX - fx) <= 1 && Math.abs(e.clientY - fy) <= 1 ? { x: fx, y: fy } : { x: e.clientX, y: e.clientY });

  const rectOf = (el) => {
    if (!el || !el.getBoundingClientRect) return null;
    const b = el.getBoundingClientRect();
    const f = k();
    return { x: r1(b.left * f), y: r1(b.top * f), w: r1(b.width * f), h: r1(b.height * f) };
  };
  const targetOf = (el) => {
    if (!el || el.nodeType !== 1) return null;
    return el.closest ? el.closest(INTERACTIVE) || el : el;
  };
  const isRoot = (el) => !el || el === document.body || el === document.documentElement;
  const describe = (el) => {
    if (!el || el.nodeType !== 1) return null;
    const out = { tag: el.tagName.toLowerCase() };
    const role = el.getAttribute('role');
    if (role) out.role = role;
    if (el.type && (out.tag === 'input' || out.tag === 'button')) out.type = el.type;
    let text = el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.getAttribute('title') || '';
    if (!text && el.childElementCount <= 20) text = (el.innerText || '').replace(/\s+/g, ' ').trim();
    if (text) out.text = text.slice(0, 48);
    return out;
  };
  const cursorAt = (x, y) => {
    let raw = 'auto';
    try {
      const el = document.elementFromPoint(x, y);
      if (el) raw = getComputedStyle(el).cursor || 'auto';
    } catch (e) {}
    // "url(...), pointer" -> ultima palavra-chave
    const word = raw.split(',').pop().trim();
    const kind = word === 'pointer' ? 'pointer' : word === 'text' || word === 'vertical-text' ? 'text' : 'arrow';
    return { kind, raw: word };
  };
  const stamp = (e) => ORIGIN + (e.timeStamp || performance.now());

  const opts = { capture: true, passive: true };

  window.addEventListener(
    'pointermove',
    (e) => {
      if (e.pointerType && e.pointerType !== 'mouse') return;
      const list = typeof e.getCoalescedEvents === 'function' ? e.getCoalescedEvents() : [];
      const evs = list && list.length ? list : [e];
      for (const ce of evs) {
        const f = k();
        const c = cursorAt(ce.clientX, ce.clientY);
        trackPointer(ce);
        lastX = r1(ce.clientX * f);
        lastY = r1(ce.clientY * f);
        send({ type: 'move', t: stamp(ce), x: lastX, y: lastY, cursor: c.kind, cursorRaw: c.raw });
      }
    },
    opts
  );

  // Elemento sob o ponteiro no momento do clique (guardado: um menu/select do Radix fecha ou cobre a tela e o
  // `click` acaba disparado no <body>; nesse caso vale o elemento que foi pressionado).
  let press = null;
  // elementos que cobrem (quase) toda a janela (<body>, fundo de modal/select do Radix) nao dizem nada sobre o clique
  const huge = (el) => {
    const b = el.getBoundingClientRect();
    return b.width >= window.innerWidth * 0.9 && b.height >= window.innerHeight * 0.9;
  };
  const info = (el) => (isRoot(el) || huge(el) ? null : { rect: rectOf(el), target: describe(el) });
  const pointerEv = (type) => (e) => {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    trackPointer(e);
    const f = k();
    lastX = r1(e.clientX * f);
    lastY = r1(e.clientY * f);
    let i = info(targetOf(e.target));
    if (type === 'down') press = i;
    else if (!i) i = press;
    send({ type, t: stamp(e), x: lastX, y: lastY, button: e.button, rect: i?.rect, target: i?.target });
  };
  window.addEventListener('pointerdown', pointerEv('down'), opts);
  window.addEventListener('pointerup', pointerEv('up'), opts);

  const clickEv = (type) => (e) => {
    const f = k();
    // clique disparado pelo teclado (Enter/Espaço num botão) chega com clientX/Y = 0: o mouse NÃO foi lá.
    // Não mexe na última posição do ponteiro e marca kb (antes virava (0, 0) e levava câmera e cursor para o canto).
    if (e.detail === 0 && e.clientX === 0 && e.clientY === 0) {
      const ik = info(targetOf(e.target));
      send({ type, t: stamp(e), kb: true, button: e.button, rect: ik?.rect, target: ik?.target });
      return;
    }
    const p = snap(e);
    lastX = r1(p.x * f);
    lastY = r1(p.y * f);
    const i = info(targetOf(e.target)) || press;
    send({ type, t: stamp(e), x: lastX, y: lastY, button: e.button, rect: i?.rect, target: i?.target });
  };
  window.addEventListener('click', clickEv('click'), opts);
  window.addEventListener('dblclick', clickEv('dblclick'), opts);

  window.addEventListener(
    'wheel',
    (e) => {
      const f = k();
      const p = snap(e);
      lastX = r1(p.x * f);
      lastY = r1(p.y * f);
      send({ type: 'scroll', t: stamp(e), x: lastX, y: lastY, deltaY: r1(e.deltaY), deltaX: r1(e.deltaX) });
    },
    opts
  );

  // Campo de senha (input[type=password], ou autocomplete current-password/new-password): a tecla NUNCA sai no
  // telemetry.json (defesa extra; a telemetria ja descarta o que vem antes do 1o quadro). Segue o foco para dentro de
  // shadow roots abertos.
  const deepActive = () => {
    let a = document.activeElement;
    while (a && a.shadowRoot && a.shadowRoot.activeElement) a = a.shadowRoot.activeElement;
    return a;
  };
  const isSecret = (el) => {
    if (!el || el.nodeType !== 1 || el.tagName !== 'INPUT') return false;
    if (String(el.type).toLowerCase() === 'password') return true;
    return /(^|\s)(current|new)-password(\s|$)/i.test(el.getAttribute('autocomplete') || '');
  };
  // o robo (runner.mjs, passo type) pergunta antes de digitar, para mascarar as proprias amostras do mesmo jeito
  window.__recSecretFocus = () => isSecret(deepActive());

  window.addEventListener(
    'keydown',
    (e) => {
      const el = document.activeElement && document.activeElement !== document.body ? document.activeElement : null;
      if (isSecret(deepActive())) {
        // sem code, sem shift/ctrl/alt/meta: nada que ajude a reconstruir o que foi digitado
        send({ type: 'key', t: stamp(e), x: lastX, y: lastY, key: '•', rect: rectOf(el), target: describe(el) });
        return;
      }
      const s = { type: 'key', t: stamp(e), x: lastX, y: lastY, key: e.key, code: e.code, rect: rectOf(el), target: describe(el) };
      if (e.shiftKey) s.shift = true;
      if (e.ctrlKey) s.ctrl = true;
      if (e.altKey) s.alt = true;
      if (e.metaKey) s.meta = true;
      send(s);
    },
    opts
  );
})();
