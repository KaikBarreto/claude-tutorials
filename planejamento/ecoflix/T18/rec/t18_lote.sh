#!/bin/bash
# T18 · lote SERIAL pela fila justa (rec/fila.sh --prio 18): no máximo UMA tarefa minha na fila por vez.
# Uso: bash rec/t18/t18_lote.sh 03:r 04:r 05:s ...   (r = ensaio rápido tolerante, s = estrito, c = completo; todos com MP4 ultrafast para a folha)
cd /home/claude/ecoflix
for item in "$@"; do
  NN=${item%%:*}; MODO=${item##*:}
  echo "== $item na fila $(date +%H:%M:%S)"
  bash /home/claude/ecoflix/rec/fila.sh --prio 18 -- bash rec/t18/t18_corpo.sh "$NN" "$MODO"
  echo "== $item saiu com $? $(date +%H:%M:%S)"
done
