#!/usr/bin/env bash
# T11 · lote de ensaios rápidos (ou do que vier em "$@" depois do número): uma trava por capítulo (o rodar.sh pega e solta a trava de cada um).
# Uso: rec/t11/lote.sh "0 --rapido" "1 --rapido" "2 --rapido --seed" ...   (cada argumento = os argumentos do rodar.sh)
cd /home/claude/domiflix
mkdir -p rec/t11/_debug
for a in "$@"; do
  n=$(printf '%02d' "$((10#${a%% *}))")
  rec/t11/rodar.sh $a > rec/t11/_debug/rod-$n.log 2>&1
  echo "fim $a" >> rec/t11/_debug/rod-$n.log
done
