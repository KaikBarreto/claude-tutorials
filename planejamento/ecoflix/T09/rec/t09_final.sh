#!/bin/bash
# T09 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 9). Molde: rec/t04/t04_final.sh.
# Uso: bash rec/t09/t09_final.sh 00 01 ...   (VEZES=1 para uma tentativa só; padrão 2)
# Quadros em /dev/shm/t09_rec; depois move mp4, actions, telemetria e folha para rec/t09/. Saída: capNN.resumo e final.log.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54309 FAKE_PORT=54309 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-2}
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
for C in "$@"; do
  NN="$(printf '%02d' "$((10#$C))")"; export NN
  export FAKE_NOW=$(python3 -I -c "import json,sys;print(json.load(open('rec/t09/fake_now.json'))[sys.argv[1]])" "$NN")
  L=$(df -m / | awk 'NR==2{print $4}'); [ "$L" -ge 600 ] || { echo "DISCO BAIXO ($L MB) antes do cap$NN" >> rec/t09/final.log; break; }
  bash rec/fila.sh --prio 9 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      mkdir -p /dev/shm/t09_rec; rm -f rec/t09/t09-cap$NN.actions.json /dev/shm/t09_rec/t09-cap$NN.*
      timeout 1500 node rec/record.mjs rec/t09/cap$NN.json --out /dev/shm/t09_rec > rec/t09/.cap$NN.out 2>&1
      for e in mp4 actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t09_rec/t09-cap$NN.$e ] && mv /dev/shm/t09_rec/t09-cap$NN.$e rec/t09/; done
      python3 -I rec/t09/resumo.py $NN --tudo > rec/t09/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t09/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  python3 -I rec/t09/t09_pdfs.py $NN > rec/t09/.pdfs-$NN.txt 2>&1
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t09/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t09/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t09/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t09/final.log
done
FAKE_PORT=54309 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t09/final.log
