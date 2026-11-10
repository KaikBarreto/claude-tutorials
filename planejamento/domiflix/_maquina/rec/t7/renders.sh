#!/usr/bin/env bash
# T7 · renderiza em sequência os capítulos pedidos (render_um.sh NN: uma posse da trava por capítulo)
cd /home/claude/domiflix; export TUT_HOME=/home/claude/domiflix
for n in "$@"; do echo "=== [$(date +%H:%M:%S)] render $n"; bash rec/t7/render_um.sh "$n" 2>&1 | tail -12; done; echo "RENDERS FIM"
