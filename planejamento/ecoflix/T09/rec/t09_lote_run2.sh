#!/usr/bin/env bash
# lote 3 da T09: só os capítulos que falharam no lote 1 (e o cap04, com o L6 enxugado)
cd /home/claude/ecoflix
for NN in 10; do
  bash rec/t09/t09_lote1.sh "$NN" 2>&1 | tail -12
done
echo "FIM DO LOTE 6 $(date +%T)"
