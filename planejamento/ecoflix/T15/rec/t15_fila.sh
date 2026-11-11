#!/usr/bin/env bash
# T15: põe na fila da trava pesada (cada item com a sua trava) os itens dados: "NN" = ensaio rápido com MP4, "NN:completo" = gravação.
# Roda desanexado (setsid nohup) para não morrer no prazo das tarefas de fundo; o resultado de cada item vai para /dev/shm/t15_q_<item>.log.
cd "$(dirname "$0")/../.."
for it in "$@"; do
  nn=${it%%:*}; modo=rapido; [ "$it" != "$nn" ] && modo=${it#*:}
  setsid nohup bash rec/t15/t15_ens.sh "$nn" "$modo" > "/dev/shm/t15_q_${nn}_${modo}.log" 2>&1 < /dev/null &
done
