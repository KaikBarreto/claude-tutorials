#!/usr/bin/env bash
# T06 · fila curta de capítulos (regra do coordenador de 11/11 18:46): "NN" = rápido + completo na mesma trava; "NN:r" = só o rápido.
# Uma trava por capítulo (t06_cap.sh). Uso: bash rec/t06/t06_lote3.sh 01 03 02:r ...   Não edite com a fila rodando.
cd "$(dirname "$0")/../.."
: "${TUT_USER:=rafael@reciclavalemetais.example}"; export TUT_USER
[ -n "${TUT_SENHA:-}" ] || TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9'); export TUT_SENHA   # o falso aceita qualquer uma
for IT in "$@"; do
  CAP="${IT%%:*}"; M=""; [ "$IT" != "$CAP" ] && M="--so-rapido"
  echo "##### cap$CAP $M $(date +%H:%M:%S)"
  bash rec/t06/t06_cap.sh "$CAP" $M 2>&1 | tail -5
  case "$CAP" in 02|05|09|10|11) FAKE_URL=http://127.0.0.1:54306 python3 -I rec/t06/t06_sementes.py capturar > "rec/t06/_ens/estado-cap$CAP.txt" 2>&1 ;; esac
done
echo "##### fim da fila $(date +%H:%M:%S)"
