#!/usr/bin/env bash
# T05 · ensaio de um capítulo (NN ou NNw): prepara o rápido, grava (--rapido) sob a trava e resume. Uso: bash rec/t05/t05_ens.sh NN [--completo]
# Precisa de TUT_SENHA no ambiente. Cada chamada pega a trava uma vez (um capítulo por trava).
set -u
cd /home/claude/ecoflix || exit 1
NN="$1"; MODO="${2:---rapido}"
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54305 TUT_USER=rafael@reciclavalemetais.example
: "${TUT_SENHA:?TUT_SENHA}"
if ! tr '\0' '\n' < /proc/$(cat rec/.runtime/fake54305.pid)/environ | grep -q "^FAKE_NOW=$FAKE_NOW\$"; then echo "instância 54305 não é a minha"; exit 3; fi
if [ "$MODO" = "--rapido" ]; then
  python3 -I rec/t05/ensaio.py "$NN" >/dev/null
  SAIDA="rec/t05/_ens/cap$NN.json"; OUT="rec/t05/_ens/cap$NN.out"
  flock .heavy.lock timeout 900 node rec/record.mjs "$SAIDA" --rapido > "$OUT" 2>&1
  python3 -I rec/t05/resumo.py "$NN" --ens > "rec/t05/_ens/cap$NN.resumo.txt" 2>&1
else
  OUT="rec/t05/cap$NN.out"
  flock .heavy.lock timeout 900 node rec/record.mjs "rec/t05/cap$NN.json" > "$OUT" 2>&1
  python3 -I rec/t05/resumo.py "$NN" > "rec/t05/cap$NN.resumo.txt" 2>&1
fi
echo "fim $NN $MODO rc=$?" >> rec/t05/_ens/fila.log
