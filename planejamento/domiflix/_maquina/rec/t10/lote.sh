#!/usr/bin/env bash
# T10 · ensaio --rapido (+ semente apos-capNN) dos capítulos pedidos, NA ORDEM, uma trava por capítulo; resumo em rec/t10/_debug/ens-NN.log
#   uso: rec/t10/lote.sh 0 1 2 3 4      (a cadeia precisa da ordem: cada capítulo parte do apos-capNN do anterior)
cd /home/claude/domiflix
mkdir -p rec/t10/_debug
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  rec/t10/rodar.sh "$NN" --rapido --seed > rec/t10/_debug/ens-$NN.log 2>&1
  echo "fim ens $NN" >> rec/t10/_debug/ens-$NN.log
done
