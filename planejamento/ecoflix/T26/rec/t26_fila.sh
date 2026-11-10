#!/usr/bin/env bash
# T26 · roda uma lista de capítulos em sequência, cada um com a SUA trava (t26_rodar.sh), parando no primeiro que falhar.
#   bash rec/t26/t26_fila.sh "00 01 02" --ens
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LISTA="$1"; shift
# roda uma CÓPIA do t26_rodar.sh: editar o original durante a fila não mexe no que o bash está lendo (docs/08: rodar.sh editado no meio)
COPIA="/dev/shm/t26_rodar.$$.sh"
cp "$DIR/t26_rodar.sh" "$COPIA"
trap 'rm -f "$COPIA"' EXIT
export T26_HOME="$(cd "$DIR/../.." && pwd)"
for n in $LISTA; do
  bash "$COPIA" "$n" "$@" || { echo "== fila parou no cap$n"; exit 1; }
done
echo "== fila ok: $LISTA"
