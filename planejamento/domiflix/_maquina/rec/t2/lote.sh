#!/usr/bin/env bash
# T2 · grava VÁRIOS capítulos em sequência, com UMA TRAVA POR CAPÍTULO (cada capítulo pega e solta o flock; a fila dos outros agentes anda).
# uso: rec/t2/lote.sh 00 01 02 [--rapido] [--seguir]
#   --rapido  ensaio sem esperar a fala (tira os `at`; rec/t2/_ens/): acha seletor errado; não mede o ritmo
#   --seguir  não para no 1º capítulo com passo falho (cada capítulo parte da própria semente apos-capNN, então dá para seguir)
# Instância própria do Supabase falso (porta 54324, base do T2); o app (8080) é compartilhado. Rodar em segundo plano, prazo generoso.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54324 FAKE_NOW="2026-11-03T09:00:00-03:00"
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(bash rec/t2/senha_demo.sh)"
CAPS=(); RAPIDO=""; SEGUIR=""
for a in "$@"; do
  case "$a" in
    --rapido) RAPIDO=1 ;;
    --seguir) SEGUIR=1 ;;
    *) CAPS+=("$(printf '%02d' "$((10#$a))")") ;;
  esac
done
[ "${#CAPS[@]}" -gt 0 ] || { echo "uso: rec/t2/lote.sh NN [NN ...] [--rapido] [--seguir]"; exit 2; }
PIDF=rec/.runtime/fake54324.pid
AMB=$(tr '\0' '\n' < "/proc/$(cat "$PIDF" 2>/dev/null)/environ" 2>/dev/null || true)  # em variável: grep -q fecha o cano e o pipefail acusa falso erro
if ! grep -q '^FAKE_SEEDS_DIR=.*seeds-extra/t2/_base$' <<< "$AMB"; then
  echo "A instância 54324 não está de pé com a base do T2: FAKE_PORT=54324 FAKE_NOW=$FAKE_NOW FAKE_SEEDS_DIR=\$PWD/rec/fakebase/seeds-extra/t2/_base rec/run.sh fake"; exit 4
fi
SAIDA=rec/t2; [ -n "$RAPIDO" ] && SAIDA=rec/t2/_ens
for NN in "${CAPS[@]}"; do
  rm -f "rec/t2/.res-${NN:?}.txt"
  python3 -I rec/t2/gerar.py "$((10#$NN))" | tail -1
  [ -n "$RAPIDO" ] && python3 -I rec/t2/ensaio.py "$((10#$NN))" | tail -1
done
RC=0
for NN in "${CAPS[@]}"; do
  ROT=rec/t2/cap$NN.json; [ -n "$RAPIDO" ] && ROT=rec/t2/_ens/cap$NN.json
  echo "=== cap$NN ($(date +%H:%M:%S)) esperando a trava"
  node rec/record.mjs "$ROT" --check | tail -1
  flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "node rec/record.mjs $ROT --out $SAIDA --name t2-cap$NN ${RAPIDO:+--no-encode} > rec/t2/.rec-$NN.log 2>&1; rc=\$?; node rec/t2/estado.mjs > rec/t2/.estado-$NN.log 2>&1; exit \$rc"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "GRAVAÇÃO FALHOU (rc=$rc), cauda do log:"; tail -12 "rec/t2/.rec-$NN.log"; RC=1
    [ -n "$SEGUIR" ] && { echo "(--seguir: continua)"; continue; }
    echo "LOTE PAROU em cap$NN"; break
  fi
  python3 -I rec/t2/resumo.py "$((10#$NN))" ${RAPIDO:+--ens} > "rec/t2/.res-$NN.txt" 2>&1
  head -2 "rec/t2/.res-$NN.txt"
  FALHOS=$(head -1 "rec/t2/.res-$NN.txt" | grep -oP 'falhos \K[0-9]+' || echo 99)
  if [ "$FALHOS" != "0" ]; then
    RC=1; [ -n "$SEGUIR" ] && { echo "cap$NN: $FALHOS falho(s) (--seguir: continua)"; continue; }
    echo "LOTE PAROU em cap$NN: $FALHOS passo(s) falho(s)"; break
  fi
done
echo "--- falhos/atrasos (rec/t2/.res-NN.txt):"
for NN in "${CAPS[@]}"; do [ -f "rec/t2/.res-$NN.txt" ] && grep -E "ERRO|ATRASO" "rec/t2/.res-$NN.txt" | head -8; done
echo "FIM lote rc=$RC"
exit "$RC"
