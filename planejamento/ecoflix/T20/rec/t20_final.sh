#!/bin/bash
# T20 · gravação FINAL (com a voz real 1.60.22) dos capítulos 00..14, um por vez, pela fila (prio 20). Molde: rec/t15/t15_final.sh.
# Uso: bash rec/t20/t20_final.sh 00 01 ...   Saída: rec/t20/t20-capNN.{mp4,actions.json,telemetry.json,contact.jpg}, rec/t20/capNN.resumo, rec/t20/final.log
# As senhas (PORTAL_SENHA, TUT_SENHA) são sorteadas AQUI e só vivem neste processo: as sementes são regravadas com a PORTAL_SENHA
# desta rodada (só o hash vai para a semente) e o robô digita a mesma. Instância 54320 religada a cada tentativa (FAKE_NOW 10/11/2026 15:00).
# DISCO: grava em /dev/shm/t20_rec; só mp4, actions, telemetria e folha voltam para rec/t20/. Para (saída 4) se / < 700 MB ou /dev/shm < 1,5 GB.
set -u
cd /home/claude/ecoflix
export PORTAL_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
export FAKE_URL=http://127.0.0.1:54320 TUT_USER=rafael@reciclavalemetais.example
export FN=2026-11-10T15:00:00-03:00 FAKE_NOW=2026-11-10T15:00:00-03:00
python3 -I rec/t20/t20_sementes.py > /dev/null 2>&1 || { echo "sementes FALHOU" >> rec/t20/final.log; exit 5; }
mkdir -p /dev/shm/t20_rec
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 700 ] || [ "$SHM" -lt 1500 ]; then echo "cap$NN PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t20/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t20/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$NN")
  export TMO
  bash rec/fila.sh --prio 20 -- bash -c '
    for vez in 1 2; do
      FAKE_NOW=$FN FAKE_PORT=54320 bash rec/run.sh fake 9>&- | tail -1
      for e in actions.json telemetry.json mp4 contact.jpg; do rm -f "/dev/shm/t20_rec/t20-cap$NN.$e"; done
      timeout $TMO node rec/record.mjs rec/t20/cap$NN.json --out /dev/shm/t20_rec > rec/t20/.cap$NN.out 2>&1
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t20_rec/t20-cap$NN.$e rec/t20/ 2>/dev/null; done
      python3 -I rec/t20/resumo.py $NN > rec/t20/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t20/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t20/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t20/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t20/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t20/final.log
done
FAKE_PORT=54320 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t20/final.log
