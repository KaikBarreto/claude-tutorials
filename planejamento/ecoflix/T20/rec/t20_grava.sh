#!/bin/bash
# T20 · grava (ou ensaia) UM capítulo na instância do T20 (porta 54320), FAKE_NOW 10/11/2026 15:00 (plano.md). Religa a instância quando o
# FAKE_NOW muda ou quando handler/hook/lib do mundo mudou depois dela.
# Uso: bash rec/t20/t20_grava.sh NN [--rapido]    (rodar FORA de outro flock: a trava é pega aqui, só na gravação)
# Variáveis: PORTAL_SENHA (a senha do portal do cap04, só no ambiente). TUT_SENHA vem do ambiente (o falso aceita qualquer uma).
set -u
cd /home/claude/ecoflix
NN=$(printf '%02d' "$((10#$1))"); MODO=${2:-}
PORT=54320
PIDF=rec/.runtime/fake$PORT.pid
FN=2026-11-10T15:00:00-03:00
PID=$(cat "$PIDF" 2>/dev/null || true)
ATUAL=""; PORTA=""
if [ -n "$PID" ] && [ -r /proc/$PID/environ ]; then
  ATUAL=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_NOW=' | cut -d= -f2-)
  PORTA=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_PORT=' | cut -d= -f2-)
  [ "$PORTA" != "$PORT" ] && rm -f "/home/claude/ecoflix/rec/.runtime/fake$PORT.pid"
fi
MUDOU=$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib -name '*.mjs' -newer "$PIDF" 2>/dev/null | head -1)
if [ "$ATUAL" != "$FN" ] || [ "$PORTA" != "$PORT" ] || [ -n "$MUDOU" ]; then
  FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake 9>&- | tail -1
fi
PID=$(cat "$PIDF")
tr '\0' '\n' < /proc/$PID/environ | grep -q "^FAKE_PORT=$PORT$" || { echo "instância $PORT não é a minha"; exit 3; }
export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
echo "cap$NN FAKE_NOW=$FN $(date +%H:%M:%S)"
if [ "$MODO" = "--rapido" ]; then
  python3 -I rec/t20/ensaio.py "$NN" && flock .heavy.lock node rec/record.mjs "rec/t20/_ens/cap$NN.json" --rapido > "rec/t20/_ens/.cap$NN.out" 2>&1
else
  flock .heavy.lock node rec/record.mjs "rec/t20/cap$NN.json" > "rec/t20/.cap$NN.out" 2>&1
fi
RC=$?
echo "fim cap$NN $(date +%H:%M:%S) exit $RC"; exit $RC
