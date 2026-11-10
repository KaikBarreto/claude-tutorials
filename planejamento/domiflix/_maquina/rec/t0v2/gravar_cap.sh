#!/usr/bin/env bash
# Grava um capítulo cronometrado (ex.: gravar_cap.sh cap01-d). Saída: rec/t0v2/t0v2-capNN[-p].*  Uma trava por gravação.
cd "$(dirname "$0")/../.." || exit 1
export FAKE_NOW=2026-11-03T09:00:00-03:00 FAKE_URL=http://127.0.0.1:54328 APP_ORIGIN=https://www.dominex.app
for n in "$@"; do
  nome=$(python3 -c "import json,sys;print(json.load(open('rec/t0v2/$n.json'))['name'])")
  flock .heavy.lock nice -n 10 node rec/record.mjs "rec/t0v2/$n.json" --out rec/t0v2 --name "$nome" > "rec/t0v2/$nome.log" 2>&1; echo "$n exit $?"
done
