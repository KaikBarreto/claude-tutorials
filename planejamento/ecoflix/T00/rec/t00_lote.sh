#!/bin/bash
# T0 · ensaio rápido em lote, um flock por capítulo. Uso: bash rec/t00/t00_lote.sh 02 03 ...  (sufixos: d e p)
cd /home/claude/ecoflix
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54300
for n in "$@"; do for s in "" ".9x16"; do
  echo "== cap$n$s"; flock .heavy.lock node rec/record.mjs rec/t00/_ens/cap$n$s.json --rapido 2>&1 | tail -25
done; done
echo LOTE-FIM
