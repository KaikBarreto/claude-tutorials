#!/bin/bash
# T19 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 19). Qualidade padrão do record.mjs.
# Uso: bash rec/t19/t19_final.sh 00 01 02 ...   Saída: rec/t19/t19-capNN.{mp4,actions.json,telemetry.json}, rec/t19/capNN.resumo, rec/t19/final.log
# Molde: rec/t15/t15_final.sh. Instância 54319 religada a cada tentativa (FAKE_NOW do capítulo), até 2 tentativas, aceita maxLate < 0,8 e 0 falho.
# DISCO: grava em /dev/shm/t19_rec; só mp4, actions, telemetria e folha voltam para rec/t19/. Para (saída 4) se / < 1000 MB ou /dev/shm < 1500 MB.
# Capítulos 02 a 16 regravam a semente apos-capNN depois de gravar (cadeia: o capítulo seguinte parte dela). Tablet (13): 1024x768.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54319 TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
mkdir -p /dev/shm/t19_rec
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  python3 -I rec/t19/gerar.py "$NN" > /dev/null
  export FAKE_NOW=$(python3 -I -c "import json,sys;print(json.load(open('rec/t19/fake_now.json'))[sys.argv[1]])" "$NN")
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 1000 ] || [ "$SHM" -lt 1500 ]; then echo "cap$NN PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t19/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t19/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$NN")
  export TMO
  unset TUT_VIEWPORT TUT_SCALE
  [ "$((10#$NN))" -eq 13 ] && export TUT_VIEWPORT=1024x768
  { [ "$((10#$NN))" -eq 12 ] || [ "$((10#$NN))" -eq 13 ]; } && export TUT_SCALE=2
  SEED=0; [ "$((10#$NN))" -ge 2 ] && [ "$((10#$NN))" -le 16 ] && SEED=1; export SEED
  bash rec/fila.sh --prio 19 -- bash -c '
    rm -f rec/t19/.cap$NN.rc
    for vez in 1 2; do
      FAKE_PORT=54319 bash rec/run.sh fake | tail -1
      for e in actions.json telemetry.json mp4 contact.jpg; do rm -f "/dev/shm/t19_rec/t19-cap$NN.$e"; done
      timeout $TMO node rec/record.mjs rec/t19/cap$NN.json --out /dev/shm/t19_rec > rec/t19/.cap$NN.out 2>&1; echo $? > rec/t19/.cap$NN.rc
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t19_rec/t19-cap$NN.$e rec/t19/ 2>/dev/null; done
      python3 -I rec/t19/resumo.py $NN > rec/t19/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t19/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done
    if [ "$SEED" = 1 ] && [ "$(cat rec/t19/.cap$NN.rc)" = 0 ]; then node rec/t19/t19_semente.mjs apos-cap$NN >> rec/t19/.cap$NN.out 2>&1; fi'
  echo "cap$NN $(date +%H:%M:%S) rc $(cat rec/t19/.cap$NN.rc 2>/dev/null) $(head -1 rec/t19/cap$NN.resumo) | SEM ALVO $(grep -v SEMENTE rec/t19/.cap$NN.out | grep -c 'SEM ALVO') DIFERENTE $(grep -c DIFERENTE rec/t19/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t19/final.log
done
FAKE_PORT=54319 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t19/final.log
