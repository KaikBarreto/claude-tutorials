#!/bin/bash
# T21 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 21). Qualidade padrão do record.mjs.
# Uso: bash rec/t21/t21_final.sh 00 01 02 02b ...   Saída: rec/t21/t21-capNN.{mp4,actions.json,telemetry.json}, rec/t21/capNN.resumo, rec/t21/final.log
# Molde: rec/t18/t18_final.sh + rec/t21/t21_corpo.sh. Instância 54321 religada a cada tentativa (mundo da T21 refeito; o overlay guarda estado em
# memória), FAKE_NOW fixo; até 2 tentativas, aceita maxLate < 0,8 e 0 falho. A senha só existe no ambiente.
# DISCO: grava em /dev/shm/t21_rec; só mp4, actions, telemetria e folha voltam para rec/t21/. Para (saída 4) se / < 1000 MB ou /dev/shm < 1,5 GB.
set -u
cd /home/claude/ecoflix
PORT=54321; FN=2026-11-10T08:30:00-03:00
export FAKE_URL=http://127.0.0.1:$PORT TUT_USER=rafael@reciclavalemetais.example FAKE_NOW=$FN FAKE_MUNDO=/dev/shm/t21_mundo
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
mkdir -p /dev/shm/t21_rec
for C in "$@"; do
  SUF=""; RAW=$C; case "$RAW" in *b) SUF=b; RAW=${RAW%b};; esac
  NN=$(printf '%02d' "$((10#$RAW))"); export NN SUF; NOME="cap$NN$SUF"; export NOME
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 1000 ] || [ "$SHM" -lt 1500 ]; then echo "$NOME PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t21/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t21/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$NN"); export TMO
  bash rec/fila.sh --prio 21 -- bash -c '
    for vez in 1 2; do
      python3 -I rec/t21/t21_mundo.py > /dev/null
      ( for i in 3 4 5 6 7 8 9 10; do eval "exec $i>&-"; done; FAKE_MUNDO=$FAKE_MUNDO FAKE_NOW=$FAKE_NOW FAKE_PORT=54321 bash rec/run.sh fake | tail -1 )
      for e in actions.json telemetry.json mp4 contact.jpg; do rm -f "/dev/shm/t21_rec/t21-$NOME.$e"; done
      timeout $TMO node rec/record.mjs rec/t21/$NOME.json --out /dev/shm/t21_rec > rec/t21/.$NOME.out 2>&1
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t21_rec/t21-$NOME.$e rec/t21/ 2>/dev/null; done
      rm -rf /dev/shm/t21_rec/t21-$NOME* 2>/dev/null
      python3 -I rec/t21/resumo.py $NN$SUF > rec/t21/$NOME.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t21/$NOME.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "$NOME $(date +%H:%M:%S) $(head -1 rec/t21/$NOME.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t21/.$NOME.out) DIFERENTE $(grep -c DIFERENTE rec/t21/$NOME.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t21/final.log
done
FAKE_MUNDO=/dev/shm/t21_mundo FAKE_PORT=54321 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t21/final.log
