#!/bin/bash
# T0 · ensaio rápido em lote, UMA tarefa por vez pela fila justa. Uso: bash rec/t00/t00_lote.sh 02 03 ...
cd /home/claude/ecoflix
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54300
for n in "$@"; do for s in "" ".9x16"; do
  echo "== cap$n$s"; bash rec/fila.sh --prio 00 -- node rec/record.mjs rec/t00/_ens/cap$n$s.json --rapido --preset ultrafast --crf 30 > /dev/shm/t00_cap$n$s.out 2>&1; tail -12 /dev/shm/t00_cap$n$s.out
done; done
echo LOTE-FIM
