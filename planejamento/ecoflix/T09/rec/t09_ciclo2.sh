#!/usr/bin/env bash
# T09 · um capítulo numa trava só, pela regra de 11/11 18:46 (_BRIEF_ROBO.md, item 3):
#   sempre: o ensaio rápido COM o MP4 (folha de contato) e o prever.py;
#   completo só se: forçado (gesto sensível a espera: menu ou lista aberta com a fala andando, aviso que some sozinho...),
#   ou o prever.py mostra algum gesto com atraso >= 0,4 s, ou o rápido teve aviso. Rápido com falha/"SEM ALVO": nada de completo.
#   bash rec/t09/t09_ciclo2.sh NN            rápido; completo só pela regra
#   bash rec/t09/t09_ciclo2.sh NN completo   rápido e completo (gesto sensível a espera)
# Instância: a da T09 (porta 54309, FAKE_NOW 2026-11-11T08:30:00-03:00); se não estiver assim, para (suba FORA da trava).
set -uo pipefail
cd /home/claude/ecoflix
NN=$(printf %02d "$((10#$1))"); MODO="${2:-auto}"
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
  timeout 900 node rec/record.mjs "rec/t09/_ens/cap$NN.json" --rapido >> "rec/t09/_ens/.ens-$NN.out" 2>&1; echo "rc=$?" >> "rec/t09/_ens/.ens-$NN.out"
  python3 -I rec/t09/resumo.py "$NN" --ens --tudo > "rec/t09/_ens/.resumo-$NN.txt" 2>&1
  python3 -I rec/t09/prever.py "$NN" --ens > "rec/t09/.prever-$NN.txt" 2>&1
  ok=1; head -1 "rec/t09/_ens/.resumo-$NN.txt" | grep -q "falhos 0," || ok=0
  grep -q "SEM ALVO" "rec/t09/_ens/t09-cap$NN.actions.json" 2>/dev/null && ok=0
  sed -n 2p "rec/t09/_ens/.resumo-$NN.txt" | grep -q "pageErrors 0, failed 0, bad 0" || ok=0
  quer=0; [ "$MODO" = completo ] && quer=1
  pior=$(grep -o "maior atraso [0-9.]*" "rec/t09/.prever-$NN.txt" | grep -o "[0-9.]*$" | head -1)
  [ -n "$pior" ] && python3 -c "import sys; sys.exit(0 if float(sys.argv[1]) >= 0.4 else 1)" "$pior" && quer=1
  grep -q "\[aviso:" "rec/t09/_ens/.resumo-$NN.txt" && quer=1
  if [ "$ok" = 1 ] && [ "$quer" = 1 ]; then
    timeout 1200 node rec/record.mjs "rec/t09/cap$NN.json" > "rec/t09/.rec-$NN.out" 2>&1; echo "rc=$?" >> "rec/t09/.rec-$NN.out"
    python3 -I rec/t09/resumo.py "$NN" > "rec/t09/.resumo-$NN.txt" 2>&1
  fi
  echo "solta $(date +%T) ok=$ok completo=$quer prever=$pior" >> "rec/t09/_ens/.ens-$NN.out"'
python3 -I rec/t09/t09_pdfs.py "$NN" --ens > /dev/null 2>&1
echo "===== cap$NN rápido: $(head -1 $E/.resumo-$NN.txt 2>/dev/null)  SEM ALVO: $(grep -c 'SEM ALVO' $E/t09-cap$NN.actions.json 2>/dev/null)"
tail -1 $E/.ens-$NN.out
grep -E "DIFERENTE|FALHOU|falhou|ERRO|SEM PDF|SEM ABA|pageError|failed:|\[aviso" $E/.resumo-$NN.txt 2>/dev/null | head -8
grep -E "maior atraso" rec/t09/.prever-$NN.txt 2>/dev/null | tail -1
if [ -f "rec/t09/.resumo-$NN.txt" ] && [ "rec/t09/.resumo-$NN.txt" -nt "$E/.resumo-$NN.txt" ]; then
  python3 -I rec/t09/t09_pdfs.py "$NN" > "rec/t09/.pdfs-$NN.txt" 2>&1
  echo "----- cap$NN completo: $(head -2 rec/t09/.resumo-$NN.txt | tr '\n' ' ')"
  grep -E "DIFERENTE|FALHOU|falhou|ERRO|SEM PDF|SEM ABA|pageError|failed:" rec/t09/.resumo-$NN.txt rec/t09/.rec-$NN.out 2>/dev/null | head -8
fi
