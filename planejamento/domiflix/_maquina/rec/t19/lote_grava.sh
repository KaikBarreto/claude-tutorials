#!/usr/bin/env bash
# T19 · GRAVAÇÃO (fase 2): rec/t19/rodar.sh NN [--seed] com `at`, um capítulo por vez, uma trava por capítulo; resumo em rec/t19/_debug/grav-NN.log
#   uso: rec/t19/lote_grava.sh 0 1 2 ...     (cadeia: cada capítulo parte do apos-capNN do anterior; --seed só nos que mudam o mundo)
cd /home/claude/domiflix
mkdir -p rec/t19/_debug
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  S=""; case "$((10#$n))" in 2|3|6|8|10|12) S="--seed";; esac
  curl -s -o /dev/null --max-time 5 -w "" http://127.0.0.1:8080/ || { echo "8080 fora do ar" > rec/t19/_debug/grav-$NN.log; continue; }
  rec/t19/rodar.sh "$NN" $S > rec/t19/_debug/grav-$NN.log 2>&1
  echo "fim grav $NN" >> rec/t19/_debug/grav-$NN.log
done
