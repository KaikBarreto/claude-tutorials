#!/bin/bash
# T15 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 15). Qualidade padrão do record.mjs.
# Uso: bash rec/t15/t15_final.sh 00 01 02 ...   Saída: rec/t15/t15-capNN.{mp4,actions.json,telemetry.json}, rec/t15/capNN.resumo, rec/t15/final.log
# Molde: rec/t05/t05_final.sh. Instância 54315 religada a cada tentativa (FAKE_NOW do capítulo), até 2 tentativas, aceita maxLate < 0,8 e 0 falho.
# DISCO: grava em /dev/shm/t15_rec; só mp4, actions, telemetria e folha voltam para rec/t15/. Para (saída 4) se / < 600 MB ou /dev/shm < 1,2 GB.
# Os capítulos 01, 02 e 10 regravam a semente apos-capNN depois de gravar (t15_sementes.py; o 13 do roteiro usa a semente apos-cap10).
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54315 TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
mkdir -p /dev/shm/t15_rec
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  export FAKE_NOW=$(python3 -I -c "import json,sys;print(json.load(open('rec/t15/fake_now.json'))[sys.argv[1]])" "$NN")
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 600 ] || [ "$SHM" -lt 1200 ]; then echo "cap$NN PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t15/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t15/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$NN")
  export TMO
  SEM=""; case "$NN" in 01|02) SEM="python3 -I rec/t15/t15_sementes.py $NN";; 13) SEM="python3 -I rec/t15/t15_sementes.py 10";; esac; export SEM
  bash rec/fila.sh --prio 15 -- bash -c '
    for vez in 1 2; do
      FAKE_PORT=54315 bash rec/run.sh fake | tail -1
      for e in actions.json telemetry.json mp4 contact.jpg; do rm -f "/dev/shm/t15_rec/t15-cap$NN.$e"; done
      timeout $TMO node rec/record.mjs rec/t15/cap$NN.json --out /dev/shm/t15_rec > rec/t15/.cap$NN.out 2>&1
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t15_rec/t15-cap$NN.$e rec/t15/ 2>/dev/null; done
      python3 -I rec/t15/resumo.py $NN > rec/t15/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t15/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done
    if ! grep -q "FALHOU no passo" rec/t15/.cap$NN.out && [ -n "$SEM" ]; then $SEM >> rec/t15/.cap$NN.out 2>&1; fi'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t15/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t15/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t15/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t15/final.log
done
FAKE_PORT=54315 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t15/final.log
