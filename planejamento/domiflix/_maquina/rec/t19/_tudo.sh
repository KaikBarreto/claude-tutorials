#!/usr/bin/env bash
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54333 FAKE_NOW=2026-11-10T10:00:00-03:00
until [ -f rec/t19/_ex/eD.done ]; do sleep 5; done
FAKE_PORT=54333 rec/run.sh fake > /dev/null 2>&1
node rec/t19/snap.mjs base
rec/t19/lote.sh 0 1 2 3 4 5 6 7 8 9 10 11 12 13
echo TUDO_FIM > rec/t19/_debug/tudo.fim
