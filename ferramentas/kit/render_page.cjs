// Renderiza uma página com window.renderFrame(n) quadro a quadro (Chromium headless via Playwright).
// uso: node render_page.cjs <url> <saída> [--frames N | --dur S] [--fps 30] [--w 1920 --h 1080] [--alpha] [--stills 0,30,60]
//   saída .mp4  -> H.264 (sem alfa)          saída .mkv -> FFV1 RGBA (com --alpha, para sobreposições)
//   saída pasta -> PNGs (com --stills, só os quadros pedidos)
const {spawn} = require('child_process');
const fs = require('fs');
const path = require('path');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright');

const args = process.argv.slice(2);
const url = args[0], out = args[1];
const opt = (k, d) => { const i = args.indexOf('--' + k); return i < 0 ? d : args[i + 1]; };
const has = k => args.includes('--' + k);
const FPS = +opt('fps', 30), W = +opt('w', 1920), H = +opt('h', 1080), ALPHA = has('alpha');

(async () => {
  const browser = await chromium.launch({args: ['--disable-gpu', '--force-color-profile=srgb', '--hide-scrollbars']});
  const page = await browser.newPage({viewport: {width: W, height: H}, deviceScaleFactor: 1});
  page.on('console', m => { if (m.type() === 'error') console.error('[page]', m.text()); });
  page.on('pageerror', e => console.error('[pageerror]', e.message));
  await page.goto(url, {waitUntil: 'networkidle'});
  await page.waitForFunction('window.READY === true', null, {timeout: 60000});
  const dur = await page.evaluate('window.DURATION || 0');
  const N = +opt('frames', 0) || Math.round(+opt('dur', dur) * FPS);
  if (has('meta')) fs.writeFileSync(opt('meta'), JSON.stringify(await page.evaluate('({duration: window.DURATION, cues: window.CUES || [], fps: ' + FPS + '})'), null, 1));
  const shot = async n => {
    await page.evaluate(n => window.renderFrame(n), n);
    return ALPHA || has('stills') ? page.screenshot({type: 'png', omitBackground: ALPHA, clip: {x: 0, y: 0, width: W, height: H}})
                                  : page.screenshot({type: 'jpeg', quality: 97, clip: {x: 0, y: 0, width: W, height: H}});
  };
  if (has('stills')) {
    fs.mkdirSync(out, {recursive: true});
    for (const n of opt('stills').split(',').map(Number)) fs.writeFileSync(path.join(out, `f${String(n).padStart(5, '0')}.png`), await shot(n));
    await browser.close(); console.log('stills ok'); return;
  }
  const enc = out.endsWith('.mkv')
    ? ['-c:v', 'ffv1', '-pix_fmt', ALPHA ? 'bgra' : 'bgr0']
    : ['-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', '-movflags', '+faststart'];
  const grainArg = opt('grain', '0') !== '0' ? ['-vf', `noise=alls=${opt('grain')}:allf=u`] : [];
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', ALPHA ? 'png' : 'mjpeg', '-i', '-', ...grainArg, ...enc, out],
                   {stdio: ['pipe', 'inherit', 'inherit']});
  const t0 = Date.now();
  for (let n = 0; n < N; n++) {
    const buf = await shot(n);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (n % 30 === 0) process.stdout.write(`\r${n}/${N} ${((Date.now() - t0) / 1000 / (n + 1)).toFixed(2)} s/q`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(`\nok ${out} (${N} quadros, ${((Date.now() - t0) / 1000).toFixed(1)} s)`);
})().catch(e => { console.error(e); process.exit(1); });
