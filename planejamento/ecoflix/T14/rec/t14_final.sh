#!/bin/bash
# T14 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 14). Qualidade padrão do record.mjs.
# Uso: bash rec/t14/t14_final.sh 00 01 ...   (VEZES=1 por padrão: a rodada de regravação é decidida à mão)
# Quadros em /dev/shm/t14_rec; depois move mp4, actions, telemetria e folha para rec/t14/. Saída: rec/t14/capNN.resumo e rec/t14/final.log
# Molde: rec/t06/t06_final.sh. Instância 54314 religada no FAKE_NOW do capítulo.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54314 FAKE_PORT=54314 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-1}
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  export FAKE_NOW=$(python3 -I -c "import json,sys;print(json.load(open('rec/t14/fake_now.json'))[sys.argv[1]])" "$NN")
  L=$(df --output=avail -m / | tail -1); [ "$L" -lt 1000 ] && { echo "PAROU: disco $L MB" >> rec/t14/final.log; exit 9; }
  bash rec/fila.sh --prio 14 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      mkdir -p /dev/shm/t14_rec; rm -f rec/t14/t14-cap$NN.actions.json
      timeout 900 node rec/record.mjs rec/t14/cap$NN.json --out /dev/shm/t14_rec > rec/t14/.cap$NN.out 2>&1
      for e in mp4 actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t14_rec/t14-cap$NN.$e ] && mv /dev/shm/t14_rec/t14-cap$NN.$e rec/t14/; done
      python3 -I rec/t14/resumo.py $NN --tudo > rec/t14/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t14/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t14/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t14/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t14/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t14/final.log
done
bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t14/final.log
