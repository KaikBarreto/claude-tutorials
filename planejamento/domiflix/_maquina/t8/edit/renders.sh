#!/usr/bin/env bash
# T12 · renderiza os capítulos pedidos, um por vez (o render_chapter.py pega a trava sozinho); log em out/render_capNN.log
cd /home/claude/domiflix/t8/edit
export TUT_HOME=/home/claude/domiflix
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  python3 -I montar_cap.py "$NN" > out/montar_cap$NN.log 2>&1
  python3 -I render_chapter.py caps/cap$NN.chapter.json > out/render_cap$NN.log 2>&1
  echo "cap$NN exit $? $(tail -c 200 out/render_cap$NN.log | tr '\r' '\n' | tail -1)" >> out/renders_feitos.txt
done
