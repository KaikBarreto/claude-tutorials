#!/usr/bin/env node
// Diagnostico: o carimbo de tempo dos quadros esta alinhado com o relogio dos eventos (telemetria)?
// A pagina troca a cor de um quadrado (a cor codifica o numero do flip) em instantes aleatorios, anotando o relogio
// real de cada troca (rAF). Depois achamos o 1o quadro que mostra cada cor e medimos: carimbo do quadro - instante da
// troca. Resultado esperado numa pagina leve: positivo e pequeno (40 a 70 ms = latencia normal de pintura do Chrome);
// negativo ou de centenas de ms = relogios desalinhados ou maquina sobrecarregada.
//   node rec/recorder/clock-check.mjs [segundos=10] [--load]     (--load mexe o mouse sem parar para gerar carga)
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { openSession, closeSession } from './browser.mjs';
import { startCapture } from './capture.mjs';
import { RUNTIME_DIR } from './env.mjs';

const seconds = Number(process.argv.find((a) => /^\d+(\.\d+)?$/.test(a)) || 10);
const load = process.argv.includes('--load');
const outDir = path.join(RUNTIME_DIR, 'clock-check');

const s = await openSession({ anonymous: true, telemetry: false });
const { page } = s;
await page.setContent('<html><body style="margin:0"><div id="c" style="position:fixed;left:0;top:0;width:200px;height:200px;background:#101010"></div></body></html>');
await page.evaluate(() => {
  const levels = [16, 48, 80, 112, 144, 176, 208, 240]; // 3 canais x 8 niveis = 512 codigos (robusto ao JPEG)
  const el = document.getElementById('c');
  window.__flips = [];
  let idx = 0;
  const flip = () => {
    requestAnimationFrame(() => {
      idx++;
      el.style.background = `rgb(${levels[(idx >> 6) & 7]},${levels[(idx >> 3) & 7]},${levels[idx & 7]})`;
      window.__flips.push([idx % 512, performance.timeOrigin + performance.now()]);
    });
    setTimeout(flip, 90 + Math.random() * 230);
  };
  flip();
});

const cap = await startCapture(page, path.join(outDir, 'frames'), { quality: 92 });
await cap.firstFrame;
const t0 = Date.now();
if (load) {
  for (let a = 0; Date.now() - t0 < seconds * 1000; a += 0.18) {
    await page.mouse.move(640 + Math.cos(a) * 500, 400 + Math.sin(a * 1.3) * 300);
    await new Promise((r) => setTimeout(r, 6));
  }
} else {
  await new Promise((r) => setTimeout(r, seconds * 1000));
}
const res = await cap.stop(Date.now());
const flips = await page.evaluate(() => window.__flips);
await closeSession(s);

// cor do canto de cada quadro -> codigo do flip
const lv = [16, 48, 80, 112, 144, 176, 208, 240];
const q = (v) => lv.reduce((b, x, i) => (Math.abs(x - v) < Math.abs(lv[b] - v) ? i : b), 0);
const flipAt = new Map(flips);
const lags = [];
const delivery = [];
let prev = -1;
for (const f of res.frames) {
  const px = execFileSync('ffmpeg', ['-v', 'error', '-i', f.file, '-vf', 'crop=16:16:60:60,scale=1:1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], { maxBuffer: 1 << 20 });
  const code = (q(px[0]) << 6) | (q(px[1]) << 3) | q(px[2]);
  const stamp = res.t0Ms + f.t * 1000;
  delivery.push(f.recvMs - stamp);
  if (code !== prev && flipAt.has(code)) lags.push(stamp - flipAt.get(code));
  prev = code;
}
fs.rmSync(path.join(outDir, 'frames'), { recursive: true, force: true });
const pct = (a, p) => [...a].sort((x, y) => x - y)[Math.min(a.length - 1, Math.floor(a.length * p))];
const r = (v) => Math.round(v * 10) / 10;
console.log(
  JSON.stringify(
    {
      seconds, load, frames: res.frames.length, flips: flips.length, medidos: lags.length,
      'carimbo - troca (ms)': { min: r(Math.min(...lags)), mediana: r(pct(lags, 0.5)), p90: r(pct(lags, 0.9)), max: r(Math.max(...lags)) },
      'chegada - carimbo (ms)': { mediana: r(pct(delivery, 0.5)), p90: r(pct(delivery, 0.9)), max: r(Math.max(...delivery)) },
    },
    null,
    1
  )
);
