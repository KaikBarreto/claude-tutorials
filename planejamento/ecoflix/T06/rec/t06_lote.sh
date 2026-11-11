#!/usr/bin/env bash
# T06 · lote de capítulos, UM `flock` por capítulo (t06_rodar.sh), na ordem dada. Uso: bash rec/t06/t06_lote.sh [--ens] 00 01 02 ...
# Depois dos capítulos que mudam o banco (02, 05, 09, 10, 11) guarda o que o app gravou (t06_sementes.py capturar) em
# rec/t06/_ens/estado-capNN.txt, para conferir as sementes. Não edite este arquivo com um lote rodando (lição 45/75).
cd "$(dirname "$0")/../.."
MODO=""
[ "$1" = "--ens" ] && { MODO="--ens"; shift; }
: "${TUT_USER:=rafael@reciclavalemetais.example}"; export TUT_USER
[ -n "${TUT_SENHA:-}" ] || TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9'); export TUT_SENHA   # o falso aceita qualquer uma
for CAP in "$@"; do
  echo "##### cap$CAP $MODO $(date +%H:%M:%S)"
  bash rec/t06/t06_rodar.sh "$CAP" $MODO 2>&1 | tail -6
  case "$CAP" in 02|05|09|10|11) FAKE_URL=http://127.0.0.1:54306 python3 -I rec/t06/t06_sementes.py capturar > "rec/t06/_ens/estado-cap$CAP.txt" 2>&1 ;; esac
done
echo "##### fim do lote $(date +%H:%M:%S)"
