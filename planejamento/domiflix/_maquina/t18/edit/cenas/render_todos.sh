#!/usr/bin/env bash
# Renderiza os capítulos ilustrados (cenas.html) em $TUT_HOME/rec/<tut>/<tut>-capNN.mp4, um por vez, sob a trava de
# tarefa pesada. Sem argumentos: todos os capítulos com narração processada (<tutorial>/narracao/capNN.json).
# uso: bash render_todos.sh [NN ...]        (ex.: bash render_todos.sh 05 00)
set -euo pipefail
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; TUT="$(cd "$H/../.." && pwd)"; DOMI="$(dirname "$TUT")"; N="$(basename "$TUT")"
[ -d "$H/node_modules/lucide-static" ] || (cd "$H" && npm install --no-audit --no-fund >/dev/null 2>&1)
mkdir -p "$DOMI/rec/$N"
CAPS=("$@"); [ ${#CAPS[@]} -gt 0 ] || CAPS=($(ls "$TUT/narracao" | sed -n 's/^cap\([0-9][0-9]\)\.json$/\1/p'))
for c in "${CAPS[@]}"; do
  nice -n 5 flock "$DOMI/.heavy.lock" node "$H/render_cenas.cjs" "$((10#$c))" "$TUT/narracao/cap$c.json" "$DOMI/rec/$N/$N-cap$c.mp4" --cauda "${CAUDA:-1.2}"
done
