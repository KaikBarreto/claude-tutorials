#!/usr/bin/env bash
# T16 · ensaio rápido e gravação completa de UM capítulo na mesma trava (um capítulo por trava; o rápido acha seletor e estado,
# o completo mede o ritmo com os tempos estimados). Uso: bash rec/t16/t16_lote.sh NN [--semente] [--so-rapido|--so-completo]
#   --semente : depois do rápido com 0 falho, captura o estado do Supabase falso em seeds-extra/t16/apos-capNN.json
# A senha do login é aleatória, só no ambiente deste processo (o falso aceita qualquer uma); nunca vai para arquivo.
# O MP4 e a folha de contato do completo ficam para olhar (apagar à mão depois); o rápido sai sem MP4 (--no-encode).
set -u
cd "$(dirname "$0")/../.."
NN=$(printf '%02d' "$((10#$1))"); shift
SEM=0; SO=ambos
for a in "$@"; do case "$a" in --semente) SEM=1;; --so-completo) SO=completo;; --so-rapido) SO=rapido;; esac; done
PORTA=54316
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:$PORTA TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14); export TUT_SENHA
PID=$(cat rec/.runtime/fake$PORTA.pid 2>/dev/null)
tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -qx "FAKE_PORT=$PORTA" || { echo "instância $PORTA fora do ar"; exit 3; }
tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_NOW=$FAKE_NOW" || { echo "instância $PORTA sem FAKE_NOW"; exit 3; }
python3 -I rec/t16/ensaio.py "$NN" > /dev/null || exit 2
mkdir -p rec/t16/_ens; [ -e rec/t16/_ens/assets ] || ln -s ../assets rec/t16/_ens/assets
FALHOS='import json,sys;a=json.load(open(sys.argv[1]))["actions"];print(sum(1 for x in a if x.get("error") or x.get("ok") is False))'
flock .heavy.lock bash -c '
  NN=$1; SEM=$2; SO=$3; F=$4
  echo "trava $(date +%T)"
  if [ "$SO" != completo ]; then
    timeout 600 node rec/record.mjs rec/t16/_ens/cap$NN.json --rapido --no-encode > rec/t16/_ens/.t16-cap$NN.out 2>&1
    f=$(python3 -I -c "$F" rec/t16/_ens/t16-cap$NN.actions.json 2>/dev/null || echo x)
    echo "rapido falhos=$f $(date +%T)"
    if [ "$SEM" = 1 ] && [ "$f" = 0 ]; then python3 -I rec/t16/t16_sementes.py captura "$((10#$NN))" --porta 54316; fi
    [ "$f" = 0 ] || exit 4
  fi
  if [ "$SO" != rapido ]; then
    timeout 900 node rec/record.mjs rec/t16/cap$NN.json > rec/t16/.t16-cap$NN.out 2>&1
    echo "completo rc=$? falhos=$(python3 -I -c "$F" rec/t16/t16-cap$NN.actions.json 2>/dev/null || echo x) $(date +%T)"
  fi' _ "$NN" "$SEM" "$SO" "$FALHOS"
RC=$?
[ "$SO" != completo ] && python3 -I rec/t16/resumo.py "$NN" --ens > rec/t16/_ens/t16-cap$NN.resumo.txt 2>&1
[ "$SO" != rapido ] && [ $RC = 0 ] && python3 -I rec/t16/resumo.py "$NN" > rec/t16/t16-cap$NN.resumo.txt 2>&1
echo "fim rc=$RC"
