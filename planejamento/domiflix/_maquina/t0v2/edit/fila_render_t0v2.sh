#!/usr/bin/env bash
# Renderiza os capítulos 16:9 e 9:16 do T0 v2 (cada render pega a trava sozinho). uso: fila_render_t0v2.sh 01 02 ...
cd "$(dirname "$0")" || exit 1
for n in "$@"; do
  python3 -I render_chapter.py caps/cap$n.chapter.json > out/render_cap$n.log 2>&1; echo "16x9 cap$n exit $?"
  python3 -I render_chapter_vertical.py caps/cap$n.9x16.chapter.json > out/render_cap${n}_9x16.log 2>&1; echo "9x16 cap$n exit $?"
  python3 -I compor_ilus_vertical_multi.py $n >> out/render_cap${n}_9x16.log 2>&1; echo "ilus9x16 cap$n exit $?"
done; echo FIM
