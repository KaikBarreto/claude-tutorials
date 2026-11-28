#!/bin/bash
# T26 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 26). Qualidade padrão do record.mjs.
# Uso: bash rec/t26/t26_final.sh 00 01 02 ...   Saída: rec/t26/t26-capNN.{mp4,actions.json,telemetry.json}, rec/t26/capNN.resumo, rec/t26/final.log
# Molde: rec/t22/t22_final.sh. Instância 54326 religada a cada tentativa com o FAKE_NOW do capítulo (rec/t26/fake_now.json), até 2 tentativas,
# aceita maxLate < 0,8 e 0 falho. DISCO: grava em /dev/shm/t26_rec; só mp4, actions, telemetria e folha voltam para rec/t26/.
# Para (saída 4) se / < 1000 MB ou /dev/shm < 1,5 GB. Sementes: arquivos fixos em rec/mundo/seeds-extra/t26/.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54326 TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
mkdir -p /dev/shm/t26_rec
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  FAKE_NOW=$(python3 -I -c "import json,sys;print(json.load(open('rec/t26/fake_now.json'))[sys.argv[1]])" "$NN") || exit 2
  export FAKE_NOW
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 1000 ] || [ "$SHM" -lt 1500 ]; then echo "cap$NN PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> rec/t26/final.log; exit 4; fi
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t26/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+300))" "$NN")
  export TMO
  bash rec/fila.sh --prio 26 -- bash -c '
    for vez in 1 2; do
      ( for i in 3 4 5 6 7 8 9 10; do eval "exec $i>&-"; done; FAKE_PORT=54326 bash rec/run.sh fake | tail -1 )
      for e in actions.json telemetry.json mp4 contact.jpg; do rm -f "/dev/shm/t26_rec/t26-cap$NN.$e"; done
      timeout $TMO node rec/record.mjs rec/t26/cap$NN.json --out /dev/shm/t26_rec > rec/t26/.cap$NN.out 2>&1
      for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t26_rec/t26-cap$NN.$e rec/t26/ 2>/dev/null; done
      python3 -I rec/t26/resumo.py $NN > rec/t26/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t26/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t26/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t26/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t26/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t26/final.log
done
FAKE_PORT=54326 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t26/final.log
