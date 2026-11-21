#!/bin/bash
# T27 · lote em segundo plano: cada item "NN:modo[:sem]" roda pela fila (prioridade 27). Uso: bash rec/t27/t27_lote.sh 00:r 01:r 04:r:sem ...
# Para sozinho se o disco cair abaixo de 450 MB. Log: redirecione para /dev/shm/t27_lote*.log.
cd /home/claude/ecoflix
for it in "$@"; do
  IFS=: read -r N M S <<< "$it"
  echo "== $it $(date +%H:%M:%S)"
  bash rec/fila.sh --prio 27 -- bash rec/t27/t27_corpo.sh "$N" "$M" ${S:-}
  rc=$?; echo "== $it saiu rc=$rc $(date +%H:%M:%S)"
  [ $rc = 4 ] && { echo "PARADO: disco"; break; }
done
echo "== FIM do lote $(date +%H:%M:%S)"
