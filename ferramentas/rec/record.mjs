#!/usr/bin/env node
// Grava um roteiro de acoes no Dominex (com Supabase falso) e gera MP4 + logs.
//   node rec/record.mjs rec/poc/poc.json [--out rec/poc] [--name poc] [opcoes]
// Modo url (o app de qualquer pessoa, por endereco; sem Supabase falso): "mode": "url" no roteiro ou REC_MODE=url, e
//   APP_URL=http://127.0.0.1:3000 TUT_USER=... TUT_SENHA=... node rec/record.mjs meu.json     (ver rec/README.md)
// Opcoes:
//   --out <pasta>         onde gravar as saidas (padrao: pasta do roteiro)
//   --name <nome>         nome base dos arquivos (padrao: "name" do roteiro ou nome do arquivo)
//   --cursor-overlay      DEPURACAO: desenha um cursor na pagina (o video final nao leva cursor)
//   --headed              abre a janela do navegador (so com tela)
//   --keep-frames         mantem os quadros JPEG em <out>/_frames
//   --no-encode           so captura + telemetria (sem montar o MP4)
//   --no-reset            nao reinicia os dados do Supabase falso antes de gravar (so fakebase; no modo url nao ha reset)
//   --check               so confere o roteiro (passos, alvos, `at`) e sai; nao abre o navegador
//   --preset <x264>       preset do x264 (padrao veryfast)    --crf <n>   (padrao 16)
// Requisitos (fakebase): rec/run.sh up (Supabase falso + app no ar); modo url: o app no ar no endereco de APP_URL.
// Nao rode duas gravacoes ao mesmo tempo.
import path from 'node:path';
import { runScript, loadScript, validateScript, missingEnvVars } from './recorder/runner.mjs';

const argv = process.argv.slice(2);
const flag = (n) => argv.includes(n);
const val = (n) => {
  const i = argv.indexOf(n);
  return i >= 0 ? argv[i + 1] : undefined;
};
const file = argv.find((a, i) => !a.startsWith('--') && (i === 0 || !['--out', '--name', '--preset', '--crf'].includes(argv[i - 1])));
if (!file) {
  console.error('uso: node rec/record.mjs <roteiro.json|.mjs> [--out pasta] [--name nome] [--cursor-overlay] [--keep-frames] [--no-encode]');
  process.exit(2);
}

const script = await loadScript(file);
if (flag('--check')) {
  const lint = validateScript(script);
  // "$NOME" nos passos type: aqui so avisa (conferir o roteiro nao exige as credenciais); gravar exige
  const envMissing = missingEnvVars(script).map((m) => `variavel de ambiente ${m.name} ${m.empty ? 'vazia' : 'nao definida'} neste ambiente (${m.where.join(', ')}): a gravacao exige`);
  const warnings = [...lint.warnings, ...envMissing];
  if (lint.mode === 'url') console.log(`modo url (${lint.modeSource})`);
  for (const w of warnings) console.log(`aviso: ${w}`);
  for (const e of lint.errors) console.log(`ERRO: ${e}`);
  console.log(lint.errors.length ? `roteiro com ${lint.errors.length} erro(s)` : `roteiro ok (${script.steps.length} passos${warnings.length ? `, ${warnings.length} aviso(s)` : ''})`);
  process.exit(lint.errors.length ? 1 : 0);
}
const name = val('--name') || script.name || path.basename(file).replace(/\.(json|mjs)$/, '');
const outDir = val('--out') || script.outDir || path.dirname(path.resolve(file));
console.log(`gravando "${name}" -> ${outDir}`);
const res = await runScript(script, {
  name,
  outDir,
  headed: flag('--headed'),
  cursorOverlay: flag('--cursor-overlay') || undefined,
  keepFrames: flag('--keep-frames'),
  noEncode: flag('--no-encode'),
  noReset: flag('--no-reset') || undefined,
  preset: val('--preset'),
  crf: val('--crf') ? Number(val('--crf')) : undefined,
});
console.log('\nsaidas:');
for (const [k, v] of Object.entries(res.files)) if (v) console.log(`  ${k.padEnd(10)} ${v}`);
console.log('\nestatisticas:', JSON.stringify(res.stats, null, 2));
if (res.probe) console.log('video:', JSON.stringify({ w: res.probe.width, h: res.probe.height, fps: res.probe.r_frame_rate, codec: res.probe.codec_name, pix: res.probe.pix_fmt, cs: res.probe.color_space, range: res.probe.color_range, nb: res.probe.nb_frames, dur: res.probe.duration }));
if (!res.ok) {
  console.error(`\nFALHOU no passo ${res.failure.i} (${res.failure.do}): ${res.failure.error}`);
  process.exit(1);
}
