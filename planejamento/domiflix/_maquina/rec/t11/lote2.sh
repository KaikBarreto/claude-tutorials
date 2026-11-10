#!/usr/bin/env bash
# T11 · lote com a cadeia do rascunho: depois de cada capítulo 4 a 8 colhe o rascunho do assistente (colher.py) para o capítulo seguinte.
# Uso: rec/t11/lote2.sh "3 --rapido --seed" "4 --rapido" "5 --rapido" ...   (cada argumento = os argumentos do rodar.sh; uma trava por capítulo)
cd /home/claude/domiflix
mkdir -p rec/t11/_debug
for a in "$@"; do
  n=$(printf '%02d' "$((10#${a%% *}))")
  rec/t11/rodar2.sh $a > rec/t11/_debug/rod-$n.log 2>&1
  if [ "$((10#$n))" -ge 4 ] && [ "$((10#$n))" -le 8 ]; then
    ens=""; case "$a" in *--rapido*) ens="--ens" ;; esac
    python3 -I rec/t11/colher.py "$((10#$n))" $ens >> rec/t11/_debug/rod-$n.log 2>&1
  fi
  echo "fim $a" >> rec/t11/_debug/rod-$n.log
done
