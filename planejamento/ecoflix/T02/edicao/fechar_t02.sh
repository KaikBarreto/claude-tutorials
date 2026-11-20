#!/bin/bash
# T02 1.60.x · fecha a aula depois da gravação final e do render das ilustrações (molde: t08/edit/fechar_t08.sh):
# specs das ilustrações, capítulos montados, câmera auditada, render dos capítulos que faltam (pela fila), finish e legendas.
cd /home/claude/ecoflix/t02/edit
python3 -I specs_ilus.py > out/fechar.log 2>&1
python3 -I montar_cap.py 00 01 02 03 04 05 06 07 08 09 10 11 12 13 >> out/fechar.log 2>&1 || { echo "MONTAR FALHOU" >> out/fechar.log; exit 1; }
nice -n 10 python3 -I auditar_camera.py >> out/fechar.log 2>&1
for c in ${REFAZER:-}; do rm -f "/home/claude/ecoflix/t02/edit/out/cap$c/cap$c.mp4"; done   # REFAZER="02 ...": capítulos cujo specs mudou
bash montar_t02.sh >> out/fechar.log 2>&1
echo "FECHAR FIM $(date +%H:%M)" >> out/fechar.log
