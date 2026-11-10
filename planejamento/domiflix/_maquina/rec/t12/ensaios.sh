#!/usr/bin/env bash
# T12 · ensaio --rapido dos capítulos pedidos (uma trava por capítulo), log por capítulo em rec/t12/_debug/ens-NN.log
cd /home/claude/domiflix
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  rec/t12/rodar.sh "$NN" --rapido > rec/t12/_debug/ens-$NN.log 2>&1
  echo "fim ens $NN" >> rec/t12/_debug/ens-$NN.log
done
