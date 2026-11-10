#!/usr/bin/env bash
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54333 FAKE_NOW=2026-11-10T10:00:00-03:00
rec/t19/lote.sh "$@"
echo TUDO_FIM > rec/t19/_debug/tudo.fim
