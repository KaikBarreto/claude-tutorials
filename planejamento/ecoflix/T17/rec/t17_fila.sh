#!/bin/bash
# T17 · ensaios/gravações em sequência, um capítulo por vez na fila justa da trava pesada (rec/fila.sh --prio 17: só UMA tarefa do T17
# na fila de cada vez). Itens: NN:r (ensaio rápido, MP4 ultrafast/crf 30 para a folha de contato) ou NN:c (gravação completa), com
# :apos-capNN no fim para gravar a semente cumulativa logo depois (dentro da mesma vez na trava, só se a gravação saiu sem falha).
# Uso: bash rec/t17/t17_fila.sh 00:r 01:r 02:r:apos-cap02 ...   (rodar FORA de outro flock; em segundo plano com prazo de 2 h)
# Prazo: o comando de cada item confere a hora ao ganhar a vez; passou de INICIO + 6300 s, não grava (sai 99) e a fila para com
# "PARADA" (relançar com os itens que faltam). Assim o prazo de 2 h do segundo plano nunca mata uma gravação no meio.
set -u
cd /home/claude/ecoflix
PORT=54317
PIDF=rec/.runtime/fake$PORT.pid
LIMITE=$(( $(date +%s) + 6300 ))
LOG=rec/t17/fila.log
for item in "$@"; do
  IFS=: read -r NN MODO SEED <<< "$item"
  NN=$(printf '%02d' "$((10#$NN))")
  if [ "$(date +%s)" -ge "$LIMITE" ]; then echo "PARADA antes de cap$NN:$MODO (prazo)" | tee -a $LOG; exit 4; fi
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
    ROT="rec/t17/_ens/cap$NN.json"; OUT="rec/t17/_ens/.cap$NN.out"; EXTRA="--rapido --preset ultrafast --crf 30"
  else
    ROT="rec/t17/cap$NN.json"; OUT="rec/t17/.cap$NN.out"; EXTRA=""
  fi
  SEMENTE=":"
  [ -n "${SEED:-}" ] && SEMENTE="python3 -I rec/t17/t17_semente.py $SEED >> $OUT 2>&1"
  echo "cap$NN:$MODO entra na fila $(date +%H:%M:%S)" | tee -a $LOG
  bash rec/fila.sh --prio 17 -- bash -c "if [ \$(date +%s) -ge $LIMITE ]; then echo PRAZO > $OUT; exit 99; fi
    node rec/record.mjs $ROT $EXTRA > $OUT 2>&1; r=\$?
    if [ \$r -eq 0 ]; then $SEMENTE; else echo 'semente NAO gravada (gravacao com falha)' >> $OUT; fi; exit \$r"
  RC=$?
  if [ "$RC" = "99" ]; then echo "PARADA: a vez de cap$NN:$MODO veio depois do prazo" | tee -a $LOG; exit 4; fi
  echo "fim cap$NN:$MODO $(date +%H:%M:%S) exit $RC; SEM ALVO $(grep -c 'SEM ALVO' "$OUT")" | tee -a $LOG
done
echo "fila concluída $(date +%H:%M:%S)" | tee -a $LOG
