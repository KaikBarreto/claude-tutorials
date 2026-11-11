#!/usr/bin/env bash
# T11 · ensaio e gravação de um capítulo, cada um sob a própria trava (os outros agentes entram entre dois capítulos).
#   bash rec/t11/t11_rodar.sh NN rapido     ensaio rápido (sem os `at`, sem MP4): falhas, seletores, "SEM ALVO"
#   bash rec/t11/t11_rodar.sh NN completo   gravação com os tempos (prever.py antes; resumo.py depois; MP4 + folha de contato)
# A instância do Supabase falso é a da T11 (porta 54311) e tem de estar com o FAKE_NOW do capítulo (08:30 nos caps 0 a 6,
# 17:30 do 7 ao 14): se não estiver, o script para (suba de novo FORA da trava: FAKE_NOW=... FAKE_PORT=54311 bash rec/run.sh fake).
# A senha é gerada aqui e só existe no ambiente deste processo (o Supabase falso aceita qualquer uma).
set -uo pipefail
cd /home/claude/ecoflix
NN=$(printf %02d "$((10#$1))"); MODO="${2:-rapido}"
export FAKE_URL=http://127.0.0.1:54311
if [ "$((10#$NN))" -ge 7 ]; then export FAKE_NOW=2026-11-10T17:30:00-03:00; else export FAKE_NOW=2026-11-10T08:30:00-03:00; fi
export TUT_USER=rafael@reciclavalemetais.example
export TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)}"
PID=$(cat rec/.runtime/fake54311.pid 2>/dev/null)
INST=$(tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -E '^FAKE_(PORT|NOW)=' | sort | tr '\n' ' ')
case "$INST" in
  *"FAKE_NOW=$FAKE_NOW"*"FAKE_PORT=54311"*) ;;
  *) echo "instância 54311 não está com FAKE_NOW=$FAKE_NOW (achei: ${INST:-nada}); suba de novo fora da trava"; exit 3 ;;
esac
python3 -I rec/t11/t11_sementes.py >/dev/null || exit 4   # sementes sempre do mundo base atual
python3 -I rec/t11/gerar.py "$NN" >/dev/null || exit 4
if [ "$MODO" = rapido ]; then
  python3 -I rec/t11/ensaio.py "$NN" >/dev/null
  flock .heavy.lock timeout 900 node rec/record.mjs "rec/t11/_ens/cap$NN.json" --no-encode > "rec/t11/_ens/.ens-$NN.out" 2>&1
  echo "rc=$?" >> "rec/t11/_ens/.ens-$NN.out"
  python3 -I rec/t11/resumo.py "$NN" --ens --tudo > "rec/t11/_ens/.resumo-$NN.txt" 2>&1
  grep -c "SEM ALVO" "rec/t11/_ens/.ens-$NN.out" "rec/t11/_ens/t11-cap$NN.actions.json" 2>/dev/null | sed 's/^/SEM ALVO: /'
  head -3 "rec/t11/_ens/.resumo-$NN.txt"; grep -E "ERRO|DIFERENTE|FALHOU" "rec/t11/_ens/.resumo-$NN.txt" "rec/t11/_ens/.ens-$NN.out" | head -12
else
  python3 -I rec/t11/prever.py "$NN" --ens > "rec/t11/.prever-$NN.txt" 2>&1
  flock .heavy.lock timeout 1200 node rec/record.mjs "rec/t11/cap$NN.json" > "rec/t11/.rec-$NN.out" 2>&1
  echo "rc=$?" >> "rec/t11/.rec-$NN.out"
  python3 -I rec/t11/resumo.py "$NN" > "rec/t11/.resumo-$NN.txt" 2>&1
  grep -c "SEM ALVO" "rec/t11/t11-cap$NN.actions.json" 2>/dev/null | sed 's/^/SEM ALVO: /'
  head -3 "rec/t11/.resumo-$NN.txt"; grep -E "ERRO|DIFERENTE|ATRASO|FALHOU" "rec/t11/.resumo-$NN.txt" "rec/t11/.rec-$NN.out" | head -12
fi
