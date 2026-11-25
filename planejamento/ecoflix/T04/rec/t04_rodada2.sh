#!/bin/bash
# T04 · espera a gravação em curso (final.log com "fim") e regrava a 2a rodada. Uso: bash rec/t04/t04_rodada2.sh caps...
cd /home/claude/ecoflix
until grep -q "^fim" rec/t04/final.log 2>/dev/null; do sleep 15; done
mv rec/t04/final.log rec/t04/final_a.log
TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc A-Za-z0-9 | head -c 14)" bash rec/t04/t04_final.sh "$@"
