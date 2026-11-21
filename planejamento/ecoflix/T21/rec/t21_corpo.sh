#!/bin/bash
# T21 · UM trabalho do robô por vez, DENTRO da trava pesada (corpo: rode pela fila, via t21_lote.sh). Instância 54321 com o mundo da T21
# (FAKE_MUNDO=/dev/shm/t21_mundo, montado por t21_mundo.py), FAKE_NOW fixo.
# Uso: bash rec/t21/t21_corpo.sh NN r      ensaio rápido do capítulo NN (ensaio.py + --rapido; NN pode ser 02b ou 15b: o corte do Marcos)
#      bash rec/t21/t21_corpo.sh NN c      ensaio completo (com os `at`, voz estimada)
# DISCO: os quadros JPEG do record.mjs (um capítulo chega a 345 MB) vão SEMPRE para /dev/shm/t21_ens (--out); só mp4, actions.json,
# telemetry.json e contact.jpg voltam para rec/t21/_ens. Abaixo de 450 MB livres em / o trabalho não começa (saída 4); o mp4 de
# ensaio é apagado ao fim se sobrar menos de 550 MB.
set -u
cd /home/claude/ecoflix
PORT=54321
FN=2026-11-10T08:30:00-03:00
SUF=""; RAW=$1; case "$RAW" in *b) SUF=b; RAW=${RAW%b};; esac
NN=$(printf '%02d' "$((10#$RAW))"); NOME="cap$NN$SUF"; MODO=$2
LIVRE=$(df -m / | awk 'NR==2{print $4}')
echo "$NOME:$MODO começou $(date +%H:%M:%S) livre=${LIVRE}MB"
[ "$LIVRE" -lt 450 ] && { echo "DISCO ABAIXO DE 450 MB ($LIVRE): parado"; exit 4; }
export FAKE_MUNDO=/dev/shm/t21_mundo
[ -d "$FAKE_MUNDO" ] || python3 -I rec/t21/t21_mundo.py
PIDF=rec/.runtime/fake$PORT.pid
PID=$(cat "$PIDF" 2>/dev/null || true)
# sempre reinicia a instância: o overlay guarda estado em memória (memória do Cato, rotinas) que o /__dev/reset não zera
python3 -I rec/t21/t21_mundo.py > /dev/null
( for i in 3 4 5 6 7 8 9 10; do eval "exec $i>&-"; done; FAKE_MUNDO=$FAKE_MUNDO FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake | tail -1 )
PID=$(cat "$PIDF")
tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_PORT=$PORT" || { echo "instância $PORT não é a minha"; exit 3; }
export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
# a senha só existe no ambiente deste processo (nunca vai para arquivo)
TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14); export TUT_SENHA
mkdir -p /dev/shm/t21_ens rec/t21/_ens
python3 -I rec/t21/gerar.py "$RAW$SUF" > /dev/null || exit 2
if [ "$MODO" = r ]; then
  python3 -I rec/t21/ensaio.py "$RAW$SUF" > /dev/null || exit 2
  ROT=rec/t21/_ens/$NOME.json; DIR=rec/t21/_ens; EXTRA="--rapido --preset ultrafast --crf 30"; RES=--ens
else
  ROT=rec/t21/$NOME.json; DIR=rec/t21/_ens; EXTRA="--preset ultrafast --crf 30"; RES=--ens
fi
TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('/home/claude/ecoflix/t21/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+420))" "$NN")
OUT="$DIR/.t21-$NOME.out"
timeout $TMO node rec/record.mjs "$ROT" --out /dev/shm/t21_ens $EXTRA > "$OUT" 2>&1; RC=$?
for e in actions.json telemetry.json mp4 contact.jpg; do mv -f /dev/shm/t21_ens/t21-$NOME.$e "$DIR/" 2>/dev/null; done
rm -rf /dev/shm/t21_ens/t21-$NOME* 2>/dev/null
FALHOS=$(python3 -I -c "import json;a=json.load(open('$DIR/t21-$NOME.actions.json'))['actions'];print(sum(1 for x in a if x.get('error') or x.get('ok') is False))" 2>/dev/null || echo x)
python3 -I rec/t21/resumo.py "$RAW$SUF" $RES > "$DIR/t21-$NOME.resumo.txt" 2>&1
[ "$(df -m / | awk 'NR==2{print $4}')" -lt 550 ] && rm -f "$DIR/t21-$NOME.mp4"
echo "fim $NOME:$MODO $(date +%H:%M:%S) rc=$RC falhos=$FALHOS livre=$(df -m / | awk 'NR==2{print $4}')MB SEM-ALVO=$(grep -c 'SEM ALVO' "$OUT")"
tail -2 "$OUT"; head -3 "$DIR/t21-$NOME.resumo.txt"
exit $RC
