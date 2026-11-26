#!/bin/bash
# T01 · roda a captura do papel real (rec/t01/papel.json) pela fila, instância 54311. Saída: /dev/shm/t01_papel e rec/t01/papel.log
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54311 FAKE_PORT=54311 FAKE_NOW=2026-11-10T08:30:00-03:00 TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
mkdir -p /dev/shm/t01_papel
bash rec/fila.sh --prio 1 -- bash -c '
  bash rec/run.sh fake | tail -1
  timeout 900 node rec/record.mjs rec/t01/papel.json --rapido --preset ultrafast --crf 30 --out /dev/shm/t01_papel > rec/t01/papel.log 2>&1
  bash rec/run.sh down >/dev/null 2>&1'
python3 -I rec/t01/t01_papel.py extrair >> rec/t01/papel.log 2>&1
echo "papel fim $(date +%T)" >> rec/t01/papel.log
