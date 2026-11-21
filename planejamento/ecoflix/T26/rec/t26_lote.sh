#!/bin/bash
# T26 · lote SERIAL pela fila justa (rec/fila.sh --prio 26): no máximo UMA tarefa minha na fila por vez.
# Uso: bash rec/t26/t26_lote.sh 03:r 04:r 05:s ...   (r = ensaio rápido tolerante, s = estrito, c = completo; todos com MP4 ultrafast para a folha)
cd /home/claude/ecoflix
for item in "$@"; do
  NN=${item%%:*}; MODO=${item##*:}
  LIVRE=$(df -m / | awk 'NR==2{print $4}'); echo "disco livre ${LIVRE} MB"; [ "$LIVRE" -lt 450 ] && { echo "PARADO: disco abaixo de 450 MB"; exit 9; }
  echo "== $item na fila $(date +%H:%M:%S)"
  bash /home/claude/ecoflix/rec/fila.sh --prio 26 -- bash rec/t26/t26_corpo.sh "$NN" "$MODO"
  echo "== $item saiu com $? $(date +%H:%M:%S)"
done
