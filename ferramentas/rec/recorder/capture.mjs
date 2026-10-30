// Captura de tela pelo CDP (Page.startScreencast): guarda cada quadro JPEG com o instante real em que o Chrome o gerou.
// A pagina parada nao gera quadros — o montador (assemble.mjs) segura o ultimo ate o proximo.
import fs from 'node:fs';
import path from 'node:path';

/**
 * @param {import('playwright').Page} page
 * @param {string} dir        pasta dos quadros (criada/limpa)
 * @param {object} opts       { quality=92, width=2560, height=1600 }
 * @returns {Promise<{ stop(): Promise<CaptureResult>, firstFrame: Promise<number>, stats(): object }>}
 */
export async function startCapture(page, dir, { quality = 92, width = 2560, height = 1600 } = {}) {
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });

  const cdp = await page.context().newCDPSession(page);
  const frames = []; // { file, t (s, relogio do Chrome), recvMs (Date.now() ao receber), bytes }
  let writes = Promise.resolve();
  let pending = 0;
  let maxPending = 0;
  let n = 0;
  let resolveFirst;
  const firstFrame = new Promise((r) => (resolveFirst = r));
  let stopped = false;

  cdp.on('Page.screencastFrame', (ev) => {
    // reconhece JA: pedir o proximo quadro o quanto antes e o que decide a taxa de captura
    cdp.send('Page.screencastFrameAck', { sessionId: ev.sessionId }).catch(() => {});
    if (stopped) return;
    const idx = ++n;
    const file = path.join(dir, String(idx).padStart(6, '0') + '.jpg');
    const buf = Buffer.from(ev.data, 'base64');
    const t = ev.metadata.timestamp;
    frames.push({ file, t, recvMs: Date.now(), bytes: buf.length });
    pending++;
    maxPending = Math.max(maxPending, pending);
    writes = writes.then(() => fs.promises.writeFile(file, buf)).then(() => void pending--);
    if (idx === 1) resolveFirst(t * 1000);
  });

  await cdp.send('Page.startScreencast', { format: 'jpeg', quality, maxWidth: width, maxHeight: height, everyNthFrame: 1 });
  const startedAt = Date.now();

  return {
    firstFrame,
    stats: () => ({ frames: frames.length, elapsedMs: Date.now() - startedAt, maxPending }),
    /** Para a captura e devolve os quadros com tempo relativo ao primeiro (s). `endMs` = instante final (epoch ms). */
    async stop(endMs = Date.now()) {
      stopped = true;
      await cdp.send('Page.stopScreencast').catch(() => {});
      await writes;
      await cdp.detach().catch(() => {});
      const t0 = frames.length ? frames[0].t : 0;
      return {
        dir,
        t0Ms: t0 * 1000,
        frames: frames.map((f) => ({ file: f.file, t: f.t - t0, recvMs: f.recvMs, bytes: f.bytes })),
        endS: Math.max(0, endMs / 1000 - t0),
        maxPending,
      };
    },
  };
}
