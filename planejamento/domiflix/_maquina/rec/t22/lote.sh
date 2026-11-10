#!/usr/bin/env bash
# T22 · fase 2 · uso: rec/t22/lote.sh [--gravar] NN NN ...
#   sem --gravar: ensaio --rapido dos capítulos, NA ORDEM, uma trava por capítulo; resumo em rec/t22/_debug/ens-NN.log
#   --gravar:     gravação completa (G) dos capítulos, uma trava por capítulo; resumo em rec/t22/_debug/rec-NN.log
#   NUNCA grava semente: as seeds-extra/t22/apos-capNN.json de 05/11 valem (o rodar.sh recusa --seed na fase 2).
cd /home/claude/domiflix
mkdir -p rec/t22/_debug
MODO="--rapido"; PRE="ens"
if [ "${1:-}" = "--gravar" ]; then MODO=""; PRE="rec"; shift; fi
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  echo "início $(date +%H:%M:%S)" > rec/t22/_debug/$PRE-$NN.log
  rec/t22/rodar.sh "$NN" $MODO >> rec/t22/_debug/$PRE-$NN.log 2>&1
  curl -s http://127.0.0.1:54337/__dev/unknowns | head -c 600 >> rec/t22/_debug/$PRE-$NN.log
  echo "" >> rec/t22/_debug/$PRE-$NN.log
  echo "fim $PRE $NN $(date +%H:%M:%S)" >> rec/t22/_debug/$PRE-$NN.log
done
