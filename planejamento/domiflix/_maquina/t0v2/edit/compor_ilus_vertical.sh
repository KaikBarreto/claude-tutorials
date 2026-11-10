#!/usr/bin/env bash
# O render vertical com a tela real do celular não desenha "illustrations" (celular_vertical.py as desliga). Aqui a ilustração vertical
# (1080x1920, já com palco e painel) cobre o começo do capítulo já renderizado: troca os quadros de 0 a DUR s, sem mexer no áudio.
# uso: compor_ilus_vertical.sh <capNN_9x16 (pasta em out/)> <capNN.mp4 dentro dela> <ilustração.mp4> <DUR>
set -euo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/out/$1"; V="$D/$2"; I="$3"; DUR="$4"
[ -f "$D/.sem_ilus_$2" ] || cp -l "$V" "$D/.sem_ilus_$2"
nice -n 10 flock "$(dirname "$(dirname "$D")")/../../.heavy.lock" ffmpeg -y -loglevel error -i "$D/.sem_ilus_$2" -i "$I" \
  -filter_complex "[0:v][1:v]overlay=0:0:enable='lt(t,$DUR)':eof_action=pass[v]" -map "[v]" -map 0:a? -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -c:a copy -movflags +faststart "$D/.novo_$2"
mv "$D/.novo_$2" "$V"; echo "ok $V"
