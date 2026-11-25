#!/bin/bash
# T04 · espera a rodada em curso (final.log com "fim") e regrava a seguinte. Uso: bash rec/t04/t04_rodada3.sh NOME caps...
cd /home/claude/ecoflix
N=$1; shift
until grep -q "^fim" rec/t04/final.log 2>/dev/null; do sleep 15; done
mv rec/t04/final.log rec/t04/final_$N.log
TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc A-Za-z0-9 | head -c 14)" bash rec/t04/t04_final.sh "$@"
