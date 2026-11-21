#!/bin/bash
# T05 · lote em segundo plano: cada item "NN:modo" (r rápido, c completo) roda pela fila (prioridade 05). Uso: bash rec/t05/t05_lote.sh 00:r 01:r 06:c ...
# Para sozinho se o disco cair abaixo de 450 MB. Log: redirecione para /dev/shm/t05_lote*.log. (Substitui o t05_lote.sh antigo, que chamava t05_ens.sh.)
cd /home/claude/ecoflix
for it in "$@"; do
  IFS=: read -r N M <<< "$it"
  echo "== $it $(date +%H:%M:%S)"
  bash rec/fila.sh --prio 05 -- bash rec/t05/t05_corpo.sh "$N" "$M"
  rc=$?; echo "== $it saiu rc=$rc $(date +%H:%M:%S)"
  [ $rc = 4 ] && { echo "PARADO: disco"; break; }
done
echo "== FIM do lote $(date +%H:%M:%S)"
