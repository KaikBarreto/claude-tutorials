#!/bin/bash
# T0 · repete só alguns arquivos (nomes sem .json: 03 04 06 07.9x16 ...), uma tarefa por vez pela fila
cd /home/claude/ecoflix
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54300
for n in "$@"; do
  echo "== cap$n"; bash rec/fila.sh --prio 00 -- node rec/record.mjs rec/t00/_ens/cap$n.json --rapido --preset ultrafast --crf 30 > /dev/shm/t00_cap$n.out 2>&1; grep -c FALHOU /dev/shm/t00_cap$n.out
done
echo LOTE-FIM
