#!/usr/bin/env bash
# Folhas de revisão do vídeo INTEIRO (aula final, capítulo ou remendo): um quadro a cada 3 s (6x5 por folha = 90 s), com o tempo do
# vídeo em cada quadro. Obrigatória antes de entregar (docs/07-conferencia.md): olhe todas as folhas, do começo ao fim.
#   uso: bash folhas3s.sh <video.mp4> <pasta_saida> [passo_s=3] [inicio_s=0] [fim_s=fim]      (TILE=6x5 muda a grade)
#   pesado numa aula longa (decodifica tudo): rode sob `flock $TUT_HOME/.heavy.lock nice -n 10 bash folhas3s.sh ...`
# `fps=1/PASSO:round=up`: com o arredondamento padrão (near) o quadro mostrado era o de ~meio passo DEPOIS do tempo escrito (1,5 s numa
# folha de 3 s); com `up` o quadro é o do próprio tempo do rótulo (conferido no cap. 12 do T15). Vídeo vertical (9:16): quadros 180x320
# e grade 10x3 (os mesmos 30 quadros por folha).
set -euo pipefail
MP4="${1:?uso: folhas3s.sh <video.mp4> <pasta_saida> [passo_s] [inicio_s] [fim_s]}"; OUTD="${2:?pasta de saída}"
PASSO="${3:-3}"; INI="${4:-0}"; FIM="${5:-}"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FONTE=""   # Montserrat do kit: da área de trabalho (<TUT_HOME>/kit, pela posição do script em <TUT_HOME>/<tutorial>/edit) ou da skill
for f in ${TUT_HOME:+"$TUT_HOME/kit/fonts/Montserrat-700.ttf"} "$AQUI/../../kit/fonts/Montserrat-700.ttf" "$AQUI/../kit/fonts/Montserrat-700.ttf"; do
  [ -f "$f" ] && { FONTE="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"; break; }
done
[ -n "$FONTE" ] || { echo "fonte Montserrat-700.ttf não encontrada (kit/fonts do TUT_HOME)"; exit 1; }
mkdir -p "$OUTD"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MP4")
[ -n "$FIM" ] || FIM="$DUR"
IFS=, read -r LARG ALT < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$MP4")
if [ "$ALT" -gt "$LARG" ]; then QUADRO="180:320"; GRADE="${TILE:-10x3}"; else QUADRO="320:180"; GRADE="${TILE:-6x5}"; fi
VF="fps=1/${PASSO}:round=up,scale=${QUADRO},drawtext=fontfile=${FONTE}:text='%{pts\\:hms\\:${INI}}':x=4:y=4:fontsize=15:fontcolor=white:box=1:boxcolor=black@0.6,tile=${GRADE}:padding=2:color=white"
nice -n 15 ffmpeg -v error -y -ss "$INI" -to "$FIM" -i "$MP4" -vf "$VF" -q:v 3 "$OUTD/folha_%02d.jpg"
ls "$OUTD"
