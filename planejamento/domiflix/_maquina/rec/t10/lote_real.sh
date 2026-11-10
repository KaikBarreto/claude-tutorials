#!/usr/bin/env bash
# T10 · gravação REAL (com vídeo) dos capítulos pedidos, NA ORDEM, uma trava por capítulo (+ semente apos-capNN); resumo em rec/t10/_debug/real-NN.log
cd /home/claude/domiflix
mkdir -p rec/t10/_debug
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  rec/t10/rodar.sh "$NN" --seed > rec/t10/_debug/real-$NN.log 2>&1
  echo "fim real $NN" >> rec/t10/_debug/real-$NN.log
done
