#!/usr/bin/env bash
# T14 · render dos capítulos, um por trava (`flock .heavy.lock nice -n 10`; outras aulas dividem a trava). Molde: t21/edit/render_todos.sh.
# Piso de disco do coordenador (06/11, "T14: render"): 1,3 GiB livres para começar cada render (abaixo disso para e avisa).
# uso: bash t14/edit/render_todos.sh NN [NN ...]   (log: t14/edit/out/render_capNN.log)
set -uo pipefail
cd /home/claude/domiflix/t14/edit
export TUT_HOME=/home/claude/domiflix
mkdir -p out
for NN in "$@"; do
  livre=$(df --output=avail -m /home/claude | tail -1)
  [ "$livre" -ge 1331 ] || { echo "PARADO: disco ${livre} MB (< 1,3 GiB) antes do cap$NN"; exit 4; }
  echo "--- [$(date +%H:%M:%S)] cap$NN (disco ${livre} MB)"
  flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 -I render_chapter.py caps/cap$NN.chapter.json > out/render_cap$NN.log 2>&1
  rc=$?
  tail -c 600 out/render_cap$NN.log | tr '\r' '\n' | grep -E "^ok|CHECAGEM|Error|rror|Traceback|camera" | tail -3
  [ "$rc" -eq 0 ] || { echo "cap$NN FALHOU (saída $rc)"; exit "$rc"; }
done
echo "--- [$(date +%H:%M:%S)] fim"; df -m /home/claude | tail -1
