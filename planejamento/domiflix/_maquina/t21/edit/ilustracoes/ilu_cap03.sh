#!/usr/bin/env bash
# T21 cap03: gera a ilustração (PNG em /dev/shm) e codifica em MP4 no disco (assets/ilu_cap03_qr.mp4, yuv444p), sob a trava.
set -euo pipefail
export TUT_HOME=/home/claude/domiflix
D=/dev/shm/t21_render/ilu_qr
rm -rf /dev/shm/t21_render/ilu_qr /dev/shm/t21_render/ilu_qr_so
mkdir -p "$D"
python3 -I /home/claude/domiflix/t21/edit/ilustracoes/ilustra_qr_wa.py "$D" 6.0
ffmpeg -v error -y -framerate 30 -i "$D/%04d.png" -vf "format=yuv444p" -c:v libx264 -preset slow -crf 12 -pix_fmt yuv444p /home/claude/domiflix/t21/edit/assets/ilu_cap03_qr.mp4
rm -rf /dev/shm/t21_render/ilu_qr
ls -la /home/claude/domiflix/t21/edit/assets/
