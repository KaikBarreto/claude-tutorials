#!/bin/bash
# T27 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 27). Qualidade padrão do record.mjs.
# Uso: bash rec/t27/t27_final.sh 00 01 02 ...   Saída: rec/t27/t27-capNN.{mp4,actions.json,telemetry.json}, rec/t27/capNN.resumo, rec/t27/final.log
# Molde: rec/t26/t26_final.sh. Instância 54327 religada a cada tentativa (FAKE_NOW fixo 2026-11-10T08:30:00-03:00), até 2 tentativas,
# aceita maxLate < 0,8 e 0 falho. DISCO: grava em /dev/shm/t27_rec; só mp4, actions, telemetria e folha voltam para rec/t27/.
# Para (saída 4) se / < 1000 MB ou /dev/shm < 1,5 GB. Sementes (inicio, apos-cap03, apos-cap04) vêm do cap.json.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54327 TUT_USER=rafael@reciclavalemetais.example FAKE_NOW=2026-11-10T08:30:00-03:00
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
mkdir -p /dev/shm/t27_rec
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  python3 -I rec/t27/gerar.py > /dev/null
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 1000 ] || [ "$SHM" -lt 1500 ]; then echo "cap$NN PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t27/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t27/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$NN")
  export TMO
  bash rec/fila.sh --prio 27 -- bash -c '
    for vez in 1 2; do
      ( for i in 3 4 5 6 7 8 9 10; do eval "exec $i>&-"; done; FAKE_PORT=54327 bash rec/run.sh fake | tail -1 )
      for e in actions.json telemetry.json mp4 contact.jpg; do rm -f "/dev/shm/t27_rec/t27-cap$NN.$e"; done
      timeout $TMO node rec/record.mjs rec/t27/cap$NN.json --out /dev/shm/t27_rec > rec/t27/.cap$NN.out 2>&1
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t27_rec/t27-cap$NN.$e rec/t27/ 2>/dev/null; done
      python3 -I rec/t27/resumo.py $NN > rec/t27/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t27/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t27/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t27/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t27/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t27/final.log
done
FAKE_PORT=54327 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t27/final.log
