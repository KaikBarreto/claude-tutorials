#!/usr/bin/env bash
# uso: run2.sh NOME [NN]  roda NOME.json sob a trava; com NN, grava o estado como seeds-extra/t9/apos-capNN (snap diff) NA MESMA trava
cd /home/claude/domiflix
export FAKE_URL=http://127.0.0.1:54326 FAKE_NOW="2026-11-03T09:00:00-03:00" APP_ORIGIN=https://www.dominex.app TUT_HOME=/home/claude/domiflix
CMD="node rec/t9/explorar.mjs rec/t9/_ex2/$1.json --out rec/t9/_ex2/o_$1 > rec/t9/_ex2/$1.log 2>&1"
if [ -n "${2:-}" ]; then CMD="node rec/t9/snap.mjs base > rec/t9/_ex2/snapbase.log 2>&1; $CMD; node rec/t9/snap.mjs diff $2 > rec/t9/_ex2/snap$2.log 2>&1"; fi
flock $TUT_HOME/.heavy.lock nice -n 10 bash -c "$CMD"
