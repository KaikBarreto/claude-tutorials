#!/usr/bin/env bash
# Junta vídeo + mix final. uso: bash kit/mux.sh <projeto> [saida.mp4]
set -euo pipefail
PROJ="${1}"; OUT="${2:-$PROJ/out/aula_final.mp4}"
ffmpeg -v error -y -i "$PROJ/out/video.mp4" -i "$PROJ/build/mix.wav" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,size,bit_rate -of default=nw=1 "$OUT"
