#!/bin/bash
# T05 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prioridade 05). Qualidade padrão do record.mjs.
# Uso: bash rec/t05/t05_final.sh 00 01 02 02w ...      Saída: rec/t05/t05-capNN.{mp4,actions.json,telemetry.json}, rec/t05/capNN.resumo, rec/t05/final.log
# Cada capítulo: instância 54305 religada no FAKE_NOW dele, até 2 tentativas, aceita maxLate < 0,8 e 0 falho.
# DISCO: o record.mjs grava em /dev/shm/t05_rec (os quadros enchem o disco); só mp4, actions, telemetria e folha voltam para rec/t05/.
# Para sozinho (saída 4) se / cair abaixo de 800 MB ou /dev/shm abaixo de 1,2 GB.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54305 TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
mkdir -p /dev/shm/t05_rec
for C in "$@"; do
  K=${C:0:2}; NN=$(printf '%02d' "$((10#$K))")${C:2}; export NN
  export FAKE_NOW=$(python3 -I -c "import json,sys;print(json.load(open('rec/t05/fake_now.json'))[sys.argv[1]])" "$K")
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 800 ] || [ "$SHM" -lt 1200 ]; then echo "cap$NN PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t05/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t05/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$K")
  export TMO
  bash rec/fila.sh --prio 05 -- bash -c '
    for vez in 1 2; do
      FAKE_PORT=54305 bash rec/run.sh fake | tail -1
      timeout $TMO node rec/record.mjs rec/t05/cap$NN.json --out /dev/shm/t05_rec > rec/t05/.cap$NN.out 2>&1
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t05_rec/t05-cap$NN.$e rec/t05/ 2>/dev/null; done
      python3 -I rec/t05/resumo.py $NN > rec/t05/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t05/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t05/cap$NN.resumo)" >> rec/t05/final.log
done
FAKE_PORT=54305 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t05/final.log
