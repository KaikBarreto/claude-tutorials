#!/usr/bin/env bash
# T12 · Uso: rec/t12/rodar.sh NN [--ensaio] [--rapido]
#   NN         capítulo (0 a 11): gera o roteiro do robô, valida (--check), grava sob UMA trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t12/_ens/): acha seletor errado; não mede o ritmo
# Instância própria do Supabase falso: porta 54327 (`FAKE_PORT=54327 FAKE_NOW=... rec/run.sh fake`); o app (8080) é compartilhado.
# Link na tela: APP_ORIGIN=https://www.dominex.app. Cada capítulo parte da própria semente (cadeia.json); o robô reinicia o estado a cada gravação.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54327 FAKE_NOW="2026-11-10T10:00:00-03:00" APP_ORIGIN=https://www.dominex.app
NN=$(printf '%02d' "$((10#$1))")
shift
ENSAIO=""; RAPIDO=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
python3 -I rec/t12/gerar.py "$NN" | tail -3
node rec/record.mjs rec/t12/cap$NN.json --check | tail -1
SAIDA=rec/t12; ROT=rec/t12/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t12/ensaio.py "$NN"; SAIDA=rec/t12/_ens; ROT=rec/t12/_ens/cap$NN.json; fi
CMD="node rec/record.mjs $ROT --out $SAIDA --name t12-cap$NN $ENSAIO > rec/t12/.rec-$NN.log 2>&1"
if ! flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t12/.rec-$NN.log
fi
python3 -I rec/t12/resumo.py "$NN" ${RAPIDO:+--ens} 2>&1 | head -120
