#!/usr/bin/env bash
# T21 · põe UM capítulo na fila justa da trava pesada (rec/fila.sh, prioridade 21) e, na vez dele, roda o t21_dentro.sh.
# No máximo uma tarefa da T21 na fila (regra do coordenador, 11/11). Gera os roteiros antes (o t21_dentro.sh lê o capNN.json
# na hora de gravar, então o roteiro que vale é o da hora em que a vez chega).
# Uso: TUT_USER=... TUT_SENHA=... bash rec/t21/t21_fila.sh NN|2b ens|ambos|completo
set -uo pipefail
cd /home/claude/ecoflix
: "${TUT_USER:?defina TUT_USER}"; : "${TUT_SENHA:?defina TUT_SENHA}"
python3 -I rec/t21/gerar.py > /dev/null || exit 4
exec bash rec/fila.sh --prio 21 -- bash rec/t21/t21_dentro.sh "$1" "${2:-ens}"
