#!/usr/bin/env bash
# T20 · render dos capítulos pedidos, NA ORDEM, uma trava por capítulo (flock + nice -n 10); log em out/render_capNN.log.
# uso: bash t20/edit/render_todos.sh 00 01 02 ...   (para se o disco cair abaixo de 1,5 GB)
cd /home/claude/domiflix/t20/edit || exit 1
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  livre=$(df -k --output=avail /home/claude | tail -1)
  if [ "$livre" -lt $((1536 * 1024)) ]; then echo "DISCO BAIXO antes do cap$NN ($((livre / 1024)) MB): paro"; exit 3; fi
  flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I render_chapter.py "caps/cap$NN.chapter.json" > "out/render_cap$NN.log" 2>&1
  rc=$?
  echo "cap$NN rc=$rc $(tail -1 "out/render_cap$NN.log" | cut -c1-160)"
  [ $rc -eq 0 ] || exit $rc
done
