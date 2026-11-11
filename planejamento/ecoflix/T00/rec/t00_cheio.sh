#!/bin/bash
# T0 · gravação COMPLETA (com os `at`), uma tarefa por vez pela fila. Uso: bash rec/t00/t00_cheio.sh 01 01.9x16 ...
cd /home/claude/ecoflix
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54300
for n in "$@"; do
  echo "== cap$n"; bash rec/fila.sh --prio 00 -- node rec/record.mjs rec/t00/cap$n.json --preset ultrafast --crf 30 > /dev/shm/t00_full_$n.out 2>&1; grep -c FALHOU /dev/shm/t00_full_$n.out
done
echo LOTE-FIM
