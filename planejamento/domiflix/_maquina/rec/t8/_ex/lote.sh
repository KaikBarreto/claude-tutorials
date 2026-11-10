#!/usr/bin/env bash
# uso: lote.sh NN... (ensaio rápido + semente de cada capítulo, um por vez, uma trava por capítulo; só segue se o anterior terminou sem passo falho)
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54325 FAKE_NOW=2026-11-03T09:00:00-03:00
for n in "$@"; do
  bash rec/t8/rodar.sh $n --rapido --seed > rec/t8/_ex/lote-$n.txt 2>&1
  if ! grep -q "falhos 0," rec/t8/_ex/lote-$n.txt; then echo "parou no $n" > rec/t8/_ex/lote.done; exit 0; fi
done
echo fim > rec/t8/_ex/lote.done
