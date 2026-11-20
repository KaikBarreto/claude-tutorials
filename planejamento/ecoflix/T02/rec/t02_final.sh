#!/bin/bash
# T02 · gravação FINAL (com a voz) de uma lista de capítulos, um por vez, pela fila. Qualidade padrão do record.mjs.
# Uso: bash rec/t02/t02_final.sh 00 01 ...   Saída: rec/t02/capNN.resumo e rec/t02/final.log
# Molde: rec/t08/t08_final.sh. Na T02 o FAKE_NOW é um só para todos os capítulos; a instância (54302) é religada a cada tentativa.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54302 TUT_USER=rafael@reciclavalemetais.example FAKE_NOW=2026-11-10T08:30:00-03:00
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  bash rec/fila.sh --prio 02 -- bash -c '
    for vez in 1 2; do
      FAKE_PORT=54302 bash rec/run.sh fake | tail -1
      node rec/record.mjs rec/t02/cap$NN.json > rec/t02/.cap$NN.out 2>&1
      python3 -I rec/t02/resumo.py $NN > rec/t02/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t02/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t02/cap$NN.resumo)" >> rec/t02/final.log
done
FAKE_PORT=54302 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t02/final.log
