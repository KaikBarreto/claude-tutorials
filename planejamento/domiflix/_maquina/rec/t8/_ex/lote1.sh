#!/usr/bin/env bash
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54325 FAKE_NOW=2026-11-03T09:00:00-03:00
flock $TUT_HOME/.heavy.lock nice -n 10 node rec/t8/explorar.mjs rec/t8/_ex/i.json --out rec/t8/_ex/out > rec/t8/_ex/i.log 2>&1
for n in "$@"; do
  bash rec/t8/rodar.sh $n --rapido --seed > rec/t8/_ex/lote-$n.txt 2>&1
done
echo fim > rec/t8/_ex/lote1.done
