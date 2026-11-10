#!/usr/bin/env bash
# explora na fila (trava de 1 por vez): ex.sh arquivo.json
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54324 FAKE_NOW="${FAKE_NOW:-2026-11-03T09:00:00-03:00}"
curl -s -X POST $FAKE_URL/__dev/unknowns/clear >/dev/null
flock $TUT_HOME/.heavy.lock nice -n 10 node rec/t5/explorar.mjs "$1" --out "$(dirname "$1")/out" > "${1%.json}.log" 2>&1
curl -s $FAKE_URL/__dev/unknowns > "${1%.json}.unk.json"
