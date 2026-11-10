#!/usr/bin/env bash
# T20 · fase 2 (gravação): rec/t20/gravar_lote.sh 0 1 2 ...  -> grava cada capítulo (uma trava por capítulo), resumo em rec/t20/_debug/grav-NN.log
cd /home/claude/domiflix
mkdir -p rec/t20/_debug
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  df -k --output=avail /home/claude | tail -1 | awk '{ if ($1 < 1572864) { print "DISCO BAIXO"; exit 1 } }' || { echo "disco baixo antes do cap $NN" > rec/t20/_debug/PARADO.txt; exit 1; }
  rec/t20/rodar.sh "$NN" > rec/t20/_debug/grav-$NN.log 2>&1
  curl -s http://127.0.0.1:54335/__dev/unknowns | head -c 400 >> rec/t20/_debug/grav-$NN.log
  echo "fim grav $NN" >> rec/t20/_debug/grav-$NN.log
done
