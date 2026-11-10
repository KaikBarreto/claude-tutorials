#!/usr/bin/env bash
# Fila de renders do tutorial: renderiza cada capítulo listado em out/fila.txt (um por linha), na ordem; termina com a linha FIM.
cd "$(dirname "${BASH_SOURCE[0]}")"
F=out/fila.txt; FEITOS=out/fila_feitos.txt; touch "$F" "$FEITOS"
while true; do
  next=$(grep -vxFf "$FEITOS" "$F" | grep -vx FIM | head -1 || true)
  if [ -n "$next" ]; then
    python3 -I render_chapter.py "caps/cap$next.chapter.json" > "out/render_cap$next.log" 2>&1
    echo "cap$next exit $? $(tail -c 160 "out/render_cap$next.log" | tr '\r' '\n' | tail -1)"
    echo "$next" >> "$FEITOS"
  elif grep -qx FIM "$F"; then
    echo "fila concluída"; break
  else
    sleep 15
  fi
done
