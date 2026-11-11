#!/usr/bin/env bash
# T05 · gravação final de um capítulo (NN ou NNw): sobe a instância 54305 com o FAKE_NOW do capítulo (rec/t05/fake_now.json; o cap04 tem o
# relógio próprio do cupom 08:41:07) e grava sob a trava. Precisa de TUT_SENHA. Uso: bash rec/t05/t05_grava.sh NN [--rapido]
set -eu
cd /home/claude/ecoflix
NN="$1"; EXTRA="${2:-}"; K="${NN:0:2}"
FN=$(python3 -I -c "import json;print(json.load(open('rec/t05/fake_now.json'))['$K'])")
export FAKE_NOW="$FN" FAKE_URL=http://127.0.0.1:54305 TUT_USER=rafael@reciclavalemetais.example
: "${TUT_SENHA:?}"
bash /home/claude/ecoflix/rec/fila.sh --prio 05 -- bash -c '
  atual=$(tr "\0" "\n" < /proc/$(cat rec/.runtime/fake54305.pid)/environ | sed -n "s/^FAKE_NOW=//p")
  [ "$atual" = "$FAKE_NOW" ] || FAKE_PORT=54305 bash rec/run.sh fake >/dev/null
  timeout 900 node rec/record.mjs rec/t05/cap'"$NN"'.json '"$EXTRA"' > rec/t05/cap'"$NN"'.out 2>&1'
python3 -I rec/t05/resumo.py "$NN" > "rec/t05/cap$NN.resumo.txt" 2>&1 || true
