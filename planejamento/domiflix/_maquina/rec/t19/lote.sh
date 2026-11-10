#!/usr/bin/env bash
# T19 · ensaio --rapido (+ semente apos-capNN) dos capítulos pedidos, NA ORDEM, uma trava por capítulo; resumo em rec/t19/_debug/ens-NN.log
#   uso: rec/t19/lote.sh 0 1 2 3 4      (a cadeia precisa da ordem: cada capítulo parte do apos-capNN do anterior)
cd /home/claude/domiflix
mkdir -p rec/t19/_debug
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  rec/t19/rodar.sh "$NN" --rapido --seed > rec/t19/_debug/ens-$NN.log 2>&1
  echo "fim ens $NN" >> rec/t19/_debug/ens-$NN.log
done
