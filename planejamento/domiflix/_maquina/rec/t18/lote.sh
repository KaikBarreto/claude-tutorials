#!/usr/bin/env bash
# T18 · grava VÁRIOS capítulos em sequência, com UMA TRAVA POR CAPÍTULO (regra de 31/10: nunca um lote inteiro sob um flock só;
# entre um capítulo e outro a fila dos outros agentes anda). Para no 1º capítulo com passo falho ou erro de gravação.
# uso: rec/t18/lote.sh 02 03 04 [--rapido]
#   --rapido  ensaio sem esperar a fala (tira os `at`; rec/t18/_ens/): acha seletor errado; não mede o ritmo
#   --seguir  não para no 1º capítulo com passo falho: vai até o fim e mostra tudo (bom no ensaio rápido)
# Cada capítulo parte da mesma semente (o T18 não cria dado da empresa), então quem entra na trava entre dois capítulos não atrapalha.
# Tudo de navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`. Instância própria do Supabase falso (porta 54322).
# Rodar em segundo plano com prazo GENEROSO (a espera na fila conta); um `timeout` curto mata o flock e a gravação em andamento.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54322 FAKE_NOW="2026-11-11T11:00:00-03:00"
CAPS=(); RAPIDO=""; SEGUIR=""
for a in "$@"; do
  case "$a" in
    --rapido) RAPIDO=1 ;;
    --seguir) SEGUIR=1 ;;
    *) CAPS+=("$(printf '%02d' "$((10#$a))")") ;;
  esac
done
[ "${#CAPS[@]}" -gt 0 ] || { echo "uso: rec/t18/lote.sh NN [NN ...] [--rapido]"; exit 2; }
SAIDA=rec/t18
[ -n "$RAPIDO" ] && SAIDA=rec/t18/_ens
for NN in "${CAPS[@]}"; do
  rm -f "rec/t18/.res-${NN:?}.txt"
  python3 -I rec/t18/gerar.py "$NN" | tail -1
  [ -n "$RAPIDO" ] && python3 -I rec/t18/ensaio.py "$NN" | tail -1
done
RC=0
for NN in "${CAPS[@]}"; do
  ROT=rec/t18/cap$NN.json; [ -n "$RAPIDO" ] && ROT=rec/t18/_ens/cap$NN.json
  echo "=== cap$NN ($(date +%H:%M:%S)) esperando a trava"
  node rec/record.mjs "$ROT" --check | tail -1
  flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "node rec/record.mjs $ROT --out $SAIDA --name t18-cap$NN ${RAPIDO:+--no-encode} > rec/t18/.rec-$NN.log 2>&1"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "GRAVAÇÃO FALHOU (rc=$rc), cauda do log:"; tail -20 "rec/t18/.rec-$NN.log"; RC=1
    if [ -n "$SEGUIR" ]; then echo "(--seguir: continua)"; continue; fi
    echo "LOTE PAROU em cap$NN"; break
  fi
  python3 -I rec/t18/resumo.py "$NN" ${RAPIDO:+--ens} > "rec/t18/.res-$NN.txt" 2>&1
  head -2 "rec/t18/.res-$NN.txt"
  FALHOS=$(head -1 "rec/t18/.res-$NN.txt" | grep -oP 'falhos \K[0-9]+' || echo 99)
  if [ "$FALHOS" != "0" ]; then
    RC=1
    if [ -n "$SEGUIR" ]; then echo "cap$NN: $FALHOS passo(s) falho(s) (--seguir: continua)"; continue; fi
    echo "LOTE PAROU em cap$NN: $FALHOS passo(s) falho(s)"; break
  fi
done
echo "--- resumos (rec/t18/.res-NN.txt):"
for NN in "${CAPS[@]}"; do [ -f "rec/t18/.res-$NN.txt" ] && head -40 "rec/t18/.res-$NN.txt"; done
echo "FIM lote rc=$RC"
exit "$RC"
