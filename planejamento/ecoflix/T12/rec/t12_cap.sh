#!/bin/bash
# T12 · um capítulo numa trava só (fila longa: ~40 min por vez): ensaio rápido; se 0 falho, a semente apos-capNN (capítulos da cadeia) e,
# se o prever.py não acusar atraso >= 0,8 s, o ensaio completo logo em seguida. Tudo o que mexe na instância 54312 (gravação, semente)
# fica DENTRO da trava, então duas filas minhas podem esperar ao mesmo tempo sem uma estragar o estado da outra.
# Uso: bash rec/t12/t12_cap.sh NN [--so-rapido|--so-completo]   (FORA de outro flock; não editar com uma fila rodando)
set -u
cd /home/claude/ecoflix
NN=$(printf '%02d' "$((10#$1))"); MODO=${2:-}
PORT=54312; PIDF=rec/.runtime/fake$PORT.pid; FN=2026-11-10T07:00:00-03:00
SEMEIA=" 05 06 07 08 09 "
export FAKE_URL=http://127.0.0.1:$PORT FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
python3 -I rec/t12/gerar.py "$NN" | tail -1
python3 -I rec/t12/ensaio.py "$NN" >/dev/null
echo "cap$NN espera a trava $(date +%H:%M:%S)"
exec 9>.heavy.lock
flock 9
echo "cap$NN pegou a trava $(date +%H:%M:%S)"
# instância: a minha, com o FAKE_NOW certo, e religada se handler/hook/lib mudou (o serviço nunca herda a trava: 9>&-)
PID=$(cat "$PIDF" 2>/dev/null || true); ATUAL=""; PORTA=""
if [ -n "$PID" ] && [ -r /proc/$PID/environ ]; then
  ATUAL=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_NOW=' | cut -d= -f2-)
  PORTA=$(tr '\0' '\n' < /proc/$PID/environ | grep '^FAKE_PORT=' | cut -d= -f2-)
  [ "$PORTA" != "$PORT" ] && rm -f "$PIDF"
fi
MUDOU=$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib -name '*.mjs' -newer "$PIDF" 2>/dev/null | head -1)
if [ "$ATUAL" != "$FN" ] || [ "$PORTA" != "$PORT" ] || [ -n "$MUDOU" ]; then
  FAKE_NOW=$FN FAKE_PORT=$PORT bash rec/run.sh fake 9>&- | tail -1
fi
PID=$(cat "$PIDF"); tr '\0' '\n' < /proc/$PID/environ | grep -q "^FAKE_PORT=$PORT$" || { echo "instância $PORT não é a minha"; exit 3; }
OKR=1
if [ "$MODO" != "--so-completo" ]; then
  node rec/record.mjs "rec/t12/_ens/cap$NN.json" --rapido --no-encode > "rec/t12/_ens/.cap$NN.out" 2>&1
  FR=$(grep -c "FALHOU" "rec/t12/_ens/.cap$NN.out"); SR=$(grep -c "SEM ALVO" "rec/t12/_ens/.cap$NN.out")
  echo "cap$NN rapido falhos $FR sem_alvo $SR $(date +%H:%M:%S)"
  python3 -I rec/t12/resumo.py "$NN" --ens > "rec/t12/_ens/resumo$NN.txt" 2>&1
  [ "$FR" = "0" ] || OKR=0
  if [ "$OKR" = "1" ] && [[ "$SEMEIA" == *" $NN "* ]]; then python3 -I rec/t12/t12_semente.py "apos-cap$NN" | tail -3; fi
fi
if [ "$OKR" = "1" ] && [ "$MODO" != "--so-rapido" ]; then
  MAIOR=$(python3 -I rec/t12/prever.py "$NN" --ens 2>&1 | grep -o "maior atraso [0-9.]*" | grep -o "[0-9.]*$")
  echo "cap$NN prever: maior atraso ${MAIOR:-?} s"
  if [ "$MODO" = "--so-completo" ] || awk "BEGIN{exit !(${MAIOR:-9} < 0.8)}"; then
    node rec/record.mjs "rec/t12/cap$NN.json" > "rec/t12/.cap$NN.out" 2>&1
    FC=$(grep -c "FALHOU" "rec/t12/.cap$NN.out"); SC=$(grep -c "SEM ALVO" "rec/t12/.cap$NN.out")
    echo "cap$NN completo falhos $FC sem_alvo $SC $(date +%H:%M:%S)"
    rm -f "rec/t12/t12-cap$NN.mp4"   # disco curto: fica a folha de contato
    python3 -I rec/t12/resumo.py "$NN" > "rec/t12/resumo$NN.txt" 2>&1
  else
    echo "cap$NN completo adiado (prever acusa atraso)"
  fi
fi
flock -u 9
echo "cap$NN soltou a trava $(date +%H:%M:%S)"
