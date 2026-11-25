#!/bin/bash
# T10 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 10). Molde: rec/t09/t09_final.sh.
# Uso: bash rec/t10/t10_final.sh 00 01 ...   (VEZES=1 para uma tentativa só; padrão 2)
# Quadros em /dev/shm/t10_rec; depois move mp4, actions, telemetria e folha para rec/t10/. Saída: capNN.resumo e final.log.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54310 FAKE_PORT=54310 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-2}
export FAKE_NOW=2026-11-10T08:30:00-03:00
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)Aa1"
for C in "$@"; do
  NN="$(printf '%02d' "$((10#$C))")"; export NN
  L=$(df -m / | awk 'NR==2{print $4}'); [ "$L" -ge 600 ] || { echo "DISCO BAIXO ($L MB) antes do cap$NN" >> rec/t10/final.log; break; }
  bash rec/fila.sh --prio 10 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      mkdir -p /dev/shm/t10_rec; rm -f rec/t10/t10-cap$NN.actions.json /dev/shm/t10_rec/t10-cap$NN.*
      timeout 1500 node rec/record.mjs rec/t10/cap$NN.json --out /dev/shm/t10_rec > rec/t10/.cap$NN.out 2>&1
      for e in mp4 actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t10_rec/t10-cap$NN.$e ] && mv /dev/shm/t10_rec/t10-cap$NN.$e rec/t10/; done
      python3 -I rec/t10/resumo.py $NN --tudo > rec/t10/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t10/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t10/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t10/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t10/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t10/final.log
  case "$NN" in 07|13) python3 -I rec/t10/t10_pdfs.py > rec/t10/.pdfs-$NN.txt 2>&1 ;; esac
done
FAKE_PORT=54310 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t10/final.log
