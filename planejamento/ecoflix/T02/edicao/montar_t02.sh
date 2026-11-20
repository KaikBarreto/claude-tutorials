#!/bin/bash
# T02 · cadeia da montagem: render de cada capítulo, finish e legendas (cada etapa pesada pela fila, rec/fila.sh --prio 02).
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
for c in ${CAPS:-00 01 02 03 04 05 06 07 08 09 10 11 12 13}; do
  [ -s "out/cap$c/cap$c.mp4" ] && [ -z "${REFAZ:-}" ] && continue
  bash ../../rec/fila.sh --prio 02 -- nice -n 5 python3 -I render_chapter.py "caps/cap$c.chapter.json" > "out/render_cap$c.log" 2>&1 || { echo "cap$c falhou"; tail -5 "out/render_cap$c.log"; exit 1; }
  echo "cap$c ok $(date +%H:%M)"
done
bash ../../rec/fila.sh --prio 02 -- nice -n 5 python3 -I finish.py caps/T02.aula.json > out/finish.log 2>&1 || { echo "finish falhou"; tail -8 out/finish.log; exit 1; }
echo "finish ok: $(tail -1 out/finish.log)"
mkdir -p out/T02/legendas
(cd ../narracao && python3 -I legendas_aula.py ../edit/out/T02/capitulos.json ../edit/out/T02/proj/build/intro_v.mp4 ../edit/out/T02/legendas/aula_final --linha 32) > out/legendas.log 2>&1 || { echo "legendas falhou"; tail -5 out/legendas.log; }
ls -la out/T02/
