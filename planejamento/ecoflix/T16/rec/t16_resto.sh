#!/usr/bin/env bash
# T16 · os capítulos que faltam, um por vez na fila justa (cada um tira a sua senha só quando o anterior termina: uma tarefa
# por vez na fila). Uso: bash rec/t16/t16_resto.sh [NN ...]   (sem argumento: a lista abaixo, na ordem)
# Cada capítulo: t16_lote3.sh (rápido com MP4 + resumo + prever; o completo só quando a regra de 11/11 pede). O log fica em
# rec/t16/t16_resto.log; as folhas de contato (rec/t16/_ens/t16-capNN.contact.jpg e rec/t16/t16-capNN.contact.jpg) ficam para
# olhar e apagar depois. --completo = gesto sensível a espera (menu/lista aberta com a fala andando, tela que muda sozinha).
cd "$(dirname "$0")/../.."
declare -A OPC=( [00]="" [01]="" [02]="" [03]="--semente" [04]="--semente --completo" [05]="--semente --completo"
  [06]="--semente" [07]="--semente --completo" [08]="--completo" [09]="--semente --completo" [10]="--semente --completo"
  [11]="--semente --completo" [12]="--semente --completo" [13]="--semente --completo" [14]="--semente --completo"
  [15]="--semente --completo" [16]="--semente --completo" [17]="--semente --completo" [18]="" )
LISTA=${*:-04 05 07 08 11 12 13 14 15 16 17 00 01 02 03 06 18}
for n in $LISTA; do
  NN=$(printf '%02d' "$((10#$n))")
  echo "== cap$NN $(date +%T) ${OPC[$NN]}" >> rec/t16/t16_resto.log
  bash rec/t16/t16_lote3.sh "$NN" ${OPC[$NN]} >> rec/t16/t16_resto.log 2>&1
done
echo "== fim $(date +%T)" >> rec/t16/t16_resto.log
