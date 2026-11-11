#!/bin/bash
# T18 · grava (ou ensaia) UM capítulo na instância do T18 (porta 54318), com o FAKE_NOW do capítulo (rec/t18/fake_now.json, escrito
# pelo gerar.py). Religa a instância quando o FAKE_NOW muda ou quando handler/hook/lib do mundo mudou depois dela.
# Uso: bash rec/t18/t18_grava.sh NN [--rapido] [--seed apos-capNN]   (FORA de outro flock: a trava é pega aqui, só na gravação)
# --seed: logo depois da gravação, ainda com a trava, grava a semente cumulativa (t18_semente.py) com o estado da instância.
set -u
cd /home/claude/ecoflix
NN=$(printf '%02d' "$((10#$1))"); shift
MODO=""; SEED=""
while [ $# -gt 0 ]; do case "$1" in --rapido) MODO=--rapido;; --seed) SEED=$2; shift;; esac; shift; done
PORT=54318
PIDF=rec/.runtime/fake$PORT.pid
FN=$(python3 -I -c "import json,sys;print(json.load(open('rec/t18/fake_now.json'))[sys.argv[1]])" "$NN") || exit 2
PID=$(cat "$PIDF" 2>/dev/null || true)
ATUAL=""; PORTA=""
if [ -n "$PID" ] && [ -r /proc/$PID/environ ]; then
  ATUAL=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_NOW=' | cut -d= -f2-)
  PORTA=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_PORT=' | cut -d= -f2-)
  [ "$PORTA" != "$PORT" ] && rm -f /home/claude/ecoflix/rec/.runtime/fake54318.pid
fi
MUDOU=$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib -name '*.mjs' -newer "$PIDF" 2>/dev/null | head -1)
if [ "$ATUAL" != "$FN" ] || [ "$PORTA" != "$PORT" ] || [ -n "$MUDOU" ]; then
  FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake 9>&- | tail -1
fi
PID=$(cat "$PIDF")
tr '\0' '\n' < /proc/$PID/environ | grep -q "^FAKE_PORT=$PORT$" || { echo "instância $PORT não é a minha"; exit 3; }
export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
echo "cap$NN FAKE_NOW=$FN $(date +%H:%M:%S) $MODO"
if [ "$MODO" = "--rapido" ]; then
  python3 -I rec/t18/ensaio.py "$NN" || exit 2
  ROT="rec/t18/_ens/cap$NN.json"; OUT="rec/t18/_ens/.cap$NN.out"; EXTRA="--rapido --no-encode"
else
  ROT="rec/t18/cap$NN.json"; OUT="rec/t18/.cap$NN.out"; EXTRA=""
fi
if [ -n "$SEED" ]; then
  flock .heavy.lock bash -c "node rec/record.mjs $ROT $EXTRA > $OUT 2>&1; r=\$?; python3 -I rec/t18/t18_semente.py $SEED >> $OUT 2>&1; exit \$r"
else
  flock .heavy.lock node rec/record.mjs $ROT $EXTRA > "$OUT" 2>&1
fi
RC=$?
echo "fim cap$NN $(date +%H:%M:%S) exit $RC"; grep -c "SEM ALVO" "$OUT" | sed 's/^/SEM ALVO: /'; tail -3 "$OUT"
exit $RC
