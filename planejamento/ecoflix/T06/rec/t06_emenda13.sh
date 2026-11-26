#!/bin/bash
# T06 remendo do cap13 L10: emenda a frase nova (voz recebida) no take do cap13 e refaz palavras/legendas (proc.py). Pela fila prio 6.
set -u
cd /home/claude/ecoflix/t06/narracao
python3 -I emendar.py recebido_1.60.22/cap13_frase.mp3 > /dev/shm/t06_emendar.log 2>&1; echo "emendar exit $?" >> /dev/shm/t06_emendar.log
[ -f emendas/cap13_v2.wav ] && python3 -I proc.py 13=emendas/cap13_v2.wav >> /dev/shm/t06_emendar.log 2>&1; echo "proc exit $?" >> /dev/shm/t06_emendar.log
echo fim >> /dev/shm/t06_emendar.log
