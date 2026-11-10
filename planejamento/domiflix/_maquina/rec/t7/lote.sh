#!/usr/bin/env bash
# T7 · grava VÁRIOS capítulos em sequência numa vez só na trava (uma espera na fila em vez de uma por capítulo).
# Para no 1º capítulo com passo falho ou erro de gravação (os seguintes partem do estado do anterior, não adianta seguir).
# uso: rec/t7/lote.sh 02 03 04 [--rapido] [--seed]
#   --rapido  ensaio sem esperar a fala (tira os `at`; rec/t7/_ens/): acha seletor errado e fecha o estado; não mede o ritmo
#   --seed    depois de cada capítulo SEM falha, grava seeds-extra/t7/apos-capNN.json (snap.mjs diff NN) na mesma trava
# Tudo de navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10` (regra do coordenador, sem exceção).
# Instância própria do Supabase falso do agente A (porta 54321); o app (8080) é compartilhado e nunca é reiniciado.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54321 FAKE_NOW="2026-11-11T08:50:00-03:00"
CAPS=(); RAPIDO=""; SEED=""
for a in "$@"; do
  case "$a" in
    --rapido) RAPIDO=1 ;;
    --seed) SEED=1 ;;
    *) CAPS+=("$(printf '%02d' "$((10#$a))")") ;;
  esac
done
[ "${#CAPS[@]}" -gt 0 ] || { echo "uso: rec/t7/lote.sh NN [NN ...] [--rapido] [--seed]"; exit 2; }
SAIDA=rec/t7
[ -n "$RAPIDO" ] && SAIDA=rec/t7/_ens
# roteiros (sem navegador, sem trava): o --check de cada capítulo roda dentro da trava, depois que a semente do anterior existir
for NN in "${CAPS[@]}"; do
  rm -f "rec/t7/.res-${NN:?}.txt"
  python3 -I rec/t7/gerar.py "$NN" | tail -1
  [ -n "$RAPIDO" ] && python3 -I rec/t7/ensaio.py "$NN" | tail -1
done
# o corpo roda numa cópia (o bash lê o script aos poucos: editar este arquivo durante a gravação quebraria a execução)
CORPO="rec/t7/.lote-corpo-$$.sh"
cat > "$CORPO" <<'EOS'
set -uo pipefail
cd /home/claude/domiflix
SAIDA="$1"; RAPIDO="$2"; SEED="$3"; shift 3
for NN in "$@"; do
  ROT=rec/t7/cap$NN.json; [ -n "$RAPIDO" ] && ROT=rec/t7/_ens/cap$NN.json
  echo "=== cap$NN ($(date +%H:%M:%S))"
  node rec/record.mjs "$ROT" --check | tail -1
  python3 -I rec/t7/fotos.py "$((10#$NN))" 2>&1 | tail -1
  node rec/record.mjs "$ROT" --out "$SAIDA" --name "t7-cap$NN" ${RAPIDO:+--no-encode} > "rec/t7/.rec-$NN.log" 2>&1
  rc=$?
  if [ "$rc" -ne 0 ]; then echo "GRAVAÇÃO FALHOU (rc=$rc), cauda do log:"; tail -20 "rec/t7/.rec-$NN.log"; echo "LOTE PAROU em cap$NN"; exit 1; fi
  python3 -I rec/t7/resumo.py "$NN" ${RAPIDO:+--ens} > "rec/t7/.res-$NN.txt" 2>&1
  head -2 "rec/t7/.res-$NN.txt"
  FALHOS=$(head -1 "rec/t7/.res-$NN.txt" | grep -oP 'falhos \K[0-9]+' || echo 99)
  if [ "$FALHOS" != "0" ]; then echo "LOTE PAROU em cap$NN: $FALHOS passo(s) falho(s)"; exit 1; fi
  if [ -n "$SEED" ]; then node rec/t7/snap.mjs diff "$((10#$NN))" > "rec/t7/.snap-$NN.log" 2>&1; tail -1 "rec/t7/.snap-$NN.log"; fi
done
echo "LOTE OK: $*"
EOS
flock "$TUT_HOME/.heavy.lock" nice -n 10 bash "$CORPO" "$SAIDA" "$RAPIDO" "$SEED" "${CAPS[@]}"
RC=$?
rm -f "${CORPO:?}"
echo "--- resumos (rec/t7/.res-NN.txt):"
for NN in "${CAPS[@]}"; do [ -f "rec/t7/.res-$NN.txt" ] && head -40 "rec/t7/.res-$NN.txt"; done
echo "FIM lote rc=$RC"
exit "$RC"
