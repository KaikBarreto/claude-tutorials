#!/usr/bin/env bash
# T7 · 1.38.21: ensaio --rapido de todos os capítulos (00 a 14), uma trava por capítulo (o rodar.sh pega e solta a sua),
# com /__dev/unknowns zerado antes de cada um. Saída em rec/t7/.ens-1.38.21/NN.out e .unk.json. Uso: FAKE_URL=http://127.0.0.1:54334 rec/t7/ensaio_todos.sh
set -uo pipefail
cd /home/claude/domiflix
: "${FAKE_URL:?defina FAKE_URL (ex.: http://127.0.0.1:54334)}"
OUT=rec/t7/.ens-1.38.21; mkdir -p "$OUT"
for n in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  NN=$(printf '%02d' "$n")
  curl -s -XPOST "$FAKE_URL/__dev/unknowns/clear" >/dev/null
  timeout 3000 bash rec/t7/rodar.sh "$n" --rapido > "$OUT/$NN.out" 2>&1
  curl -s "$FAKE_URL/__dev/unknowns" > "$OUT/$NN.unk.json"
  echo "cap$NN fim" >> "$OUT/_progresso.txt"
done
echo TODOS >> "$OUT/_progresso.txt"
