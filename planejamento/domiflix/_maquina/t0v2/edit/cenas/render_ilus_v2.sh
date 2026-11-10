#!/usr/bin/env bash
# Renderiza o trecho de uma ilustração do T0 v2 (cena N, capítulo C, de DE a ATE s do capítulo) nas duas proporções.
# uso: render_ilus_v2.sh <cena> <cap> <de> <ate>     saída: $TUT_HOME/rec/t0v2/ilus/cenaNN_16x9.mp4 e cenaNN_9x16.mp4
set -euo pipefail
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; DOMI="$(cd "$H/../../.." && pwd)"
C="$1"; K="$2"; DE="$3"; ATE="$4"; N="$(printf %02d "$C")"; J="$DOMI/t0v2/narracao/cap$(printf %02d "$K").json"; O="$DOMI/rec/t0v2/ilus"; mkdir -p "$O"
nice -n 10 flock "$DOMI/.heavy.lock" node "$H/render_cena_v2.cjs" "$C" "$J" "$O/cena${N}_16x9.mp4" --de "$DE" --ate "$ATE" --html "$H/cenas_v2.html"
nice -n 10 flock "$DOMI/.heavy.lock" node "$H/render_cenas_vertical.cjs" "$C" "$J" "$O/cena${N}_9x16.mp4" --de "$DE" --ate "$ATE" --html "$H/cenas_v2_vertical.html"
