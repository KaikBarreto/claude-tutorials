#!/usr/bin/env bash
# T17 · fase 2 (06/11) · uso: rec/t17/lote.sh [--gravar] NN NN ...
#   sem --gravar: ensaio --rapido dos capítulos, NA ORDEM, uma trava por capítulo; resumo em rec/t17/_debug/ens-NN.log
#   --gravar:     gravação completa (G) dos capítulos, uma trava por capítulo; resumo em rec/t17/_debug/rec-NN.log
#   Nenhum capítulo grava no banco: todos partem de `t17/inicio` (cadeia.json). O rodar.sh religa a 54342 (fora da trava) se ela caiu.
cd /home/claude/domiflix
mkdir -p rec/t17/_debug
MODO="--rapido"; PRE="ens"
if [ "${1:-}" = "--gravar" ]; then MODO=""; PRE="rec"; shift; fi
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  echo "início $(date +%H:%M:%S)" > rec/t17/_debug/$PRE-$NN.log
  rec/t17/rodar.sh "$NN" $MODO >> rec/t17/_debug/$PRE-$NN.log 2>&1
  echo "fim $PRE $NN $(date +%H:%M:%S)" >> rec/t17/_debug/$PRE-$NN.log
done
