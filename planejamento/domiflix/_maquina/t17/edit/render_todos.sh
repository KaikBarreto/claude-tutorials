#!/usr/bin/env bash
# T17 · render dos capítulos, um por trava (`flock .heavy.lock nice -n 10`; outras aulas dividem a trava). Molde: t21/edit/render_todos.sh.
# Piso de disco do coordenador ("T17: render", 06/11 12:0x): 1,3 GiB livres para COMEÇAR cada render. Abaixo disso o script espera
# (confere de 10 em 10 min) e não para de vez: o coordenador entrega e limpa o T14 logo que ele terminar.
# Re-executável: capítulo com out/capNN/capNN.mp4 mais novo que o caps/capNN.chapter.json é pulado (TUT_REFAZER=1 refaz).
# uso: bash t17/edit/render_todos.sh NN [NN ...]   (log: t17/edit/out/render_capNN.log)
set -uo pipefail
cd /home/claude/domiflix/t17/edit
export TUT_HOME=/home/claude/domiflix
mkdir -p out
PISO=1331   # MB (1,3 GiB)
for NN in "$@"; do
  if [ -z "${TUT_REFAZER:-}" ] && [ -s "out/cap$NN/cap$NN.mp4" ] && [ "out/cap$NN/cap$NN.mp4" -nt "caps/cap$NN.chapter.json" ]; then
    echo "--- cap$NN já renderizado (pulo)"; continue
  fi
  while :; do
    livre=$(df --output=avail -m /home/claude | tail -1)
    [ "$livre" -ge "$PISO" ] && break
    echo "--- [$(date +%H:%M:%S)] disco ${livre} MB (< 1,3 GiB) antes do cap$NN: espero 10 min"
    sleep 600
  done
  echo "--- [$(date +%H:%M:%S)] cap$NN (disco ${livre} MB)"
  flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 -I render_chapter.py caps/cap$NN.chapter.json > out/render_cap$NN.log 2>&1
  rc=$?
  echo "    [$(date +%H:%M:%S)] fim do cap$NN (saída $rc)"
  tail -c 600 out/render_cap$NN.log | tr '\r' '\n' | grep -E "^ok|CHECAGEM|Error|rror|Traceback|camera" | tail -3
  [ "$rc" -eq 0 ] || { echo "cap$NN FALHOU (saída $rc)"; exit "$rc"; }
done
echo "--- [$(date +%H:%M:%S)] fim"; df -m /home/claude | tail -1
