#!/usr/bin/env bash
# exploração (não grava): rec/t15/ex.sh nome  -> lê rec/t15/_ex/nome.json, saída em rec/t15/_ex/nome.log e fotos em rec/t15/_ex/o-nome/
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=${EX_URL:-http://127.0.0.1:54336} FAKE_NOW=2026-11-11T09:00:00-03:00
flock $TUT_HOME/.heavy.lock nice -n 10 node rec/t15/explorar.mjs rec/t15/_ex/$1.json --out rec/t15/_ex/o-$1 > rec/t15/_ex/$1.log 2>&1
