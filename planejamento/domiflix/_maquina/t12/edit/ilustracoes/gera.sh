#!/usr/bin/env bash
# T12 · ilustrações dos caps. 5 (QR do T3 retemporizado) e 10 (dois cartões), uma trava por tarefa
cd /home/claude/domiflix/t12/edit
export TUT_HOME=/home/claude/domiflix
python3 -I ilustracoes/retempo_qr.py /home/claude/domiflix/t3/edit/out/ilu_qr out/ilu_qr_cap05 8.6 1.2
flock $TUT_HOME/.heavy.lock nice -n 10 python3 -I ilustracoes/ilustra_portais.py out/ilu_portais_cap10 21.1
