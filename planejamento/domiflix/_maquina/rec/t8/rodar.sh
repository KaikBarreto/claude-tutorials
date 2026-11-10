#!/usr/bin/env bash
# T8 · Uso: rec/t8/rodar.sh NN [--ensaio] [--rapido] [--seed]
#   NN         capítulo (0 a 15): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t8/_ens/): acha seletor errado e fecha o estado; não mede o ritmo
#   --seed     depois da gravação, na MESMA trava, grava seeds-extra/t8/apos-capNN.json (snap.mjs diff NN)
# Instância própria do Supabase falso do agente E (porta 54325, `FAKE_PORT=54325 FAKE_NOW=... rec/run.sh fake`); o app (8080) é compartilhado.
# QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` com `nice -n 10`, e UMA trava por capítulo.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54325 FAKE_NOW="2026-11-03T09:00:00-03:00"
NN=$(printf '%02d' "$((10#$1))")
shift
ENSAIO=""; SEED=""; RAPIDO=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    --seed) SEED=1 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
python3 -I rec/t8/gerar.py "$NN" | tail -3
node rec/record.mjs rec/t8/cap$NN.json --check | tail -1
SAIDA=rec/t8; ROT=rec/t8/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t8/ensaio.py "$NN"; SAIDA=rec/t8/_ens; ROT=rec/t8/_ens/cap$NN.json; fi
CMD="node rec/record.mjs $ROT --out $SAIDA --name t8-cap$NN $ENSAIO > rec/t8/.rec-$NN.log 2>&1; rc=\$?"
if [ -n "$SEED" ]; then CMD="$CMD; node rec/t8/snap.mjs diff $((10#$NN)) > rec/t8/.snap-$NN.log 2>&1"; fi
CMD="$CMD; exit \$rc"
if ! flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t8/.rec-$NN.log
fi
python3 -I rec/t8/resumo.py "$NN" ${RAPIDO:+--ens} 2>&1 | head -140
if [ -n "$SEED" ]; then echo "--- snapshot:"; tail -8 rec/t8/.snap-$NN.log; fi
