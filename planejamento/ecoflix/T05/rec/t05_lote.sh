#!/usr/bin/env bash
# T05 · ensaios rápidos em sequência, um por vez na fila (no máximo uma tarefa na fila). Uso: bash rec/t05/t05_lote.sh 01 02 ...
cd /home/claude/ecoflix
for n in "$@"; do bash rec/t05/t05_ens.sh "$n"; done
