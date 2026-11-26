#!/bin/bash
# T05 · renderiza as cenas de Windows (t05/windows/<id>.json, já com os tempos da voz real e a página = gravação do robô), uma por vez, pela fila (prio 05).
# Saída: rec/t05/t05-<id>.{mp4,telemetry.json,actions.json} (renderiza em /dev/shm/t05_rec e move). Uso: bash rec/t05/t05_cenas.sh id1 id2 ...   Log: rec/t05/cenas.log
set -u
export TUT_HOME=/home/claude/ecoflix CENA_WIN_CACHE=/dev/shm/cena-windows
S=/home/claude/claude-tutorials; W=$TUT_HOME/t05/windows
mkdir -p /dev/shm/t05_rec
for n in "$@"; do
  DISCO=$(df -m / | awk 'NR==2{print $4}'); SHM=$(df -m /dev/shm | awk 'NR==2{print $4}')
  if [ "$DISCO" -lt 800 ] || [ "$SHM" -lt 1200 ]; then echo "$n PARADO: / ${DISCO} MB, /dev/shm ${SHM} MB" >> $TUT_HOME/rec/t05/cenas.log; exit 4; fi
  ini=$(date +%s)
  (cd $W && bash $TUT_HOME/rec/fila.sh --prio 05 -- node $S/ferramentas/windows/cena_windows.cjs $n.json /dev/shm/t05_rec/t05-$n.mp4 > $TUT_HOME/rec/t05/.cena_$n.out 2>&1)
  rc=$?
  for e in mp4 telemetry.json actions.json; do mv -f /dev/shm/t05_rec/t05-$n.$e $TUT_HOME/rec/t05/ 2>/dev/null; done
  echo "$n rc=$rc $(( $(date +%s) - ini )) s $(tail -1 $TUT_HOME/rec/t05/.cena_$n.out | cut -c1-150)" >> $TUT_HOME/rec/t05/cenas.log
done
echo fim >> $TUT_HOME/rec/t05/cenas.log
