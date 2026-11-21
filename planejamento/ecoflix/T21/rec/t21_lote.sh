#!/bin/bash
# T21 · lote em segundo plano: cada item "NN:modo" roda pela fila (prioridade 21), um capítulo por vez, em ordem.
# Uso: bash rec/t21/t21_lote.sh 00:r 01:r 02:r 02b:r ... (modo r = rápido, c = completo). Exige TUT_USER no ambiente (a senha é gerada no corpo).
# Para sozinho se o disco cair abaixo de 450 MB. Log: redirecione para /dev/shm/t21_lote*.log.
cd /home/claude/ecoflix
for it in "$@"; do
  IFS=: read -r N M <<< "$it"
  echo "== $it $(date +%H:%M:%S)"
  bash rec/fila.sh --prio 21 -- bash rec/t21/t21_corpo.sh "$N" "$M"
  rc=$?; echo "== $it saiu rc=$rc $(date +%H:%M:%S)"
  [ $rc = 4 ] && { echo "PARADO: disco"; break; }
done
echo "== FIM do lote $(date +%H:%M:%S)"
