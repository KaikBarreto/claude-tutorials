#!/usr/bin/env bash
# T21 · grava UM capítulo (ensaio rápido com --ens, ou a gravação com os tempos da fala) na instância da T21 (porta 54321), sob a
# trava pesada (uma trava por capítulo), e imprime o resumo. Uso: bash rec/t21/t21_rodar.sh NN|2b [--ens]
#   saídas: --ens em /dev/shm/t21ens/ (actions/telemetry copiados para rec/t21/_ens/); sem --ens em /dev/shm/t21rec/ (MP4 grande fora do disco; actions/telemetry copiados para rec/t21/)
# TUT_USER e TUT_SENHA vêm do ambiente (a senha nunca vai para arquivo nem log).
set -euo pipefail
cd /home/claude/ecoflix
N="$1"; MODO="${2:-}"
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54321
: "${TUT_USER:?defina TUT_USER}"; : "${TUT_SENHA:?defina TUT_SENHA}"
PID="$(cat rec/.runtime/fake54321.pid)"
tr '\0' '\n' < "/proc/$PID/environ" | grep -q '^FAKE_PORT=54321$' || { echo "a instância 54321 não é a da T21"; exit 3; }
tr '\0' '\n' < "/proc/$PID/environ" | grep -q "^FAKE_NOW=$FAKE_NOW$" || { echo "FAKE_NOW da instância diferente"; exit 3; }
case "$N" in *b) NOME="cap$(printf %02d "${N%b}")b" ;; *) NOME="cap$(printf %02d "$N")" ;; esac
if [ "$MODO" = "--ens" ]; then
  python3 -I rec/t21/ensaio.py "$N"
  mkdir -p /dev/shm/t21ens
  flock .heavy.lock timeout 900 node rec/record.mjs "rec/t21/_ens/$NOME.json" --rapido --no-encode --out /dev/shm/t21ens > "rec/t21/_ens/.$NOME.out" 2>&1 || echo "record saiu $?"
  tail -3 "rec/t21/_ens/.$NOME.out"
  cp /dev/shm/t21ens/t21-$NOME.actions.json /dev/shm/t21ens/t21-$NOME.telemetry.json rec/t21/_ens/
  python3 -I rec/t21/resumo.py "$N" --ens
  grep -c "SEM ALVO" "rec/t21/_ens/t21-$NOME.actions.json" || true
else
  mkdir -p /dev/shm/t21rec
  flock .heavy.lock timeout 900 node rec/record.mjs "rec/t21/$NOME.json" --out /dev/shm/t21rec > "rec/t21/.$NOME.out" 2>&1 || echo "record saiu $?"
  tail -3 "rec/t21/.$NOME.out"
  cp /dev/shm/t21rec/t21-$NOME.actions.json /dev/shm/t21rec/t21-$NOME.telemetry.json rec/t21/
  python3 -I rec/t21/resumo.py "$N"
  grep -c "SEM ALVO" "rec/t21/t21-$NOME.actions.json" || true
fi
