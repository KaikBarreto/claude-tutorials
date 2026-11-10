#!/usr/bin/env bash
# T15 · render dos capítulos pedidos, NA ORDEM, uma trava por capítulo (flock + nice -n 10); log em out/render_capNN.log.
# uso: bash t15/edit/render_todos.sh 00 01 ... 09 09b 10 11 12   (para se o disco cair abaixo de 1,5 GiB ou se um capítulo falhar)
cd /home/claude/domiflix/t15/edit || exit 1
for n in "$@"; do
  case "$n" in *b) NN="$(printf '%02d' "$((10#${n%b}))")b" ;; *) NN=$(printf '%02d' "$((10#$n))") ;; esac
  livre=$(df -k --output=avail /home/claude | tail -1)
  if [ "$livre" -lt $((1536 * 1024)) ]; then echo "DISCO BAIXO antes do cap$NN ($((livre / 1024)) MB): paro"; exit 3; fi
  flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I render_chapter.py "caps/cap$NN.chapter.json" > "out/render_cap$NN.log" 2>&1
  rc=$?
  echo "cap$NN rc=$rc $(date +%T) $(tail -1 "out/render_cap$NN.log" | tr '\r' '\n' | tail -1 | cut -c1-160)"
  [ $rc -eq 0 ] || exit $rc
done
