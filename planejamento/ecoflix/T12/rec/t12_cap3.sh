#!/bin/bash
# T12 · um capítulo pela fila justa da trava pesada (rec/fila.sh, prioridade 12; uma tarefa minha por vez, regra do coordenador de 11/11):
# gera o roteiro e o ensaio rápido FORA da trava e roda o t12_dentro.sh (gravação, semente, prever, completo) quando chegar a vez.
# O completo só sai quando o prever acusa gesto com atraso >= 0,4 s, quando o capítulo tem gesto sensível a espera ou quando o rápido teve
# aviso (erro de página, aviso de erro na tela).
# Uso (em segundo plano, prazo de 2 h): bash rec/t12/t12_cap3.sh NN [--so-rapido|--so-completo]
set -u
cd /home/claude/ecoflix
NN=$(printf '%02d' "$((10#$1))"); MODO=${2:-}
python3 -I rec/t12/gerar.py "$NN" | tail -1
python3 -I rec/t12/ensaio.py "$NN" >/dev/null
echo "cap$NN entra na fila $(date +%H:%M:%S)"
bash /home/claude/ecoflix/rec/fila.sh --prio 12 -- bash rec/t12/t12_dentro.sh "$NN" $MODO
echo "cap$NN fim $(date +%H:%M:%S) exit $?"
