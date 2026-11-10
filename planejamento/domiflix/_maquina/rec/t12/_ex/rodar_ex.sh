#!/usr/bin/env bash
# explorações curtas, uma trava por arquivo
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54327 FAKE_NOW=2026-11-10T10:00:00-03:00 APP_ORIGIN=https://www.dominex.app
for x in "$@"; do
  flock $TUT_HOME/.heavy.lock nice -n 10 node rec/t12/explorar.mjs rec/t12/_ex/$x.json --out rec/t12/_ex/out > rec/t12/_debug/$x.log 2>&1
  echo "fim $x rc=$?" >> rec/t12/_debug/$x.log
done
