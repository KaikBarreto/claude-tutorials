#!/usr/bin/env bash
# Folhas de revisão de uma aula final: um quadro a cada 3 s (6x5 por folha = 90 s), com o tempo do vídeo em cada quadro.
# Cópia do folhas3s.sh do coordenador com `fps=...:round=up`: com o arredondamento padrão (near) o quadro mostrado é o de ~meio passo
# DEPOIS do tempo escrito (1,5 s numa folha de 3 s); com `up` o quadro é o do próprio tempo do rótulo (conferido no cap. 12 do T15).
# uso: folhas3s.sh <aula_final.mp4> <pasta_saida> [passo_s=3] [inicio_s=0] [fim_s=fim]
set -euo pipefail
MP4="${1:?mp4}"; OUTD="${2:?pasta}"; PASSO="${3:-3}"; INI="${4:-0}"; FIM="${5:-}"
FONTE=/home/claude/domiflix/kit/fonts/Montserrat-700.ttf
mkdir -p "$OUTD"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MP4")
[ -n "$FIM" ] || FIM="$DUR"
VF="fps=1/${PASSO}:round=up,scale=320:180,drawtext=fontfile=${FONTE}:text='%{pts\\:hms\\:${INI}}':x=4:y=4:fontsize=15:fontcolor=white:box=1:boxcolor=black@0.6,tile=${TILE:-6x5}:padding=2:color=white"
nice -n 15 ffmpeg -v error -y -ss "$INI" -to "$FIM" -i "$MP4" -vf "$VF" -q:v 3 "$OUTD/folha_%02d.jpg"
ls "$OUTD"
