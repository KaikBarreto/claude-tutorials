// Monta o MP4 a partir dos quadros capturados: 30 fps constantes, H.264 CRF 16, yuv420p, bt709 faixa TV.
// Os quadros chegam em instantes irregulares; cada um e "segurado" ate o proximo (amostragem na grade de 1/30 s)
// e a lista vai para o demuxer concat com as duracoes exatas.
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

function run(cmd, args, { cwd } = {}) {
  return new Promise((resolve, reject) => {
    const p = spawn(cmd, args, { cwd, stdio: ['ignore', 'pipe', 'pipe'] });
    let err = '';
    p.stderr.on('data', (d) => (err += d));
    p.stdout.on('data', () => {});
    p.on('error', reject);
    p.on('close', (code) => (code === 0 ? resolve(err) : reject(new Error(`${cmd} saiu com codigo ${code}\n${err.slice(-1500)}`))));
  });
}

/**
 * Escolhe, para cada tique de 1/fps, o ultimo quadro com t <= tique. Devolve entradas { file, ticks } sem repeticao
 * consecutiva (duracao = ticks / fps).
 */
export function planTicks(frames, endS, fps = 30) {
  if (!frames.length) throw new Error('nenhum quadro capturado');
  const total = Math.max(1, Math.round(endS * fps));
  const entries = [];
  let j = 0;
  for (let k = 0; k < total; k++) {
    const tk = k / fps + 1e-6;
    while (j + 1 < frames.length && frames[j + 1].t <= tk) j++;
    const file = frames[j].file;
    const last = entries[entries.length - 1];
    if (last && last.file === file) last.ticks++;
    else entries.push({ file, ticks: 1 });
  }
  return { entries, total };
}

export async function assemble({ frames, endS, outFile, fps = 30, crf = 16, preset = 'veryfast', threads = 2 }) {
  const { entries, total } = planTicks(frames, endS, fps);
  const dir = path.dirname(outFile);
  fs.mkdirSync(dir, { recursive: true });
  const list = path.join(dir, `.${path.basename(outFile, '.mp4')}.concat.txt`);
  const lines = ['ffconcat version 1.0'];
  for (const e of entries) {
    lines.push(`file '${e.file.replace(/'/g, "'\\''")}'`);
    lines.push(`duration ${(e.ticks / fps).toFixed(6)}`);
  }
  // quirk do concat: a duracao do ultimo item so vale se o arquivo for repetido no fim
  lines.push(`file '${entries[entries.length - 1].file.replace(/'/g, "'\\''")}'`);
  fs.writeFileSync(list, lines.join('\n') + '\n');

  const vf = [
    // JPEG do Chrome = faixa total, matriz bt601 (JFIF). Converte explicitamente para bt709 faixa TV.
    'scale=in_range=pc:in_color_matrix=bt601:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int+bicubic',
    'format=yuv420p',
    // o fps vem POR ULTIMO: a conversao de cor roda so nos quadros unicos e as repeticoes (tela parada) saem de graca
    `fps=${fps}`,
  ].join(',');
  const t0 = Date.now();
  await run('ffmpeg', [
    '-y', '-hide_banner', '-loglevel', 'error',
    '-f', 'concat', '-safe', '0', '-i', list,
    '-vf', vf,
    '-c:v', 'libx264', '-preset', preset, '-crf', String(crf), '-threads', String(threads),
    '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-r', String(fps), '-fps_mode', 'cfr',
    '-movflags', '+faststart',
    '-an',
    outFile,
  ]);
  fs.rmSync(list, { force: true });
  return { encodeS: (Date.now() - t0) / 1000, ticks: total, uniqueFrames: entries.length, durationS: total / fps };
}

/** Folha de contato: 12 quadros do MP4 final, igualmente espacados, em grade 4x3 (sem cursor, claro). */
export async function contactSheet(video, outFile, { count = 12, cols = 4, tileW = 640, fps = 30, totalTicks } = {}) {
  const total = totalTicks ?? (await probeFrames(video));
  const rows = Math.ceil(count / cols);
  const idx = Array.from({ length: count }, (_, i) => Math.round((i * (total - 1)) / Math.max(1, count - 1)));
  const sel = [...new Set(idx)].map((n) => `eq(n\\,${n})`).join('+');
  const font = ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/opentype/inter/Inter-Medium.otf'].find((f) => fs.existsSync(f));
  const label = font
    ? `,drawtext=fontfile=${font}:text='%{pts\\:hms}':x=10:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=5`
    : '';
  const vf = `select='${sel}',scale=${tileW}:-1:flags=lanczos${label},tile=${cols}x${rows}:padding=8:margin=8:color=0xe9e9ec`;
  await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-i', video, '-vf', vf, '-fps_mode', 'passthrough', '-frames:v', '1', '-q:v', '3', outFile]);
  return { frames: idx.map((n) => +(n / fps).toFixed(3)) };
}

export async function probeFrames(video) {
  const out = await new Promise((resolve, reject) => {
    const p = spawn('ffprobe', ['-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', video]);
    let s = '';
    p.stdout.on('data', (d) => (s += d));
    p.on('close', () => resolve(s.trim()));
    p.on('error', reject);
  });
  return Number(out) || 1;
}

export async function probeVideo(video) {
  const out = await new Promise((resolve, reject) => {
    const p = spawn('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate,avg_frame_rate,codec_name,pix_fmt,color_space,color_range,color_primaries,color_transfer,nb_frames,duration', '-of', 'json', video]);
    let s = '';
    p.stdout.on('data', (d) => (s += d));
    p.on('close', () => resolve(s));
    p.on('error', reject);
  });
  return JSON.parse(out).streams?.[0] || {};
}
