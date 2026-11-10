#!/usr/bin/env bash
# T19 · render de todos os capítulos, um por vez, cada um sob a trava (o render_chapter.py pega flock + nice sozinho); log em out/render_capNN.log
cd /home/claude/domiflix/t19/edit
export TUT_HOME=/home/claude/domiflix
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  livre=$(df -k --output=avail /home/claude | tail -1)
  if [ "$livre" -lt $((1536 * 1024)) ]; then echo "DISCO BAIXO: paro em cap$NN" >> out/render_fim.log; exit 3; fi
  python3 -I render_chapter.py caps/cap$NN.chapter.json > out/render_cap$NN.log 2>&1
  echo "cap$NN exit $?" >> out/render_fim.log
done
echo FIM >> out/render_fim.log
