#!/usr/bin/env bash
# T26 · roda uma lista de capítulos em sequência, cada um com a SUA trava (t26_rodar.sh), parando no primeiro que falhar.
#   bash rec/t26/t26_fila.sh "00 01 02" --ens
#   bash rec/t26/t26_fila.sh "07:ens 08 09 dia 12 13:ens" --ambos   (NN:modo troca o modo só daquele capítulo; "dia" monta a semente
#                                                                     apos-cap11-dia dos caps 12 e 13 com o aux/t26_dia.py)
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LISTA="$1"; shift
# roda uma CÓPIA do t26_rodar.sh: editar o original durante a fila não mexe no que o bash está lendo (docs/08: rodar.sh editado no meio)
COPIA="/dev/shm/t26_rodar.$$.sh"
cp "$DIR/t26_rodar.sh" "$COPIA"
trap 'rm -f "$COPIA"' EXIT
export T26_HOME="$(cd "$DIR/../.." && pwd)"
for item in $LISTA; do
  if [ "$item" = dia ]; then
    (cd "$T26_HOME" && python3 -I rec/t26/aux/t26_dia.py) || { echo "== fila parou no t26_dia.py"; exit 1; }
    continue
  fi
  n="${item%%:*}"
  if [ "$item" != "$n" ]; then
    bash "$COPIA" "$n" "--${item#*:}" || { echo "== fila parou no cap$n"; exit 1; }
  else
    bash "$COPIA" "$n" "$@" || { echo "== fila parou no cap$n"; exit 1; }
  fi
done
echo "== fila ok: $LISTA"
