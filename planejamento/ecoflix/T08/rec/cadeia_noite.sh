#!/bin/bash
# 19/11 noite, depois do reinício do contêiner: tudo em SÉRIE (a varredura roda o record.mjs fora da fila e, junto com a
# gravação final, deu atrasos de até 16 s no cap02). 1) gravação final 1600x900; 2) ilustrações 16:9; 3) resto da varredura.
cd /home/claude/ecoflix
curl -s -o /dev/null http://127.0.0.1:8080/ || bash rec/run.sh app >/dev/null 2>&1
echo "== 1600x900 (série) $(date +%H:%M)" >> rec/t08/final.log
bash rec/t08/t08_final.sh 01 02 03 06 08 09 10 11 12 13
REFAZ=1 bash t08/edit/render_ilus_v3.sh > t08/edit/out/ilus/render.log 2>&1
bash rec/varredura/tudo.sh t22 t25 t26 t27
echo "cadeia fim $(date +%H:%M)" >> rec/t08/final.log
