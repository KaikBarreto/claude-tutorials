#!/usr/bin/env bash
# T07 · lote de ensaios rápidos (um capítulo por vez, cada um pela fila): bash rec/t07/t07_lote160.sh 04 05 ...   (TUT_SENHA no ambiente)
cd /home/claude/ecoflix || exit 1
while pgrep -f "t07_ens.sh 3" >/dev/null; do sleep 5; done
for n in "$@"; do
  echo "===== cap$n $(date +%H:%M:%S)"
  bash rec/t07/t07_ens.sh "$n" 2>&1 | grep -v "^t07-\|^  }\|^}\|^video\|^cap[0-9]*\.\(json\|out\|resumo\)" | cut -c1-600
  python3 -I rec/t07/prever.py "$n" --ens > "rec/t07/_ens/cap$(printf '%02d' $((10#$n))).prever.txt" 2>&1
done
echo "===== fim $(date +%H:%M:%S)"
