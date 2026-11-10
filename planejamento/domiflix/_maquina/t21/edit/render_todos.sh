#!/usr/bin/env bash
# T21 · render dos capítulos, um por trava (`flock .heavy.lock nice -n 10`; o T17 divide a trava). Molde: t22/edit/render_todos.sh.
# Piso de disco do coordenador (06/11): 1,3 GiB livres para começar cada render. Depois do cap07, na trava seguinte, recorta do cap07
# renderizado o trecho do interruptor (janela em repouso, 1587x992) que o recap (cap10, L3) reaproveita: assets/ilu_cap10_interruptor.mp4.
# uso: bash t21/edit/render_todos.sh NN [NN ...]   (log: t21/edit/out/render_capNN.log)
set -uo pipefail
cd /home/claude/domiflix/t21/edit
export TUT_HOME=/home/claude/domiflix
mkdir -p out
for NN in "$@"; do
  livre=$(df --output=avail -m /home/claude | tail -1)
  [ "$livre" -ge 1331 ] || { echo "PARADO: disco ${livre} MB (< 1,3 GiB) antes do cap$NN"; exit 4; }
  if [ "$NN" = 10 ] && [ ! -s assets/ilu_cap10_interruptor.mp4 ]; then echo "PARADO: falta assets/ilu_cap10_interruptor.mp4 (renderize o cap07 antes)"; exit 6; fi
  echo "--- [$(date +%H:%M:%S)] cap$NN (disco ${livre} MB)"
  flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 -I render_chapter.py caps/cap$NN.chapter.json > out/render_cap$NN.log 2>&1
  rc=$?
  tail -c 600 out/render_cap$NN.log | tr '\r' '\n' | grep -E "^ok|CHECAGEM|Error|rror|Traceback|camera" | tail -3
  [ "$rc" -eq 0 ] || { echo "cap$NN FALHOU (saída $rc)"; exit "$rc"; }
  if [ "$NN" = 07 ]; then
    # trecho do interruptor (cap07 L2, "No Hotel Mirante do Mar, ela está ligada": gesto em 22,26 s) na janela em repouso do palco
    flock /home/claude/domiflix/.heavy.lock nice -n 10 ffmpeg -v error -y -ss 22.0 -t 2.8 -i out/cap07/cap07.mp4 -an \
      -vf "crop=1587:992:166:44,format=yuv444p" -c:v libx264 -preset slow -crf 12 -pix_fmt yuv444p assets/ilu_cap10_interruptor.mp4 \
      && echo "ok assets/ilu_cap10_interruptor.mp4 ($(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/ilu_cap10_interruptor.mp4) s)"
  fi
done
echo "--- [$(date +%H:%M:%S)] fim"; df -m /home/claude | tail -1
