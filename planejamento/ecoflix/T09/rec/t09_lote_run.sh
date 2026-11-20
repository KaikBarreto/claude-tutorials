#!/usr/bin/env bash
# lote de ensaio rápido da T09 (todos os capítulos, um atrás do outro, pela fila --prio 09)
cd /home/claude/ecoflix
for NN in 00 01 02 03 04 05 06 07 08 09 10 11; do
  bash rec/t09/t09_lote1.sh "$NN" 2>&1 | tail -12
done
echo "FIM DO LOTE $(date +%T)"
