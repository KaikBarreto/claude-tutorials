#!/bin/bash
# T05 · UM trabalho do robô por vez, DENTRO da trava pesada (corpo: rode pela fila, via t05_lote.sh). Instância 54305, FAKE_NOW do capítulo (fake_now.json; o cap04 tem o relógio do cupom).
# Uso: bash rec/t05/t05_corpo.sh NN r     ensaio rápido do capítulo NN (ensaio.py + --rapido, MP4 ultrafast)
#      bash rec/t05/t05_corpo.sh NN c     ensaio completo (com os `at`, voz estimada)
# DISCO: tudo o que o record.mjs escreve (quadros JPEG, MP4) vai para /dev/shm/t05_ens (--out); só mp4, actions.json, telemetry.json e contact.jpg voltam para rec/t05/_ens.
# Abaixo de 450 MB livres em / o trabalho não começa (saída 4). Precisa de TUT_SENHA no ambiente? Não: gera uma aleatória (mundo falso).
set -u
cd /home/claude/ecoflix
PORT=54305
NN=$(printf '%02d' "$((10#$1))"); MODO=$2
FN=$(python3 -I -c "import json,sys;print(json.load(open('rec/t05/fake_now.json'))[sys.argv[1]])" "$NN")
LIVRE=$(df -m / | awk 'NR==2{print $4}')
echo "$NN:$MODO começou $(date +%H:%M:%S) livre=${LIVRE}MB FAKE_NOW=$FN"
[ "$LIVRE" -lt 450 ] && { echo "DISCO ABAIXO DE 450 MB ($LIVRE): parado"; exit 4; }
PIDF=rec/.runtime/fake$PORT.pid
PID=$(cat "$PIDF" 2>/dev/null || true)
if [ -z "$PID" ] || ! tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -qx "FAKE_PORT=$PORT" || ! tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_NOW=$FN" \
   || [ -n "$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib rec/mundo/seeds-extra/t05 -name '*.mjs' -o -name '*.json' -newer "$PIDF" 2>/dev/null | head -1)" ]; then
  ( for i in 3 4 5 6 7 8 9 10; do eval "exec $i>&-"; done; FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake | tail -1 )
fi
PID=$(cat "$PIDF")
tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_PORT=$PORT" || { echo "instância $PORT não é a minha"; exit 3; }
export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14); export TUT_SENHA
mkdir -p /dev/shm/t05_ens rec/t05/_ens
SUF=""; [ "$MODO" = p ] && SUF=p   # p = sonda: grava rec/t05/_ens/capNNp.json (montado à mão) e só guarda actions/telemetry
if [ "$MODO" = p ]; then
  ROT=rec/t05/_ens/cap${NN}p.json; DIR=rec/t05/_ens; EXTRA="--rapido --preset ultrafast --crf 30"; RES=--ens
  [ -f "$ROT" ] || exit 2
elif [ "$MODO" = r ]; then
  python3 -I rec/t05/ensaio.py "$NN" > /dev/null || exit 2
  ROT=rec/t05/_ens/cap$NN.json; DIR=rec/t05/_ens; EXTRA="--rapido --preset ultrafast --crf 30"; RES=--ens
else
  ROT=rec/t05/cap$NN.json; DIR=rec/t05/_ens; EXTRA="--preset ultrafast --crf 30"; RES=--ens
fi
TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t05/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+240))" "$NN")
OUT="$DIR/.t05-cap$NN$SUF.out"
timeout $TMO node rec/record.mjs "$ROT" --out /dev/shm/t05_ens $EXTRA > "$OUT" 2>&1; RC=$?
for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t05_ens/t05-cap$NN$SUF.$e "$DIR/" 2>/dev/null; done
FALHOS=$(python3 -I -c "import json;a=json.load(open('$DIR/t05-cap$NN$SUF.actions.json'))['actions'];print(sum(1 for x in a if x.get('error') or x.get('ok') is False))" 2>/dev/null || echo x)
python3 -I rec/t05/resumo.py "$NN$SUF" $RES > "$DIR/t05-cap$NN$SUF.resumo.txt" 2>&1
[ "$MODO" = r ] && python3 -I rec/t05/prever.py "$NN" --ens > "$DIR/t05-cap$NN.prever.txt" 2>&1
echo "fim $NN:$MODO $(date +%H:%M:%S) rc=$RC falhos=$FALHOS livre=$(df -m / | awk 'NR==2{print $4}')MB SEM-ALVO=$(grep -c 'SEM ALVO' "$OUT")"
tail -2 "$OUT"; head -3 "$DIR/t05-cap$NN.resumo.txt"
exit $RC
