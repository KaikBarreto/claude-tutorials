#!/usr/bin/env bash
cd "$(dirname "$(readlink -f "$0")")/../.."
OUT=/dev/shm/t02rec; : > "$OUT/lote2.txt"
for n in 12 13; do
  { echo "=== ens cap$n"; bash rec/t02/t02_rodar.sh "$n" --ens 2>&1 | tail -4; python3 -I rec/t02/resumo.py "$n" --ens 2>&1 | tail -25; } >> "$OUT/lote2.txt" 2>&1
done
for n in 04 05 07; do
  { echo "=== completo cap$n"; bash rec/t02/t02_rodar.sh "$n" 2>&1 | tail -4; python3 -I rec/t02/resumo.py "$n" 2>&1 | tail -30; python3 -I rec/t02/prever.py "$n" 2>&1 | tail -6; } >> "$OUT/lote2.txt" 2>&1
done
echo FIM >> "$OUT/lote2.txt"
