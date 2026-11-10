#!/usr/bin/env bash
# Renderiza os 6 capítulos ilustrados do T0 em rec/t0/t0-capNN.mp4 (um por vez, sob a trava de tarefa pesada).
set -euo pipefail
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; DOMI="$(cd "$H/../../.." && pwd)"
for c in ${*:-5 0 1 2 3 4}; do
  nice -n 5 flock "$DOMI/.heavy.lock" node "$H/render_cenas.cjs" "$c" "$DOMI/t0/narracao/cap0$c.json" "$DOMI/rec/t0/t0-cap0$c.mp4" --cauda 1.2
done
