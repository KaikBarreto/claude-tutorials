#!/usr/bin/env bash
# T13 · fila de ensaios, um capítulo por vez e uma trava por capítulo (t13_ensaio.sh). Não editar com a fila rodando: copie antes.
# Uso: bash rec/t13/t13_fila.sh <rapido|completo> <cadeia|solto> NN [NN ...]
#   cadeia: cada capítulo captura a semente apos-capNN (--semente) e a fila PARA no 1º capítulo com passo falho ou sem semente
#   solto : só ensaia (capítulos que partem de sementes já prontas)
# Log: rec/t13/_ens/fila-<pid>.log (o resumo de cada capítulo).
set -u
cd "$(dirname "$0")/../.."
MODO=$1; TIPO=$2; shift 2
mkdir -p rec/t13/_ens
LOG=rec/t13/_ens/fila-$$.log
echo "##### fila $MODO $TIPO: $* ($(date +%H:%M:%S))" >> "$LOG"
for NN in "$@"; do
  echo "##### cap$NN $(date +%H:%M:%S)" >> "$LOG"
  if [ "$TIPO" = cadeia ]; then
    OUT=$(bash rec/t13/t13_ensaio.sh "$NN" "$MODO" --semente 2>&1)
  else
    OUT=$(bash rec/t13/t13_ensaio.sh "$NN" "$MODO" 2>&1)
  fi
  echo "$OUT" >> "$LOG"
  echo "cap$NN: $(echo "$OUT" | grep -E '^rc=|^t13/apos' | tr '\n' ' ')"
  if [ "$TIPO" = cadeia ]; then
    echo "$OUT" | grep -q '^rc=0 falhos=0' && echo "$OUT" | grep -q "^t13/apos-cap$NN" || { echo "cadeia parada em cap$NN"; exit 1; }
  fi
done
echo "##### fim $(date +%H:%M:%S)" >> "$LOG"
