#!/usr/bin/env bash
# T09 · ensaio e gravação de UM capítulo, sob a própria trava (os outros agentes entram entre dois capítulos).
#   bash rec/t09/t09_rodar.sh NN rapido     ensaio rápido (sem os `at`, sem MP4): falhas, seletores, "SEM ALVO"
#   bash rec/t09/t09_rodar.sh NN completo   gravação com os tempos (prever.py antes; resumo.py e t09_pdfs.py depois; MP4 + folha de contato)
# A instância do Supabase falso é a da T09 (porta 54309, FAKE_NOW 2026-11-11T08:30:00-03:00): se não estiver assim, o script para
# (suba de novo FORA da trava: FAKE_NOW=... FAKE_PORT=54309 bash rec/run.sh fake). A senha é gerada aqui e só existe no ambiente
# deste processo (o Supabase falso aceita qualquer uma).
set -uo pipefail
cd /home/claude/ecoflix
NN=$(printf %02d "$((10#$1))"); MODO="${2:-rapido}"
export FAKE_URL=http://127.0.0.1:54309 FAKE_NOW=2026-11-11T08:30:00-03:00
export TUT_USER=rafael@reciclavalemetais.example
export TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)}"
PID=$(cat rec/.runtime/fake54309.pid 2>/dev/null)
INST=$(tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -E '^FAKE_(PORT|NOW)=' | sort | tr '\n' ' ')
case "$INST" in
  *"FAKE_NOW=$FAKE_NOW"*"FAKE_PORT=54309"*) ;;
  *) echo "instância 54309 não está com FAKE_NOW=$FAKE_NOW (achei: ${INST:-nada}); suba de novo fora da trava"; exit 3 ;;
esac
python3 -I rec/t09/gerar.py "$NN" >/dev/null || exit 4
if [ "$MODO" = rapido ]; then
  python3 -I rec/t09/ensaio.py "$NN" >/dev/null
  flock .heavy.lock timeout 900 node rec/record.mjs "rec/t09/_ens/cap$NN.json" --rapido --no-encode > "rec/t09/_ens/.ens-$NN.out" 2>&1
  echo "rc=$?" >> "rec/t09/_ens/.ens-$NN.out"
  python3 -I rec/t09/resumo.py "$NN" --ens --tudo > "rec/t09/_ens/.resumo-$NN.txt" 2>&1
  python3 -I rec/t09/t09_pdfs.py "$NN" --ens > /dev/null 2>&1
  grep -c "SEM ALVO" "rec/t09/_ens/t09-cap$NN.actions.json" 2>/dev/null | sed 's/^/SEM ALVO: /'
  head -3 "rec/t09/_ens/.resumo-$NN.txt"; grep -E "ERRO|DIFERENTE|FALHOU|falhou|SEM PDF|SEM ABA" "rec/t09/_ens/.resumo-$NN.txt" "rec/t09/_ens/.ens-$NN.out" | head -12
else
  python3 -I rec/t09/prever.py "$NN" --ens > "rec/t09/.prever-$NN.txt" 2>&1
  flock .heavy.lock timeout 1200 node rec/record.mjs "rec/t09/cap$NN.json" > "rec/t09/.rec-$NN.out" 2>&1
  echo "rc=$?" >> "rec/t09/.rec-$NN.out"
  python3 -I rec/t09/resumo.py "$NN" > "rec/t09/.resumo-$NN.txt" 2>&1
  python3 -I rec/t09/t09_pdfs.py "$NN" > "rec/t09/.pdfs-$NN.txt" 2>&1
  grep -c "SEM ALVO" "rec/t09/t09-cap$NN.actions.json" 2>/dev/null | sed 's/^/SEM ALVO: /'
  head -3 "rec/t09/.resumo-$NN.txt"; grep -E "ERRO|DIFERENTE|ATRASO|FALHOU|falhou|SEM PDF|SEM ABA" "rec/t09/.resumo-$NN.txt" "rec/t09/.rec-$NN.out" | head -12
fi
