#!/usr/bin/env bash
# T22 · render dos capítulos, um por trava (`flock .heavy.lock nice -n 10`; o T14 divide a trava). O áudio de cada capítulo vai para
# /dev/shm/t22_caps (o disco fica para o finish: MP4s ~0,35 MB/s no disco, WAVs ~0,19 MB/s na memória; o sidecar aponta para lá).
# uso: bash t22/edit/render_todos.sh NN [NN ...]   (log: t22/edit/out/render_capNN.log)
set -uo pipefail
cd /home/claude/domiflix/t22/edit
mkdir -p out /dev/shm/t22_caps
for NN in "$@"; do
  livre=$(df --output=avail -m /home/claude | tail -1)
  [ "$livre" -ge 1536 ] || { echo "PARADO: disco ${livre} MB (< 1,5 GiB) antes do cap$NN"; exit 4; }
  echo "--- [$(date +%H:%M:%S)] cap$NN (disco ${livre} MB)"
  flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 -I render_chapter.py caps/cap$NN.chapter.json \
        --wav /dev/shm/t22_caps/cap$NN.wav > out/render_cap$NN.log 2>&1
  rc=$?
  tail -c 600 out/render_cap$NN.log | tr '\r' '\n' | grep -E "^ok|CHECAGEM|Error|rror|Traceback|camera" | tail -3
  [ "$rc" -eq 0 ] || { echo "cap$NN FALHOU (saída $rc)"; exit "$rc"; }
done
echo "--- [$(date +%H:%M:%S)] fim"; df -m /home/claude | tail -1
