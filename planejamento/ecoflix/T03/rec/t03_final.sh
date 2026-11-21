#!/bin/bash
# T03 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 03). Qualidade padrão do record.mjs.
# Uso: source rec/t03/t03_env.sh; bash rec/t03/t03_final.sh 00 01 01b ...   Saída: rec/t03/capNN.resumo e rec/t03/final.log
# Molde: rec/t02/t02_final.sh. Mundo próprio (rec/t03/_mundo, porta 54303); a instância é religada a cada tentativa.
set -u
cd /home/claude/ecoflix
: "${TUT_USER:?source rec/t03/t03_env.sh}" "${TUT_SENHA:?source rec/t03/t03_env.sh}"
export FAKE_URL=http://127.0.0.1:54303 FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_MUNDO=/home/claude/ecoflix/rec/t03/_mundo FAKE_PORT=54303
for C in "$@"; do
  case "$C" in *b) NN="$(printf '%02d' "$((10#${C%b}))")b";; *) NN=$(printf '%02d' "$((10#$C))");; esac; export NN
  bash rec/fila.sh --prio 03 -- bash -c '
    for vez in 1 2; do
      bash rec/run.sh fake | tail -1
      timeout 900 node rec/record.mjs rec/t03/cap$NN.json > rec/t03/.cap$NN.out 2>&1
      python3 -I rec/t03/resumo.py $NN > rec/t03/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t03/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t03/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t03/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t03/cap$NN.resumo)" >> rec/t03/final.log
done
bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t03/final.log
