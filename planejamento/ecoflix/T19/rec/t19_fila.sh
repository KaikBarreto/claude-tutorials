#!/usr/bin/env bash
# T19 · lote de itens, UM de cada vez na fila justa da trava (rec/fila.sh --prio 19: nunca mais de uma tarefa da aula na fila).
# Itens: "NN:modos" (ens, final, seed; ex. 03:ens,final,seed) ou "ex:<arquivo de rec/t19/_ex sem .json>". Com prazo: item que
# ganha a vez a menos de 12 min do fim do lote não grava (o lote em segundo plano não morre no meio de uma gravação). Para no
# primeiro capítulo com seed pedida que não gravou a semente (a cadeia depende dela).
#   PRAZO_MIN=115 bash rec/t19/t19_fila.sh 02:ens,final,seed 03:ens,seed ...   (saída de cada item em /dev/shm/t19/fila-<item>.txt)
set -uo pipefail
TUT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$TUT_HOME"
export PRAZO_FIM=$(( $(date +%s) + ${PRAZO_MIN:-115} * 60 ))
for it in "$@"; do
  if (( $(date +%s) > PRAZO_FIM - 15 * 60 )); then echo "PRAZO: parei antes de $it"; exit 0; fi
  if [[ $it == ex:* ]]; then
    n=${it#ex:}
    FAKE_URL=http://127.0.0.1:54319 FAKE_NOW=2026-11-10T08:30:00-03:00 bash /home/claude/ecoflix/rec/fila.sh --prio 19 -- timeout 400 node rec/t19/explorar.mjs "rec/t19/_ex/$n.json" --out "/dev/shm/t19/$n" > "/dev/shm/t19/$n.log" 2>&1
    echo "$it: exit $?"
    continue
  fi
  NN=${it%%:*}; MODOS=${it#*:}; ARGS=()
  for m in ${MODOS//,/ }; do ARGS+=("--$m"); done
  bash rec/t19/t19_rodar.sh "$NN" "${ARGS[@]}" > "/dev/shm/t19/fila-$NN.txt" 2>&1
  rc=$?
  echo "$it: exit $rc $(date +%H:%M)"
  [[ $rc == 5 ]] && { echo "PRAZO: a vez chegou tarde para $it"; exit 0; }
  if [[ $MODOS == *seed* ]] && grep -q 'NAO GRAVADA' "/dev/shm/t19/fila-$NN.txt"; then echo "PAREI: cap$NN sem semente"; exit 0; fi
done
echo "fila completa"
