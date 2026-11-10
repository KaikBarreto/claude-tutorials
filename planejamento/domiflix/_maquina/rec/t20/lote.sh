#!/usr/bin/env bash
# T20 · ensaio --rapido dos capítulos pedidos, NA ORDEM, uma trava por capítulo; só o cap. 3 grava semente (apos-cap03); resumo em rec/t20/_debug/ens-NN.log
cd /home/claude/domiflix
mkdir -p rec/t20/_debug
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  S=""; [ "$NN" = "03" ] && S="--seed"
  rec/t20/rodar.sh "$NN" --rapido $S > rec/t20/_debug/ens-$NN.log 2>&1
  curl -s http://127.0.0.1:54335/__dev/unknowns | head -c 600 >> rec/t20/_debug/ens-$NN.log
  echo "fim ens $NN" >> rec/t20/_debug/ens-$NN.log
done
