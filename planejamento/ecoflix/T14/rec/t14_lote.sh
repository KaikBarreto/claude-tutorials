#!/usr/bin/env bash
# T14 · capítulos em sequência, UMA entrada por vez na fila (rec/fila.sh): cada item é NN (só o rápido) ou NN+ (rápido e, limpo, o
# completo). Não começa capítulo novo depois de 95 min (o fundo morre em 2 h): imprime os que faltam.
#   bash rec/t14/t14_lote.sh 03 04+ 05 ...
cd "$(dirname "$0")/../.."
t0=$(date +%s)
for it in "$@"; do
  if [ $(( $(date +%s) - t0 )) -gt 5700 ]; then echo "FALTAM: $*"; exit 0; fi
  shift
  echo "##### cap$it $(date +%H:%M:%S)"
  case "$it" in
    *+) bash rec/t14/t14_cap.sh "${it%+}" 2>&1 | tail -6 ;;
    *)  bash rec/t14/t14_rapido.sh "$it" 2>&1 | tail -6 ;;
  esac
done
echo "##### FIM $(date +%H:%M:%S)"
