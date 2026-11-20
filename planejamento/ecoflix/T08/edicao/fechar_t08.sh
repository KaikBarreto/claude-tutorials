#!/bin/bash
# T08 1.60.18 · fecha a aula depois da gravação final (04/07/11) e do render das ilustrações:
# refaz as 2 ilustrações cuja voz mudou (ilu04, ilu11_comprovante), specs, câmera, render dos capítulos, finish, legendas.
cd /home/claude/ecoflix/t08/edit
[ -n "${GRAVA:-}" ] && bash ../../rec/t08/t08_final.sh $GRAVA   # GRAVA="11": regrava antes de montar
rm -f out/ilus/ilu04_entrada_saida.mp4 out/ilus/ilu11_comprovante.mp4
bash render_ilus_v3.sh > out/ilus/render2.log 2>&1
python3 -I specs_ilus.py > out/fechar.log 2>&1
python3 -I montar_cap.py 00 01 02 03 04 05 06 07 08 09 10 11 12 13 >> out/fechar.log 2>&1
nice -n 10 python3 -I auditar_camera.py >> out/fechar.log 2>&1
bash montar_t08.sh >> out/fechar.log 2>&1
echo "FECHAR FIM $(date +%H:%M)" >> out/fechar.log
