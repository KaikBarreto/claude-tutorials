#!/bin/bash
# T12 · lote de ensaio: todos os capítulos em sequência, cada um pela fila (prio 12) via t12_cap3.sh. Saída: rec/t12/_ens/lote.log
# Uso (segundo plano, prazo 7200000): bash rec/t12/t12_lote.sh [NN ...]   (sem argumentos: 00 a 16)
cd /home/claude/ecoflix
export TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64)}"
LISTA=("$@"); [ ${#LISTA[@]} -eq 0 ] && LISTA=(00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16)
for NN in "${LISTA[@]}"; do
  echo "##### cap$NN $(date +%H:%M:%S)"
  bash rec/t12/t12_cap3.sh "$NN" 2>&1 | grep -E "^cap|aviso|SEM ALVO|Erro|error" | head -12
done
echo "##### lote terminou $(date +%H:%M:%S)"
