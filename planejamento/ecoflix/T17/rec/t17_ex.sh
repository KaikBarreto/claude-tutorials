#!/bin/bash
# T17 · exploração (explorar.mjs) na instância do T17 (54317), sob a trava pesada. Uso: bash rec/t17/t17_ex.sh e1 [FAKE_NOW]
set -u
cd /home/claude/ecoflix
PORT=54317
FN=${2:-2026-11-10T09:30:00-03:00}
PID=$(cat rec/.runtime/fake$PORT.pid 2>/dev/null || true)
tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -q "^FAKE_PORT=$PORT$" || { echo "instância $PORT não é a minha"; exit 3; }
ATUAL=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_NOW=' | cut -d= -f2-)
MUDOU=$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib -name '*.mjs' -newer rec/.runtime/fake$PORT.pid 2>/dev/null | head -1)
if [ "$ATUAL" != "$FN" ] || [ -n "$MUDOU" ]; then FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake 9>&- | tail -1; fi
export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
mkdir -p rec/t17/_ex/$1
echo "ex $1 $(date +%H:%M:%S) espera a trava"
flock .heavy.lock node rec/t17/explorar.mjs rec/t17/_ex/$1.json --out rec/t17/_ex/$1 > rec/t17/_ex/$1.log 2>&1
echo "fim ex $1 $(date +%H:%M:%S) exit $?"
