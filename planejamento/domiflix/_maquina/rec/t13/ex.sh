#!/usr/bin/env bash
# exploração (não grava): rec/t13/ex.sh nome  -> lê rec/t13/_ex/nome.json, saída em rec/t13/_ex/nome.log e fotos em rec/t13/_ex/o-nome/
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=${EX_URL:-http://127.0.0.1:54332} FAKE_NOW=2026-11-10T10:00:00-03:00
flock $TUT_HOME/.heavy.lock nice -n 10 node rec/t13/explorar.mjs rec/t13/_ex/$1.json --out rec/t13/_ex/o-$1 > rec/t13/_ex/$1.log 2>&1
