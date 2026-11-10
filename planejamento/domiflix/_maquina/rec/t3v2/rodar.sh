#!/usr/bin/env bash
# T3 v2 · Uso: rec/t3v2/rodar.sh NN  -> gera o roteiro do robô, confere, grava o capítulo NN (flock + nice), resume.
# O Supabase falso do T3 v2 é a instância da porta 54323 (FAKE_PORT=54323 rec/run.sh fake); o app (8080) é compartilhado.
# Depois da gravação (ainda dentro da trava), imprime o estado do banco que o robô deixou (tabelas de etiquetas e campos), para
# conferir com a semente composta apos-capNN.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54323 FAKE_NOW="2026-11-03T09:00:00-03:00"
NN=$(printf '%02d' "$((10#$1))")
# Arquivo de parada (pedido do coordenador, 31/10): checado ANTES de cada capítulo; se existir, não grava nada e sai limpo.
# Para retomar: apagar rec/t3v2/.parar. (Substitua este arquivo só por mv atômico: há lotes lendo-o.)
if [ -e rec/t3v2/.parar ]; then echo "PARADO (rec/t3v2/.parar existe): cap$NN não foi gravado"; exit 0; fi
python3 -I rec/t3v2/gerar.py "$((10#$NN))" | tail -3
node rec/record.mjs rec/t3v2/cap$NN.json --check | tail -2
CMD="node rec/record.mjs rec/t3v2/cap$NN.json --out rec/t3v2 --name t3v2-cap$NN > rec/t3v2/.rec-$NN.log 2>&1; rc=\$?; node rec/t3v2/estado.mjs > rec/t3v2/.estado-$NN.log 2>&1; exit \$rc"
livre=$(df -k --output=avail /home/claude | tail -1)
if [ "$livre" -lt $((3 * 1024 * 1024)) ]; then echo "DISCO BAIXO (< 3 GiB): paro"; exit 3; fi
# TUT_LOCKED=1: o chamador (um lote) já segura a trava; pedir de novo travaria para sempre
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t3v2/.rec-$NN.log
fi
python3 -I rec/t3v2/resumo.py "$((10#$NN))" 2>&1 | head -120
echo "--- estado do banco:"; cat rec/t3v2/.estado-$NN.log 2>/dev/null | head -40
