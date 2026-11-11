#!/usr/bin/env bash
# T13 · lote de ensaios em sequência, uma tarefa por vez na fila justa (rec/fila.sh pelo t13_ensaio4.sh). Não editar com o lote rodando.
# Uso: bash rec/t13/t13_lote.sh NN:modo [NN:modo ...]     (modo: rapido | completo)
# Não começa capítulo novo depois de 95 min (a tarefa de fundo morre em 2 h): imprime "FALTAM: ..." para relançar o resto.
set -u
cd "$(dirname "$0")/../.."
INI=$(date +%s)
mkdir -p rec/t13/_ens
LOG=rec/t13/_ens/lote-$$.log
RESTO=("$@")
for item in "$@"; do
  if [ $(( $(date +%s) - INI )) -gt 5700 ]; then echo "FALTAM: ${RESTO[*]}"; exit 5; fi
  NN=${item%%:*}; MODO=${item#*:}
  echo "##### cap$NN $MODO $(date +%H:%M:%S)" >> "$LOG"
  OUT=$(bash rec/t13/t13_ensaio4.sh "$NN" "$MODO" 2>&1)
  echo "$OUT" >> "$LOG"
  echo "cap$NN $MODO: $(echo "$OUT" | grep -E '^rc=' | tr '\n' ' ') $(echo "$OUT" | grep -oE 'maxLate [0-9.]+' | head -1)"
  RESTO=("${RESTO[@]:1}")
done
echo "##### fim $(date +%H:%M:%S)" >> "$LOG"
echo "LOTE FIM"
