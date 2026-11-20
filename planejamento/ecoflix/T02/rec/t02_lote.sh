#!/usr/bin/env bash
# T2 · ensaio rápido em LOTE (um capítulo por vez pela fila, prioridade 02). Uso: TUT_USER=... TUT_SENHA=... bash rec/t02/t02_lote.sh 00 01 02 ...
# Resultados em /dev/shm/t02rec/lote.txt (resumo.py --ens e prever.py --ens de cada capítulo).
cd "$(dirname "$(readlink -f "$0")")/../.."
OUT=/dev/shm/t02rec; mkdir -p "$OUT"; : > "$OUT/lote.txt"
for n in "$@"; do
  { echo "=================== cap$n"; bash rec/t02/t02_rodar.sh "$n" --ens 2>&1 | tail -6
    python3 -I rec/t02/resumo.py "$n" --ens 2>&1 | tail -45
    python3 -I rec/t02/prever.py "$n" --ens 2>&1 | tail -12; } >> "$OUT/lote.txt" 2>&1
done
echo FIM >> "$OUT/lote.txt"
