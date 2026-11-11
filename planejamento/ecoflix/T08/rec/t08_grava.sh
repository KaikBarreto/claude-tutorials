#!/bin/bash
# T08 · grava (ou ensaia) UM capítulo na instância do T08 (porta 54308), com o FAKE_NOW do capítulo (rec/t08/fake_now.json,
# escrito pelo gerar.py). Religa a instância quando o FAKE_NOW muda ou quando handler/hook/lib do mundo mudou depois dela.
# Uso: bash rec/t08/t08_grava.sh NN [--rapido]    (rodar FORA de outro flock: a trava é pega aqui, só na gravação)
set -u
cd /home/claude/ecoflix
NN=$(printf '%02d' "$((10#$1))"); MODO=${2:-}
PORT=54308
PIDF=rec/.runtime/fake$PORT.pid
FN=$(python3 -I -c "import json,sys;print(json.load(open('rec/t08/fake_now.json'))[sys.argv[1]])" "$NN") || exit 2
PID=$(cat "$PIDF" 2>/dev/null || true)
ATUAL=""; PORTA=""
if [ -n "$PID" ] && [ -r /proc/$PID/environ ]; then
  ATUAL=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_NOW=' | cut -d= -f2-)
  PORTA=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_PORT=' | cut -d= -f2-)
  # .pid velho apontando para processo de outro (reinício do container): não deixar o run.sh matá-lo
  [ "$PORTA" != "$PORT" ] && rm -f /home/claude/ecoflix/rec/.runtime/fake54308.pid
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
  python3 -I rec/t08/ensaio.py "$NN" && flock .heavy.lock node rec/record.mjs "rec/t08/_ens/cap$NN.json" --rapido > "rec/t08/_ens/.cap$NN.out" 2>&1
elif [ "$MODO" = "--os-dois" ]; then
  # o ensaio rápido e, se ele sai com 0 passo falho, a gravação completa: um capítulo, uma trava (a fila passa de 20 min)
  python3 -I rec/t08/ensaio.py "$NN" || exit 2
  flock .heavy.lock bash -c "node rec/record.mjs rec/t08/_ens/cap$NN.json --rapido > rec/t08/_ens/.cap$NN.out 2>&1;
    python3 -I rec/t08/resumo.py $NN --ens > rec/t08/_ens/cap$NN.resumo 2>&1; grep -q '!!ERRO' rec/t08/_ens/cap$NN.resumo && exit 4;
    node rec/record.mjs rec/t08/cap$NN.json > rec/t08/.cap$NN.out 2>&1"
else
  flock .heavy.lock node rec/record.mjs "rec/t08/cap$NN.json" > "rec/t08/.cap$NN.out" 2>&1
fi
RC=$?
echo "fim cap$NN $(date +%H:%M:%S) exit $RC"; exit $RC
