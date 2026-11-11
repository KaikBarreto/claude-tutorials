#!/usr/bin/env bash
# T09 · um capítulo numa trava só (a fila da trava passa de 40 min): ensaio rápido -> se 0 falho e nenhum "SEM ALVO", prever.py e a
# gravação completa com os tempos. Fora da trava: gerar.py antes; t09_pdfs.py e os resumos depois.
#   bash rec/t09/t09_ciclo.sh NN            rápido + completo
#   bash rec/t09/t09_ciclo.sh NN rapido     só o rápido
# Instância: a da T09 (porta 54309, FAKE_NOW 2026-11-11T08:30:00-03:00); se não estiver assim, para (suba FORA da trava).
set -uo pipefail
cd /home/claude/ecoflix
NN=$(printf %02d "$((10#$1))"); MODO="${2:-completo}"
export FAKE_URL=http://127.0.0.1:54309 FAKE_NOW=2026-11-11T08:30:00-03:00 NN MODO
export TUT_USER=rafael@reciclavalemetais.example
export TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)}"
PID=$(cat rec/.runtime/fake54309.pid 2>/dev/null)
INST=$(tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -E '^FAKE_(PORT|NOW)=' | sort | tr '\n' ' ')
case "$INST" in
  *"FAKE_NOW=$FAKE_NOW"*"FAKE_PORT=54309"*) ;;
  *) echo "cap$NN: instância 54309 não está com FAKE_NOW=$FAKE_NOW (achei: ${INST:-nada}); suba de novo fora da trava"; exit 3 ;;
esac
python3 -I rec/t09/gerar.py "$NN" >/dev/null || exit 4
python3 -I rec/t09/ensaio.py "$NN" >/dev/null || exit 4
E=rec/t09/_ens
flock .heavy.lock bash -c '
  echo "trava $(date +%T)" > "rec/t09/_ens/.ens-$NN.out"
  timeout 900 node rec/record.mjs "rec/t09/_ens/cap$NN.json" --rapido --no-encode >> "rec/t09/_ens/.ens-$NN.out" 2>&1; echo "rc=$?" >> "rec/t09/_ens/.ens-$NN.out"
  python3 -I rec/t09/resumo.py "$NN" --ens --tudo > "rec/t09/_ens/.resumo-$NN.txt" 2>&1
  ok=1; head -1 "rec/t09/_ens/.resumo-$NN.txt" | grep -q "falhos 0," || ok=0
  grep -q "SEM ALVO" "rec/t09/_ens/t09-cap$NN.actions.json" 2>/dev/null && ok=0
  if [ "$ok" = 1 ] && [ "$MODO" != rapido ]; then
    python3 -I rec/t09/prever.py "$NN" --ens > "rec/t09/.prever-$NN.txt" 2>&1
    pior=$(grep -o "maior atraso [0-9.]*" "rec/t09/.prever-$NN.txt" | grep -o "[0-9.]*$" | head -1)
    if [ -n "$pior" ] && python3 -c "import sys; sys.exit(0 if float(sys.argv[1]) >= 0.8 else 1)" "$pior"; then
      echo "prever: atraso previsto $pior s (>= 0,8): sem gravação completa" >> "rec/t09/_ens/.ens-$NN.out"; echo "solta $(date +%T)" >> "rec/t09/_ens/.ens-$NN.out"; exit 0
    fi
    timeout 1200 node rec/record.mjs "rec/t09/cap$NN.json" > "rec/t09/.rec-$NN.out" 2>&1; echo "rc=$?" >> "rec/t09/.rec-$NN.out"
    python3 -I rec/t09/resumo.py "$NN" > "rec/t09/.resumo-$NN.txt" 2>&1
  fi
  echo "solta $(date +%T)" >> "rec/t09/_ens/.ens-$NN.out"'
python3 -I rec/t09/t09_pdfs.py "$NN" --ens > /dev/null 2>&1
echo "===== cap$NN rápido: $(head -1 $E/.resumo-$NN.txt 2>/dev/null)  SEM ALVO: $(grep -c 'SEM ALVO' $E/t09-cap$NN.actions.json 2>/dev/null)"
grep -E "DIFERENTE|FALHOU|falhou|ERRO|SEM PDF|SEM ABA|pageError|failed:" $E/.resumo-$NN.txt $E/.ens-$NN.out 2>/dev/null | head -8
if [ -f "rec/t09/.resumo-$NN.txt" ] && [ "rec/t09/.resumo-$NN.txt" -nt "$E/.resumo-$NN.txt" ]; then
  python3 -I rec/t09/t09_pdfs.py "$NN" > "rec/t09/.pdfs-$NN.txt" 2>&1
  echo "----- cap$NN completo: $(head -2 rec/t09/.resumo-$NN.txt | tr '\n' ' ')"
  grep -E "DIFERENTE|FALHOU|falhou|ERRO|SEM PDF|SEM ABA|pageError|failed:" rec/t09/.resumo-$NN.txt rec/t09/.rec-$NN.out 2>/dev/null | head -8
  grep -E "previsto|atraso" rec/t09/.prever-$NN.txt 2>/dev/null | tail -2
fi
