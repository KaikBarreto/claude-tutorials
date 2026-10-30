#!/usr/bin/env bash
# Monta o T0 "Boas-vindas à Dominex" depois das cenas renderizadas (rec/t0/t0-capNN.mp4):
# capítulos no palco (render_chapter.py), vinheta + vinhetas de capítulo + cartela + trilha (finish.py),
# legendas da aula inteira (legendas_aula.py) e conferência/entrega (entregar.py).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
LOCK=../../.heavy.lock
for c in ${CAPS:-00 01 02 03 04 05}; do
  python3 -I render_chapter.py "caps/cap$c.chapter.json" > "out/render_cap$c.log" 2>&1 || { echo "cap$c falhou"; tail -5 "out/render_cap$c.log"; exit 1; }
  echo "cap$c ok: $(tail -c 200 "out/render_cap$c.log" | tr '\r' '\n' | tail -1)"
done
python3 -I finish.py caps/T0.aula.json > out/finish.log 2>&1 || { echo "finish falhou"; tail -8 out/finish.log; exit 1; }
echo "finish ok: $(tail -1 out/finish.log)"
mkdir -p out/T0/legendas
(cd ../narracao && python3 -I legendas_aula.py ../edit/out/T0/capitulos.json ../edit/out/T0/proj/build/intro_v.mp4 ../edit/out/T0/legendas/aula_final)
flock "$LOCK" python3 -I entregar.py out/T0 "Domiflix T0 - Boas-vindas à Dominex" > out/entregar.log 2>&1 || { echo "entregar falhou"; tail -8 out/entregar.log; exit 1; }
tail -15 out/entregar.log
