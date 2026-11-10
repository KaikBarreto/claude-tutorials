#!/usr/bin/env bash
# Capítulo ilustrado inteiro do T0 v2 (ex.: cap 0 = cenas 2, 3, 4): 16:9 (2560x1600 -> rec/t0v2/t0v2-capNN.mp4) e 9:16 (quadro final -> t0v2-capNN-9x16.mp4).
# uso: render_cap_ilus.sh <n do capítulo>      (CAPS[1000+n] em cenas_v2.js)
set -euo pipefail
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; DOMI="$(cd "$H/../../.." && pwd)"; N="$(printf %02d "$1")"; J="$DOMI/t0v2/narracao/cap$N.json"
nice -n 10 flock "$DOMI/.heavy.lock" node "$H/render_cenas.cjs" "$((1000+$1))" "$J" "$DOMI/rec/t0v2/t0v2-cap$N.mp4" --cauda 1.2 --html "$H/cenas_v2.html"
nice -n 10 flock "$DOMI/.heavy.lock" node "$H/render_cenas_vertical.cjs" "$((1000+$1))" "$J" "$DOMI/rec/t0v2/t0v2-cap$N-9x16.mp4" --cauda 1.2 --html "$H/cenas_v2_vertical.html"
