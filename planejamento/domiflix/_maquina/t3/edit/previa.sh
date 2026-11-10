#!/usr/bin/env bash
# Prévia de um capítulo: folha de quadros nos tempos pedidos + cópia leve (< 30 MiB) com a narração.
# uso: t3/edit/previa.sh <capNN> "t1 t2 t3 ..."
set -euo pipefail
N="${1:?capítulo}"; TS="${2:?tempos}"
D="/home/claude/domiflix/t3/edit/out/$N"; IN="$D/$N.mp4"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height -show_entries format=duration -of compact "$IN"
F="$D/folha"; mkdir -p "$F"; rm -f "${F:?}"/q_*.jpg
i=0; for t in $TS; do i=$((i+1)); ffmpeg -v error -y -ss "$t" -i "$IN" -frames:v 1 -vf "scale=640:360,drawtext=text='$t s':x=8:y=8:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6" "$F/q_$(printf %02d $i).jpg"; done
ffmpeg -v error -y -pattern_type glob -i "$F/q_*.jpg" -vf "tile=4x$(( (i+3)/4 )):padding=4:color=black" -frames:v 1 "$D/$N.folha_previa.jpg"
ffmpeg -v error -y -i "$IN" -i "$D/$N.wav" -map 0:v:0 -map 1:a:0 -c:v libx264 -preset veryfast -crf 25 -pix_fmt yuv420p -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 128k -shortest -movflags +faststart "$D/${N}_previa.mp4"
ls -la "$D/${N}_previa.mp4" "$D/$N.folha_previa.jpg"
