#!/usr/bin/env bash
# T13 · fase 2: grava os capítulos pedidos NA ORDEM (uma trava por capítulo, dentro do rodar.sh); uso: rec/t13/gravar_lote.sh 0 1 2 ...
# espera o lote de ensaios terminar (PID em $ESPERA) para não misturar o mundo do fake
cd /home/claude/domiflix
mkdir -p rec/t13/_debug
while [ -n "${ESPERA:-}" ] && kill -0 "$ESPERA" 2>/dev/null; do sleep 10; done
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  rec/t13/rodar.sh "$NN" > rec/t13/_debug/rec-$NN.log 2>&1
  echo "fim rec $NN" >> rec/t13/_debug/rec-$NN.log
done
