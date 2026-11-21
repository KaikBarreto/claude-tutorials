#!/bin/bash
# T25 · UM trabalho do robô por vez, DENTRO da trava pesada (corpo: rode pela fila, via t25_lote.sh). Instância 54325, FAKE_NOW fixo.
# Uso: bash rec/t25/t25_corpo.sh NN r [sem]   ensaio rápido do capítulo NN (ensaio.py + --rapido, MP4 ultrafast apagado ao fim); `sem` captura apos-capNN
#      bash rec/t25/t25_corpo.sh NN c         ensaio completo (com os `at`, voz estimada), MP4 e folha de contato em /dev/shm/t25rec
# DISCO: os quadros JPEG do record.mjs vão para /dev/shm/t25_ens (--out); só actions.json e telemetry.json voltam para rec/t25/_ens (ou rec/t25).
# Abaixo de 450 MB livres em / o trabalho não começa (saída 4).
set -u
cd /home/claude/ecoflix
PORT=54325
FN=2026-11-10T08:30:00-03:00
NN=$(printf '%02d' "$((10#$1))"); MODO=$2; SEM=${3:-}
LIVRE=$(df -m / | awk 'NR==2{print $4}')
echo "$NN:$MODO começou $(date +%H:%M:%S) livre=${LIVRE}MB"
[ "$LIVRE" -lt 450 ] && { echo "DISCO ABAIXO DE 450 MB ($LIVRE): parado"; exit 4; }
PIDF=rec/.runtime/fake$PORT.pid
PID=$(cat "$PIDF" 2>/dev/null || true)
if [ -z "$PID" ] || ! tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -qx "FAKE_PORT=$PORT" || ! tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_NOW=$FN" \
   || [ -n "$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib -name '*.mjs' -newer "$PIDF" 2>/dev/null | head -1)" ]; then
  ( for i in 3 4 5 6 7 8 9 10; do eval "exec $i>&-"; done; FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake | tail -1 )
fi
PID=$(cat "$PIDF")
tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_PORT=$PORT" || { echo "instância $PORT não é a minha"; exit 3; }
export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14); export TUT_SENHA
mkdir -p /dev/shm/t25_ens /dev/shm/t25rec rec/t25/_ens
if [ "$MODO" = r ]; then
  python3 -I rec/t25/ensaio.py "$NN" > /dev/null || exit 2
  ROT=rec/t25/_ens/cap$NN.json; DIR=rec/t25/_ens; EXTRA="--rapido --preset ultrafast --crf 30"; RES=--ens
else
  ROT=rec/t25/cap$NN.json; DIR=rec/t25; EXTRA="--preset ultrafast --crf 30"; RES=""
fi
TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t25/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+240))" "$NN")
OUT="$DIR/.t25-cap$NN.out"
timeout $TMO node rec/record.mjs "$ROT" --out /dev/shm/t25_ens $EXTRA > "$OUT" 2>&1; RC=$?
for e in actions.json telemetry.json; do mv -f /dev/shm/t25_ens/t25-cap$NN.$e "$DIR/" 2>/dev/null; done
mv -f /dev/shm/t25_ens/t25-cap$NN.mp4 /dev/shm/t25_ens/t25-cap$NN.contact.jpg /dev/shm/t25rec/ 2>/dev/null
FALHOS=$(python3 -I -c "import json;a=json.load(open('$DIR/t25-cap$NN.actions.json'))['actions'];print(sum(1 for x in a if x.get('error') or x.get('ok') is False))" 2>/dev/null || echo x)
if [ "$SEM" = sem ] && [ "$FALHOS" = 0 ]; then python3 -I rec/t25/t25_sementes.py captura "$((10#$NN))" --porta $PORT 2>&1 | tail -1; fi
python3 -I rec/t25/resumo.py "$NN" $RES > "$DIR/t25-cap$NN.resumo.txt" 2>&1
[ "$MODO" = r ] && rm -f /dev/shm/t25rec/t25-cap$NN.mp4
echo "fim $NN:$MODO $(date +%H:%M:%S) rc=$RC falhos=$FALHOS livre=$(df -m / | awk 'NR==2{print $4}')MB SEM-ALVO=$(grep -c 'SEM ALVO' "$OUT")"
tail -2 "$OUT"; head -3 "$DIR/t25-cap$NN.resumo.txt"
exit $RC
