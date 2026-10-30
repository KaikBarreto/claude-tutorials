// SO PARA DEPURACAO (opcao cursorOverlay: true): desenha uma seta/mao/barra seguindo o mouse e um circulo no clique.
// O video final NAO leva cursor — o editor desenha a partir de telemetry.json.
(() => {
  if (window.__recCursorInstalled) return;
  window.__recCursorInstalled = true;
  try {
    if (window.top !== window) return;
  } catch (e) {
    return;
  }
  const ARROW = '<svg width="24" height="30" viewBox="0 0 24 30"><path d="M3 2 L3 22.5 L8.2 18 L11.6 26.2 L15.1 24.7 L11.7 16.9 L18.5 16.4 Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  const HAND = '<svg width="26" height="28" viewBox="0 0 26 28"><path d="M9 2.5c-1 0-1.8.8-1.8 1.8v10.2l-1.7-1.7c-.7-.6-1.8-.6-2.4.1-.6.7-.5 1.8.2 2.4l6 6.7c.9 1 2.1 1.5 3.4 1.5h4.5c2.2 0 4-1.8 4-4v-5.4c0-1-.8-1.8-1.8-1.8-.3 0-.6.1-.8.2-.2-.7-.9-1.2-1.7-1.2-.4 0-.8.1-1.1.4-.3-.6-.9-1-1.6-1-.2 0-.5.1-.7.1V4.3C10.8 3.3 10 2.5 9 2.5z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
  const IBEAM = '<svg width="20" height="28" viewBox="0 0 20 28"><path d="M6 3h8M10 3v22M6 25h8" stroke="#fff" stroke-width="4.4" stroke-linecap="round"/><path d="M6 3h8M10 3v22M6 25h8" stroke="#111" stroke-width="2" stroke-linecap="round"/></svg>';
  const HOT = { arrow: [3, 2], pointer: [9, 3], text: [10, 14] };

  const host = document.createElement('div');
  host.setAttribute('data-rec-debug-cursor', '');
  host.style.cssText = 'position:fixed;left:0;top:0;width:0;height:0;z-index:2147483647;pointer-events:none;';
  const sprite = document.createElement('div');
  sprite.style.cssText = 'position:absolute;left:0;top:0;will-change:transform;filter:drop-shadow(0 1px 1.5px rgba(0,0,0,.35));';
  host.appendChild(sprite);
  const style = document.createElement('style');
  style.textContent = '@keyframes recRipple{from{transform:translate(-50%,-50%) scale(.2);opacity:.7}to{transform:translate(-50%,-50%) scale(1.5);opacity:0}}';
  host.appendChild(style);

  let kind = 'arrow';
  let x = -100;
  let y = -100;
  const draw = () => {
    const h = HOT[kind];
    sprite.style.transform = `translate3d(${x - h[0]}px,${y - h[1]}px,0)`;
  };
  const setKind = (k) => {
    if (k === kind) return;
    kind = k;
    sprite.innerHTML = k === 'pointer' ? HAND : k === 'text' ? IBEAM : ARROW;
    draw();
  };
  sprite.innerHTML = ARROW;
  // O init script roda ANTES do <html> existir: anexar em `document` faria o overlay virar a raiz da pagina (pagina em
  // branco). So monta quando houver documentElement (e de novo a cada evento, caso o app remova o no).
  const mount = () => {
    if (host.isConnected || !document.documentElement) return;
    document.documentElement.appendChild(host);
  };
  mount();
  document.addEventListener('readystatechange', mount);
  document.addEventListener('DOMContentLoaded', mount);

  const raw = (el) => {
    let r = 'auto';
    try {
      r = getComputedStyle(el).cursor || 'auto';
    } catch (e) {}
    const w = r.split(',').pop().trim();
    return w === 'pointer' ? 'pointer' : w === 'text' || w === 'vertical-text' ? 'text' : 'arrow';
  };
  window.addEventListener(
    'pointermove',
    (e) => {
      x = e.clientX;
      y = e.clientY;
      const el = document.elementFromPoint(x, y);
      if (el) setKind(raw(el));
      draw();
      mount();
    },
    { capture: true, passive: true }
  );
  window.addEventListener(
    'mousedown',
    (e) => {
      const r = document.createElement('div');
      r.style.cssText = `position:absolute;left:${e.clientX}px;top:${e.clientY}px;width:44px;height:44px;border-radius:50%;border:3px solid rgba(34,197,139,.9);background:rgba(34,197,139,.18);animation:recRipple 520ms ease-out forwards;`;
      host.appendChild(r);
      setTimeout(() => r.remove(), 600);
      sprite.style.opacity = '.85';
    },
    { capture: true, passive: true }
  );
  window.addEventListener('mouseup', () => (sprite.style.opacity = '1'), { capture: true, passive: true });
})();
