#!/bin/bash
# T20 · sementes + ensaio rapido dos caps 3 4 10, com PORTAL_SENHA aleatoria so no ambiente deste processo.
set -u
cd /home/claude/ecoflix
export PORTAL_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
python3 -I rec/t20/t20_sementes.py
bash rec/t20/t20_fila.sh --rapido "$@"
