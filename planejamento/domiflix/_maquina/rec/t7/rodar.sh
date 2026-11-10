#!/usr/bin/env bash
# T7 · Uso: rec/t7/rodar.sh NN [--ensaio] [--seed]
#   NN         capítulo (0 a 14): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t7/_ens/): acha seletor errado e fecha o estado; não mede o ritmo
#   --seed     depois da gravação, na MESMA trava, grava seeds-extra/t7/apos-capNN.json (snap.mjs diff NN)
# Instância própria do Supabase falso do agente A (porta 54321, `FAKE_PORT=54321 rec/run.sh fake`); o app (8080) é compartilhado.
# QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` com `nice -n 10` (regra do coordenador, sem exceção).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL="${FAKE_URL:-http://127.0.0.1:54321}" FAKE_NOW="2026-11-11T08:50:00-03:00"
NN=$(printf '%02d' "$((10#$1))")
case "$NN" in 11|12) export APP_ORIGIN=https://www.dominex.app ;; esac   # link do cliente / Copiar Link: domínio real na tela
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
python3 -I rec/t7/gerar.py "$NN" | tail -3
node rec/record.mjs rec/t7/cap$NN.json --check | tail -1
# a foto do checklist vive na memória do falso: se ele reiniciou, sobe de novo (só quando o capítulo parte de um estado com a foto)
python3 -I rec/t7/fotos.py "$NN" 2>&1 | tail -2
SAIDA=rec/t7; ROT=rec/t7/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t7/ensaio.py "$NN"; SAIDA=rec/t7/_ens; ROT=rec/t7/_ens/cap$NN.json; fi
CMD="node rec/record.mjs $ROT --out $SAIDA --name t7-cap$NN $ENSAIO > rec/t7/.rec-$NN.log 2>&1; rc=\$?"
if [ -n "$SEED" ]; then CMD="$CMD; node rec/t7/snap.mjs diff $((10#$NN)) > rec/t7/.snap-$NN.log 2>&1"; fi
CMD="$CMD; exit \$rc"
if ! flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t7/.rec-$NN.log
fi
python3 -I rec/t7/resumo.py "$NN" ${RAPIDO:+--ens} 2>&1 | head -120
if [ -n "$SEED" ]; then echo "--- snapshot:"; tail -6 rec/t7/.snap-$NN.log; fi
