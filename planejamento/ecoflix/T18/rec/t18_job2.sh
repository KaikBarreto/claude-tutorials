#!/bin/bash
# T18 · UM trabalho do robô por vez, TUDO dentro da trava pesada (a instância 54318 também é religada aqui dentro).
# Uso: bash rec/t18/t18_job2.sh NN r          ensaio rápido do capítulo NN (ensaio.py + --rapido, sem MP4)
#      bash rec/t18/t18_job2.sh NN c          gravação completa do capítulo NN (rec/t18/capNN.json, com MP4)
#      bash rec/t18/t18_job2.sh eX e [FAKE_NOW]   exploração rec/t18/_ex/eX.json -> rec/t18/_ex/eX/ (relógio padrão 09:30)
# Rodar em segundo plano (run_in_background); a espera da trava é limitada a 1 h 50; a execução, a ~3x a duração do capítulo.
set -u
cd /home/claude/ecoflix
PORT=54318
PIDF=rec/.runtime/fake$PORT.pid
ALVO=$1; MODO=$2
if [ "$MODO" = "e" ]; then
  NN=$ALVO; FN=${3:-2026-11-10T09:30:00-03:00}; TMO=900
else
  NN=$(printf '%02d' "$((10#$ALVO))")
  FN=$(python3 -I -c "import json,sys;print(json.load(open('rec/t18/fake_now.json'))[sys.argv[1]])" "$NN") || exit 2
  TMO=$(python3 -I -c "import json,sys;print(int(json.load(open('t18/narracao/cap'+sys.argv[1]+'.json'))['dur']*3+180))" "$NN") || exit 2
fi
echo "$NN:$MODO espera a trava $(date +%H:%M:%S)"
exec 9>.heavy.lock
flock -w 6600 9 || { echo "sem trava em 1 h 50"; exit 4; }
echo "$NN:$MODO começou $(date +%H:%M:%S) FAKE_NOW=$FN"
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
case "$MODO" in
  e)
    mkdir -p rec/t18/_ex/$NN
    timeout $TMO node rec/t18/explorar.mjs rec/t18/_ex/$NN.json --out rec/t18/_ex/$NN > rec/t18/_ex/$NN.log 2>&1; RC=$?
    echo "fim ex $NN $(date +%H:%M:%S) exit $RC"; tail -3 rec/t18/_ex/$NN.log ;;
  r|s)
    python3 -I rec/t18/ensaio.py "$NN" > /dev/null || exit 2
    # r = ensaio TOLERANTE (explorativo): todo passo vira `optional` e o robô segue até o fim, para achar TODOS os seletores errados de uma vez;
    # s = ensaio ESTRITO (o de aceite: 0 passos falhos, sem "SEM ALVO").
    if [ "$MODO" = "r" ]; then python3 -I - "$NN" <<'PY'
import json, sys
p = f'rec/t18/_ens/cap{sys.argv[1]}.json'
d = json.load(open(p, encoding='utf8'))
for st in d['steps']:
    if st.get('do') in ('click', 'type', 'hover', 'waitFor', 'press'):
        st['optional'] = True
        st['timeout'] = min(st.get('timeout', 6), 6)
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
PY
    fi
    OUT="rec/t18/_ens/.cap$NN.out"
    timeout $TMO node rec/record.mjs rec/t18/_ens/cap$NN.json --rapido --no-encode > "$OUT" 2>&1; RC=$?
    echo "fim cap$NN r $(date +%H:%M:%S) exit $RC"; grep -c "SEM ALVO" "$OUT" | sed 's/^/SEM ALVO: /'; tail -3 "$OUT" ;;
  c)
    OUT="rec/t18/.cap$NN.out"
    timeout $TMO node rec/record.mjs rec/t18/cap$NN.json > "$OUT" 2>&1; RC=$?
    echo "fim cap$NN c $(date +%H:%M:%S) exit $RC"; grep -c "SEM ALVO" "$OUT" | sed 's/^/SEM ALVO: /'; tail -3 "$OUT" ;;
esac
exit $RC
