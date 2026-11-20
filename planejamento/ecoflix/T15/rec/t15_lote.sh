#!/usr/bin/env bash
# T15: ensaio rápido (com MP4) de uma lista de capítulos em sequência, cada um pela fila (--prio 15), e prever.py de cada um.
# Uso: bash rec/t15/t15_lote.sh 00 01 02 ...   (saídas: rec/t15/_ens/lote_NN.txt e rec/t15/_ens/prever_NN.txt)
cd "$(dirname "$0")/../.."
for NN in "$@"; do
  bash rec/t15/t15_ens.sh "$NN" > rec/t15/_ens/lote_$NN.txt 2>&1
  python3 -I rec/t15/prever.py "$NN" --ens > rec/t15/_ens/prever_$NN.txt 2>&1
done
echo FIM > rec/t15/_ens/lote_FIM.txt
