#!/usr/bin/env bash
# T21 · fase 2 (06/11) · uso: rec/t21/lote.sh [--gravar] NN NN ...
#   sem --gravar: ensaio --rapido dos capítulos, NA ORDEM, uma trava por capítulo; resumo em rec/t21/_debug/ens-NN.log
#   --gravar:     gravação completa (G) dos capítulos, uma trava por capítulo; resumo em rec/t21/_debug/rec-NN.log
#   NUNCA grava semente: as seeds-extra/t21/apos-capNN.json de 05/11 valem (o rodar.sh recusa --seed na fase 2).
#   O rodar.sh troca o FAKE_NOW da 54340 (fora da trava) quando o capítulo pede outro dia (caps 8 e 10: 13/11 15:00).
cd /home/claude/domiflix
mkdir -p rec/t21/_debug
MODO="--rapido"; PRE="ens"
if [ "${1:-}" = "--gravar" ]; then MODO=""; PRE="rec"; shift; fi
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  echo "início $(date +%H:%M:%S)" > rec/t21/_debug/$PRE-$NN.log
  rec/t21/rodar.sh "$NN" $MODO >> rec/t21/_debug/$PRE-$NN.log 2>&1
  curl -s http://127.0.0.1:54340/__dev/unknowns | head -c 600 >> rec/t21/_debug/$PRE-$NN.log
  echo "" >> rec/t21/_debug/$PRE-$NN.log
  echo "fim $PRE $NN $(date +%H:%M:%S)" >> rec/t21/_debug/$PRE-$NN.log
done
