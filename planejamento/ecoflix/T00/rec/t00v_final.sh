#!/bin/bash
# T00 vertical · gravação FINAL no celular 390x844 (capNN.9x16.json, voz real) de uma lista de capítulos, um por vez, pela fila (prio 30, depois da T15).
# Uso: bash rec/t00/t00v_final.sh 00 01 ... 40 41   (VEZES=1 para uma tentativa só; padrão 2). Porta 54300; FAKE_NOW 08:30.
# O mp4 fica em /dev/shm/t00v_rec (o disco / está apertado); actions, telemetria e folha vão para rec/t00/. Saída: capNNb.resumo e final_v.log.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54300 FAKE_PORT=54300 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-2}
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)Aa1"
mkdir -p /dev/shm/t00v_rec
node rec/t00/t00_catalogo.mjs >/dev/null 2>&1 || { echo "sementes falharam" >> rec/t00/final_v.log; exit 4; }
for C in "$@"; do
  NN="$(printf '%02d' "$((10#$C))")"; export NN
  export FAKE_NOW=2026-11-10T08:30:00-03:00
  L=$(df -m / | awk 'NR==2{print $4}'); [ "$L" -ge 820 ] || { echo "DISCO BAIXO ($L MB) antes do cap$NN" >> rec/t00/final_v.log; break; }
  S=$(df -m /dev/shm | awk 'NR==2{print $4}'); [ "$S" -ge 2100 ] || { echo "SHM BAIXO ($S MB) antes do cap$NN" >> rec/t00/final_v.log; break; }
  bash rec/fila.sh --prio 30 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      rm -f rec/t00/t00-cap${NN}b.actions.json /dev/shm/t00v_rec/t00-cap${NN}b.*
      timeout 1500 node rec/record.mjs rec/t00/cap$NN.9x16.json --out /dev/shm/t00v_rec > rec/t00/.cap${NN}b.out 2>&1
      for e in mp4; do [ -f /dev/shm/t00v_rec/t00-cap${NN}b.$e ] && echo ok >/dev/null; done
      for e in actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t00v_rec/t00-cap${NN}b.$e ] && mv /dev/shm/t00v_rec/t00-cap${NN}b.$e rec/t00/; done
      python3 -I rec/t00/resumo.py ${NN}b --tudo > rec/t00/cap${NN}b.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t00/cap${NN}b.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap${NN}b $(date +%H:%M:%S) $(head -1 rec/t00/cap${NN}b.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t00/.cap${NN}b.out) DIFERENTE $(grep -c DIFERENTE rec/t00/cap${NN}b.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t00/final_v.log
done
FAKE_PORT=54300 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t00/final_v.log
