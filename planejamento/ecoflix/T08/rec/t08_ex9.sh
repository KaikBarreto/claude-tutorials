#!/bin/bash
# T08 · exploração e9 (sem internet, queda de verdade): espera o lote do coordenador (PID dado) acabar, religa a 54308 no FAKE_NOW
# do cap12 DENTRO da fila e roda o explorador. Uso: bash rec/t08/t08_ex9.sh [PID_DO_LOTE] [eN]
cd /home/claude/ecoflix
P=${1:-}; E=${2:-e9}
if [ -n "$P" ]; then while [ -d "/proc/$P" ]; do sleep 20; done; fi
export FAKE_URL=http://127.0.0.1:54308 FAKE_NOW=2026-11-10T09:20:00-03:00 TUT_USER=rafael@reciclavalemetais.example E
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
bash /home/claude/ecoflix/rec/fila.sh --prio 08 -- bash -c '
  FAKE_PORT=54308 bash rec/run.sh fake | tail -1
  tr "\0" "\n" < /proc/$(cat rec/.runtime/fake54308.pid)/environ | grep -q "^FAKE_PORT=54308$" || { echo "instância 54308 não é a minha"; exit 3; }
  timeout 900 node rec/t08/explorar.mjs rec/t08/_ex/$E.json --out rec/t08/_ex/out${E#e} > rec/t08/_ex/$E.out 2>&1
'
echo "fim $E $(date +%H:%M:%S) rc=$?"
