#!/usr/bin/env bash
# Grava as telas pedidas (ex.: gravar.sh R01-d R01-p). Uma trava por gravação.
cd "$(dirname "$0")/../.." || exit 1
export FAKE_NOW=2026-11-03T09:00:00-03:00 FAKE_URL=http://127.0.0.1:54328 APP_ORIGIN=https://www.dominex.app
mkdir -p rec/t0v2/telas
for n in "$@"; do
  echo "== $n"
  flock .heavy.lock nice -n 10 node rec/record.mjs "rec/t0v2/$n.json" --out rec/t0v2/telas --name "$n" > "rec/t0v2/telas/$n.log" 2>&1
  echo "exit $?"; grep -E "failed|falh|lateBy|pageIssues" "rec/t0v2/telas/$n.log" | head -5
done
