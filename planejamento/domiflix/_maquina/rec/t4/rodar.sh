#!/usr/bin/env bash
# T4 (remendo 1.38.19) · Uso: rec/t4/rodar.sh NN [--rapido] [--ensaio]
#   --rapido  ensaio sem esperar a fala (tira os `at`; rec/t4/_ens/): acha seletor errado e fecha o estado; não mede o ritmo
#   --ensaio  só captura + telemetria (--no-encode)
# Porta única 54324 (FAKE_PORT=54324 FAKE_NOW=... rec/run.sh fake); o app (8080) é compartilhado. Uma trava por capítulo.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54324 FAKE_NOW="2026-11-03T09:00:00-03:00"
NN=$(printf '%02d' "$((10#$1))"); shift
ENSAIO=""; RAPIDO=""; SEED=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    --seed) SEED=1 ;;  # grava seeds-extra/t4/novo-capNN.json (snap_novo.mjs), nunca o apos-capNN de 31/10
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
python3 -I rec/t4/gerar.py "$NN" | tail -3
node rec/record.mjs rec/t4/cap$NN.json --check | tail -1
SAIDA=rec/t4; ROT=rec/t4/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t4/ensaio.py "$NN"; SAIDA=rec/t4/_ens; ROT=rec/t4/_ens/cap$NN.json; fi
curl -s -X POST "$FAKE_URL/__dev/unknowns/clear" >/dev/null
CMD="node rec/record.mjs $ROT --out $SAIDA --name t4-cap$NN $ENSAIO > rec/t4/.rec-$NN.log 2>&1; rc=\$?"
if [ -n "$SEED" ]; then CMD="$CMD; node rec/t4/snap_novo.mjs diff $((10#$NN)) > rec/t4/.snap-$NN.log 2>&1"; fi
CMD="$CMD; exit \$rc"
if ! flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t4/.rec-$NN.log
fi
if [ -n "$SEED" ]; then echo "--- snapshot:"; tail -4 rec/t4/.snap-$NN.log; fi
echo "--- /__dev/unknowns:"; curl -s "$FAKE_URL/__dev/unknowns" | python3 -c "import json,sys;d=json.load(sys.stdin);print([(i['kind'],i['name'],i['count']) for i in d['items']] or 'vazio')"
python3 -I rec/t4/resumo.py "$NN" ${RAPIDO:+--ens} 2>&1 | head -110
