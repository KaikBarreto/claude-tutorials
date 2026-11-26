#!/bin/bash
# T12 remendo do cap17: grava o cap16 (rápido, só para o estado) e deixa a semente apos-cap16 (rec/mundo/seeds-extra/t12/apos-cap16.json).
# Não toca nas gravações finais de rec/t12/. Pela fila prio 12.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54312 FAKE_PORT=54312 TUT_USER=rafael@reciclavalemetais.example
export FAKE_NOW=2026-11-10T07:00:00-03:00
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
bash rec/fila.sh --prio 12 -- bash -c '
  bash rec/run.sh fake | tail -1
  rm -rf /dev/shm/t12_sem16; mkdir -p /dev/shm/t12_sem16
  timeout 900 node rec/record.mjs rec/t12/cap16.json --preset ultrafast --crf 30 --out /dev/shm/t12_sem16 > /dev/shm/t12_sem16/rec.out 2>&1
  echo "gravou cap16 falhos=$(grep -c FALHOU /dev/shm/t12_sem16/rec.out)"
  python3 -I rec/t12/t12_semente.py apos-cap16
  bash rec/run.sh down >/dev/null 2>&1
'
echo fim
