#!/usr/bin/env bash
# Prévia vertical (~20 s) do T0 v2: vinheta, vinheta de capítulo, cena ilustrada (cap04, 20,45-29,45 s) e cartela.
# Cada etapa pesada pega a própria trava (uma por peça). Saída: out/PREVIA_9x16/ e out/PREVIA_9x16_entrega/.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"; DOMI="$(cd ../.. && pwd)"; mkdir -p "$DOMI/rec/t0v2" out
flock "$DOMI/.heavy.lock" nice -n 10 node cenas/render_cenas_vertical.cjs 4 ../narracao/cap04_t0.json "$DOMI/rec/t0v2/t0v2-cap04-9x16.mp4" --cauda 0 --de 20.45 --ate 29.45 --html cenas/cenas_vertical.html
flock "$DOMI/.heavy.lock" nice -n 10 node cenas/render_cenas_vertical.cjs 4 ../narracao/cap04_t0.json - --auditar --de 20.45 --ate 29.45 --html cenas/cenas_vertical.html | tee out/auditoria_previa.log
python3 -I finish.py caps/PREVIA.9x16.aula.json > out/finish_previa.log 2>&1 || { tail -15 out/finish_previa.log; exit 1; }
tail -2 out/finish_previa.log
