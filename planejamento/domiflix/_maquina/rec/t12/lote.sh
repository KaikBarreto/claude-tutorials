#!/usr/bin/env bash
# T12 · gravação real dos capítulos pedidos, uma trava por capítulo; resumo em rec/t12/_debug/rec-NN.log
cd /home/claude/domiflix
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  rec/t12/rodar.sh "$NN" > rec/t12/_debug/rec-$NN.log 2>&1
  echo "fim rec $NN" >> rec/t12/_debug/rec-$NN.log
done
