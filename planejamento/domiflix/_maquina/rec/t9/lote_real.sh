#!/usr/bin/env bash
# T9 · gravação REAL (com vídeo) dos capítulos pedidos, NA ORDEM, uma trava por capítulo (+ semente apos-capNN); resumo em rec/t9/_debug/real-NN.log
cd /home/claude/domiflix
mkdir -p rec/t9/_debug
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  rec/t9/rodar.sh "$NN" --seed > rec/t9/_debug/real-$NN.log 2>&1
  echo "fim real $NN" >> rec/t9/_debug/real-$NN.log
done
