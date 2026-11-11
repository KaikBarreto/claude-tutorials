#!/usr/bin/env bash
# T19 · fila de itens, UM por trava, com prazo: cada item espera a trava só o que cabe antes do fim do lote (FLOCK_W), para o lote em
# segundo plano não morrer no meio de uma gravação. Itens: "NN:modos" (modos separados por vírgula: ens, final, seed; ex. 03:ens,final,seed)
# ou "ex:<arquivo de rec/t19/_ex sem .json>". Para no primeiro capítulo com seed pedida que não gravou a semente (a cadeia depende dela).
#   PRAZO_MIN=110 bash rec/t19/t19_fila.sh 02:ens,final,seed 03:ens,final,seed ...   (saída de cada item em /dev/shm/t19/fila-<item>.txt)
set -uo pipefail
TUT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$TUT_HOME"
FIM=$(( $(date +%s) + ${PRAZO_MIN:-110} * 60 ))
for it in "$@"; do
  RESTA=$(( FIM - $(date +%s) - 14 * 60 ))
  if (( RESTA < 60 )); then echo "PRAZO: parei antes de $it"; exit 0; fi
  if [[ $it == ex:* ]]; then
    n=${it#ex:}
    FAKE_URL=http://127.0.0.1:54319 FAKE_NOW=2026-11-10T08:30:00-03:00 flock -w "$RESTA" .heavy.lock timeout 400 node rec/t19/explorar.mjs "rec/t19/_ex/$n.json" --out "/dev/shm/t19/$n" > "/dev/shm/t19/$n.log" 2>&1
    echo "$it: exit $?"
    continue
  fi
  NN=${it%%:*}; MODOS=${it#*:}; ARGS=()
  for m in ${MODOS//,/ }; do ARGS+=("--$m"); done
  FLOCK_W=$RESTA bash rec/t19/t19_rodar.sh "$NN" "${ARGS[@]}" > "/dev/shm/t19/fila-$NN.txt" 2>&1
  rc=$?
  echo "$it: exit $rc"
  [[ $rc == 5 ]] && { echo "PRAZO: a trava não veio para $it"; exit 0; }
  if [[ $MODOS == *seed* ]] && grep -q 'NAO GRAVADA' "/dev/shm/t19/fila-$NN.txt"; then echo "PAREI: cap$NN sem semente"; exit 0; fi
done
echo "fila completa"
