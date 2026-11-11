#!/bin/bash
# T17 · fila de ensaios/gravações (um capítulo por trava, na ordem dada). Itens: NN:r (ensaio rápido) ou NN:c (gravação completa),
# com :apos-capNN no fim para gravar a semente cumulativa logo depois (dentro da mesma trava).
# Uso: bash rec/t17/t17_fila.sh 00:r 01:r 02:r:apos-cap02 ...   (rodar FORA de outro flock; em segundo plano com timeout de 2 h)
# Para nunca ser morto no meio de uma gravação pelo prazo do segundo plano, a espera da trava tem limite (flock -w): passou de
# ~1 h 50 min, o item não começa e a fila sai com "PARADA" (relançar com os itens que faltam).
set -u
cd /home/claude/ecoflix
PORT=54317
PIDF=rec/.runtime/fake$PORT.pid
INICIO=$(date +%s)
LOG=rec/t17/fila.log
for item in "$@"; do
  IFS=: read -r NN MODO SEED <<< "$item"
  NN=$(printf '%02d' "$((10#$NN))")
  FN=$(python3 -I -c "import json,sys;print(json.load(open('rec/t17/fake_now.json'))[sys.argv[1]])" "$NN") || exit 2
  PID=$(cat "$PIDF" 2>/dev/null || true)
  ATUAL=$(tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep '^FAKE_NOW=' | cut -d= -f2-)
  PORTA=$(tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep '^FAKE_PORT=' | cut -d= -f2-)
  [ -n "$PID" ] && [ "$PORTA" != "$PORT" ] && rm -f /home/claude/ecoflix/rec/.runtime/fake54317.pid
  MUDOU=$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib -name '*.mjs' -newer "$PIDF" 2>/dev/null | head -1)
  if [ "$ATUAL" != "$FN" ] || [ "$PORTA" != "$PORT" ] || [ -n "$MUDOU" ]; then
    FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake 9>&- | tail -1
  fi
  PID=$(cat "$PIDF")
  tr '\0' '\n' < /proc/$PID/environ | grep -q "^FAKE_PORT=$PORT$" || { echo "instância $PORT não é a minha" | tee -a $LOG; exit 3; }
  export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
  [ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
  if [ "$MODO" = "r" ]; then
    python3 -I rec/t17/ensaio.py "$NN" > /dev/null || exit 2
    # processo de 11/11 18:46: o rápido monta o MP4 (folha de contato) e o completo só onde a regra pede (_BRIEF_ROBO.md, item 3)
    ROT="rec/t17/_ens/cap$NN.json"; OUT="rec/t17/_ens/.cap$NN.out"; EXTRA="--rapido"
  else
    ROT="rec/t17/cap$NN.json"; OUT="rec/t17/.cap$NN.out"; EXTRA=""
  fi
  RESTA=$(( 6600 - ($(date +%s) - INICIO) ))
  if [ "$RESTA" -lt 300 ]; then echo "PARADA antes de cap$NN:$MODO (prazo)" | tee -a $LOG; exit 4; fi
  echo "cap$NN:$MODO espera a trava $(date +%H:%M:%S) (limite ${RESTA}s)" | tee -a $LOG
  : > "$OUT"
  if [ -n "${SEED:-}" ]; then
    flock -w "$RESTA" .heavy.lock bash -c "node rec/record.mjs $ROT $EXTRA > $OUT 2>&1; r=\$?; if [ \$r -eq 0 ]; then python3 -I rec/t17/t17_semente.py $SEED >> $OUT 2>&1; else echo 'semente NAO gravada (gravacao com falha)' >> $OUT; fi; exit \$r"
  else
    flock -w "$RESTA" .heavy.lock bash -c "node rec/record.mjs $ROT $EXTRA > $OUT 2>&1"
  fi
  RC=$?
  if [ ! -s "$OUT" ]; then echo "PARADA: trava não veio a tempo para cap$NN:$MODO" | tee -a $LOG; exit 4; fi
  echo "fim cap$NN:$MODO $(date +%H:%M:%S) exit $RC; SEM ALVO $(grep -c 'SEM ALVO' "$OUT"); $(grep -E 'falhos|passos,' "$OUT" | tail -1 | cut -c1-120)" | tee -a $LOG
done
echo "fila concluída $(date +%H:%M:%S)" | tee -a $LOG
