#!/bin/bash
# T22 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 22). Qualidade padrão do record.mjs.
# Uso: bash rec/t22/t22_final.sh 00 01 02 ...   Saída: rec/t22/t22-capNN.{mp4,actions.json,telemetry.json}, rec/t22/capNN.resumo, rec/t22/final.log
# Molde: rec/t05/t05_final.sh. Instância 54322 religada a cada tentativa (FAKE_NOW do capítulo), até 2 tentativas, aceita maxLate < 0,8 e 0 falho.
# DISCO: grava em /dev/shm/t22_rec; só mp4, actions, telemetria e folha voltam para rec/t22/. Para (saída 4) se / < 1000 MB ou /dev/shm < 1,5 GB.
# Sementes: arquivos fixos em rec/mundo/seeds-extra/t22/ (nada a regravar). FAKE_NOW 2026-11-10T08:30:00-03:00 em todos.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54322 TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
mkdir -p /dev/shm/t22_rec
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  export FAKE_NOW=2026-11-10T08:30:00-03:00
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 1000 ] || [ "$SHM" -lt 1500 ]; then echo "cap$NN PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t22/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t22/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$NN")
  export TMO
  SEM=""; export SEM
  bash rec/fila.sh --prio 22 -- bash -c '
    for vez in 1 2; do
      FAKE_PORT=54322 bash rec/run.sh fake | tail -1
      for e in actions.json telemetry.json mp4 contact.jpg; do rm -f "/dev/shm/t22_rec/t22-cap$NN.$e"; done
      timeout $TMO node rec/record.mjs rec/t22/cap$NN.json --out /dev/shm/t22_rec > rec/t22/.cap$NN.out 2>&1
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t22_rec/t22-cap$NN.$e rec/t22/ 2>/dev/null; done
      python3 -I rec/t22/resumo.py $NN > rec/t22/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t22/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done
    if ! grep -q "FALHOU no passo" rec/t22/.cap$NN.out && [ -n "$SEM" ]; then $SEM >> rec/t22/.cap$NN.out 2>&1; fi'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t22/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t22/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t22/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t22/final.log
done
FAKE_PORT=54322 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t22/final.log
