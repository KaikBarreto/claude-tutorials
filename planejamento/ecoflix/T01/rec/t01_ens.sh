#!/usr/bin/env bash
# T1 · ensaio de um capítulo, UMA trava por capítulo (docs/04-gravacao.md). Quadros, MP4 e folha de contato ficam em /dev/shm
# (o disco de /home está quase cheio: 200 s de gravação são ~1 GB de quadros); só o actions.json e o telemetry.json voltam para
# rec/t01 (o prever.py e o resumo.py usam). Uso (de qualquer pasta):
#   bash rec/t01/t01_ens.sh rapido 05 [--seed]   ensaio rápido (sem os `at`, sem MP4) + resumo + prévia; --seed grava apos-capNN
#   bash rec/t01/t01_ens.sh completo 05          gravação com os tempos estimados (MP4 + folha em /dev/shm/t01_rec) + resumo
# Precisa no ambiente: TUT_USER e TUT_SENHA (a senha nunca vai para arquivo). FAKE_URL/FAKE_NOW fixos da aula (porta 54301).
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."   # $TUT_HOME
MODO="$1"; NN="$(printf %02d "$((10#$2))")"; SEED="${3:-}"
export FAKE_URL=http://127.0.0.1:54301 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:?defina TUT_USER}"; : "${TUT_SENHA:?defina TUT_SENHA}"
PID="$(cat rec/.runtime/fake54301.pid 2>/dev/null)"
AMB="$(tr '\0' '\n' < "/proc/$PID/environ" 2>/dev/null)"   # lido de uma vez (grep -q num pipe com pipefail falhava às vezes: SIGPIPE no tr)
if ! grep -qx 'FAKE_PORT=54301' <<< "$AMB" || ! grep -qx "FAKE_NOW=$FAKE_NOW" <<< "$AMB"; then
  echo "instância 54301 não é a da aula (ou caiu): suba com FAKE_NOW=$FAKE_NOW FAKE_PORT=54301 bash rec/run.sh fake" >&2; exit 3
fi
python3 -I rec/t01/gerar.py "$NN" > /dev/null || exit 4
SHM=/dev/shm/t01_rec
if [ "$MODO" = rapido ]; then
  python3 -I rec/t01/ensaio.py "$NN"
  mkdir -p "$SHM/_ens"; rm -rf "$SHM/_ens/_debug"   # _debug: fotos dos passos que falharam (ficam para olhar)
  CMD="node rec/record.mjs rec/t01/_ens/cap$NN.json --rapido --no-encode --out $SHM/_ens"
  [ "$SEED" = --seed ] && CMD="$CMD && python3 -I rec/t01/t01_semente.py $NN"
  flock .heavy.lock bash -c "$CMD" > "rec/t01/_ens/cap$NN.log" 2>&1; echo "saida $?" >> "rec/t01/_ens/cap$NN.log"
  cp -f "$SHM/_ens/t01-cap$NN.actions.json" "$SHM/_ens/t01-cap$NN.telemetry.json" rec/t01/_ens/ 2>/dev/null
  rm -rf "$SHM/_ens/_frames"
  python3 -I rec/t01/resumo.py "$NN" --ens > "rec/t01/_ens/cap$NN.resumo.txt" 2>&1
  python3 -I rec/t01/prever.py "$NN" --ens > "rec/t01/_ens/cap$NN.prever.txt" 2>&1
  echo "SEM ALVO: $(grep -c "SEM ALVO" "rec/t01/_ens/cap$NN.resumo.txt")" >> "rec/t01/_ens/cap$NN.resumo.txt"
  head -1 "rec/t01/_ens/cap$NN.resumo.txt"; tail -1 "rec/t01/_ens/cap$NN.prever.txt"
else
  mkdir -p "$SHM"; rm -rf "$SHM/_debug"
  flock .heavy.lock node rec/record.mjs "rec/t01/cap$NN.json" --out "$SHM" > "rec/t01/cap$NN.log" 2>&1; echo "saida $?" >> "rec/t01/cap$NN.log"
  cp -f "$SHM/t01-cap$NN.actions.json" "$SHM/t01-cap$NN.telemetry.json" rec/t01/ 2>/dev/null
  rm -rf "$SHM/_frames"
  python3 -I rec/t01/resumo.py "$NN" > "rec/t01/cap$NN.resumo.txt" 2>&1
  echo "SEM ALVO: $(grep -c "SEM ALVO" "rec/t01/cap$NN.resumo.txt")" >> "rec/t01/cap$NN.resumo.txt"
  head -1 "rec/t01/cap$NN.resumo.txt"
fi
