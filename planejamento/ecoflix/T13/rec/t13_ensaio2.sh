#!/usr/bin/env bash
# T13 · ensaio de um capítulo (uma trava por capítulo; molde rec/t04/t04_ensaio.sh). Uso: bash rec/t13/t13_ensaio.sh NN [rapido|completo] [--semente]
#   rapido   : ensaio.py NN (sem os `at`) + gravação --rapido + resumo.py NN --ens
#   completo : gravação com os `at` (capNN.json) + resumo.py NN
#   --semente: depois de 0 passo falho, captura o estado do Supabase falso em seeds-extra/t13/apos-capNN.json
# A senha do login é aleatória, só no ambiente deste processo (o Supabase falso aceita qualquer uma); nunca vai para arquivo.
# Apaga o MP4 do ensaio rápido logo depois (disco curto); a folha de contato fica sempre, para olhar (regra de 11/11 18:46) e apagar
# olhar (apagar à mão depois de olhar).
set -u
cd "$(dirname "$0")/../.."
NN=$(printf '%02d' "$((10#$1))")
MODO=${2:-rapido}
PORTA=54313
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:$PORTA TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)
export TUT_SENHA
PID=$(cat rec/.runtime/fake$PORTA.pid 2>/dev/null)
if [ -z "$PID" ] || ! tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -qx "FAKE_PORT=$PORTA"; then
  echo "instância $PORTA fora do ar ou de outro: suba com FAKE_NOW=$FAKE_NOW FAKE_PORT=$PORTA bash rec/run.sh fake"; exit 3
fi
tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_NOW=$FAKE_NOW" || { echo "instância $PORTA sem FAKE_NOW=$FAKE_NOW"; exit 3; }
if [ "$MODO" = rapido ]; then
  python3 -I rec/t13/ensaio.py "$NN" || exit 2
  mkdir -p rec/t13/_ens; [ -e rec/t13/_ens/assets ] || ln -s ../assets rec/t13/_ens/assets
  ROT=rec/t13/_ens/cap$NN.json; DIR=rec/t13/_ens; EXTRA=--rapido; RES="--ens"
else
  ROT=rec/t13/cap$NN.json; DIR=rec/t13; EXTRA=; RES=""
fi
# gravação e captura da semente na MESMA trava (outra gravação na instância reseta o banco: docs/08, T5)
SEM=0; [ "${3:-}" = --semente ] && SEM=1
flock .heavy.lock bash -c '
  timeout 900 node rec/record.mjs "$1" $2 > "$3/.t13-cap$4.out" 2>&1; rc=$?
  if [ "$5" = 1 ] && [ $rc = 0 ]; then
    f=$(python3 -I -c "import json;a=json.load(open(\"$3/t13-cap$4.actions.json\"))[\"actions\"];print(sum(1 for x in a if x.get(\"error\") or x.get(\"ok\") is False))" 2>/dev/null || echo x)
    if [ "$f" = 0 ]; then python3 -I rec/t13/t13_sementes.py captura "$((10#$4))" --porta 54313 > "$3/.t13-cap$4.semente" 2>&1; fi
  fi
  exit $rc' _ "$ROT" "$EXTRA" "$DIR" "$NN" "$SEM"
RC=$?
tail -3 "$DIR/.t13-cap$NN.out"
python3 -I rec/t13/resumo.py "$NN" $RES > "$DIR/t13-cap$NN.resumo.txt" 2>&1
head -4 "$DIR/t13-cap$NN.resumo.txt"
grep -c "SEM ALVO" "$DIR/t13-cap$NN.actions.json" 2>/dev/null | sed 's/^/SEM ALVO no actions: /'
FALHOS=$(python3 -I -c "import json;a=json.load(open('$DIR/t13-cap$NN.actions.json'))['actions'];print(sum(1 for x in a if x.get('error') or x.get('ok') is False))" 2>/dev/null || echo '?')
echo "rc=$RC falhos=$FALHOS"
if [ "$MODO" = rapido ]; then rm -f "$DIR/t13-cap$NN.mp4"; fi   # a folha de contato fica para olhar (apagar depois)
[ -f "$DIR/.t13-cap$NN.semente" ] && [ "$SEM" = 1 ] && cat "$DIR/.t13-cap$NN.semente" && rm -f "$DIR/.t13-cap$NN.semente"
