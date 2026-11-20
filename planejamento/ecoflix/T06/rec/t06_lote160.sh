#!/usr/bin/env bash
# T06 · lote de ensaio rápido de todos os capítulos no app 1.60.18 (um capítulo por vez, pela fila --prio 06 dentro do t06_cap.sh).
# Uso: bash rec/t06/t06_lote160.sh [caps...]   (padrão: todos). Saída resumida em rec/t06/_ens/lote160.log
cd "$(dirname "$0")/../.."
: "${TUT_USER:?}"; : "${TUT_SENHA:?}"
CAPS=("$@"); [ ${#CAPS[@]} -eq 0 ] && CAPS=(00 01 02 03 04 05 06 07 08 09 09b 10 11 12 13 13a 14 15)
LOG=rec/t06/_ens/lote160.log; : > "$LOG"
for c in "${CAPS[@]}"; do
  echo "=== cap$c $(date +%H:%M:%S)" >> "$LOG"
  bash rec/t06/t06_cap.sh "$c" --so-rapido >> "$LOG" 2>&1
  python3 -I rec/t06/prever.py "$c" --ens > "rec/t06/_ens/cap$c.prever.txt" 2>&1
done
echo "=== fim $(date +%H:%M:%S)" >> "$LOG"
