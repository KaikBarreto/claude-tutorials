#!/usr/bin/env bash
# T7 · renders dos capítulos (fase 2 na 1.38.24): um `render_um.sh NN` por vez, cada um com a própria posse da trava
# (o render_um.sh faz `flock $TUT_HOME/.heavy.lock nice -n 10`). Antes de cada capítulo confere o disco (>= 1,5 GB); senão para.
# Uso: bash rec/t7/fila_render.sh 0 1 2 ...   (saída: t7/edit/out/render_um_NN.out e o resumo em t7/edit/out/_fila_render.txt)
set -uo pipefail
cd /home/claude/domiflix
RES=t7/edit/out/_fila_render.txt
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  livre=$(df --output=avail -k /home/claude | tail -1)
  if [ "$livre" -lt 1572864 ]; then echo "cap$NN PARADO: disco $((livre / 1024)) MB" >> "$RES"; exit 4; fi
  bash rec/t7/render_um.sh "$n" > "t7/edit/out/render_um_$NN.out" 2>&1; rc=$?
  echo "cap$NN fim $(date +%H:%M) rc=$rc | $(grep -m1 -o 'checagem.*' "t7/edit/out/audit_$NN.log") | $(du -sh "t7/edit/out/cap$NN" | cut -f1) | livre $(df -h /home/claude | tail -1 | awk '{print $4}')" >> "$RES"
done
echo "LOTE FIM $(date +%H:%M): $*" >> "$RES"
