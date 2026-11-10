#!/usr/bin/env bash
# T18 · Uso: rec/t18/rodar.sh NN [--ensaio] [--rapido]
#   NN         capítulo (0 a 15): gera o roteiro do robô, valida (--check), grava sob UMA trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t18/_ens/): acha seletor errado; não mede o ritmo
# Instância própria do Supabase falso do agente B (porta 54322, `FAKE_PORT=54322 FAKE_NOW=... rec/run.sh fake`); o app (8080) é compartilhado.
# QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` com `nice -n 10`, e UMA trava por capítulo (regra de 31/10).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54322 FAKE_NOW="2026-11-11T11:00:00-03:00"
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
python3 -I rec/t18/gerar.py "$NN" | tail -3
node rec/record.mjs rec/t18/cap$NN.json --check | tail -1
SAIDA=rec/t18; ROT=rec/t18/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t18/ensaio.py "$NN"; SAIDA=rec/t18/_ens; ROT=rec/t18/_ens/cap$NN.json; fi
CMD="node rec/record.mjs $ROT --out $SAIDA --name t18-cap$NN $ENSAIO > rec/t18/.rec-$NN.log 2>&1"
if ! flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t18/.rec-$NN.log
fi
python3 -I rec/t18/resumo.py "$NN" ${RAPIDO:+--ens} 2>&1 | head -120
