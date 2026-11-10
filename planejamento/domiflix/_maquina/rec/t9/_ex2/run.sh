#!/usr/bin/env bash
# uso: run.sh NOME  (roda rec/t9/_ex2/NOME.json sob a trava, fotos em _ex2/o_NOME)
cd /home/claude/domiflix
export FAKE_URL=http://127.0.0.1:54326 FAKE_NOW="2026-11-03T09:00:00-03:00" APP_ORIGIN=https://www.dominex.app TUT_HOME=/home/claude/domiflix
flock $TUT_HOME/.heavy.lock nice -n 10 node rec/t9/explorar.mjs rec/t9/_ex2/$1.json --out rec/t9/_ex2/o_$1 > rec/t9/_ex2/$1.log 2>&1
