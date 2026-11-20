#!/bin/bash
# espera a cadeia da noite (varredura) terminar e grava o final de 04, 07 e 11 sem concorrência
cd /home/claude/ecoflix
until grep -q "cadeia fim" rec/t08/final.log; do sleep 30; done
bash rec/t08/t08_final.sh 04 07 11
