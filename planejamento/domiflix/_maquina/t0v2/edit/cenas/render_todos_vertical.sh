#!/usr/bin/env bash
# Renderiza os capítulos ilustrados VERTICAIS (cenas_vertical.html, 1080x1920) em $TUT_HOME/rec/<tut>/<tut>-capNN-9x16.mp4, um
# por vez, sob a trava de tarefa pesada (uma trava por capítulo). Sem argumentos: todos os capítulos com narração processada
# (<tutorial>/narracao/capNN.json). O vídeo já é o quadro final (palco + painel + cena); o palco vertical é gerado se faltar.
# uso: bash render_todos_vertical.sh [NN ...]        (ex.: bash render_todos_vertical.sh 05 00)
#   CAUDA=1.2   segundos de respiro depois da última palavra (o mesmo do render_todos.sh)
# Depois: python3 capitulos_ilustrados.py "<Título>" --formato 9x16 e finish.py caps/<AULA>.9x16.aula.json (docs/09-aula-ilustrada.md).
set -euo pipefail
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; TUT="$(cd "$H/../.." && pwd)"; DOMI="$(dirname "$TUT")"; N="$(basename "$TUT")"
[ -f "$H/cenas_vertical.html" ] || { echo "falta $H/cenas_vertical.html (copie cenas_modelo_vertical.html e desenhe as cenas)"; exit 1; }
[ -d "$H/node_modules/lucide-static" ] || (cd "$H" && npm install --no-audit --no-fund >/dev/null 2>&1)
[ -f "$TUT/edit/assets/fundo_escuro_9x16.png" ] || python3 "$TUT/edit/fundo_escuro_vertical.py" >/dev/null
mkdir -p "$DOMI/rec/$N"
CAPS=("$@"); [ ${#CAPS[@]} -gt 0 ] || CAPS=($(ls "$TUT/narracao" | sed -n 's/^cap\([0-9][0-9]\)\.json$/\1/p'))
for c in "${CAPS[@]}"; do
  flock "$DOMI/.heavy.lock" nice -n 10 node "$H/render_cenas_vertical.cjs" "$((10#$c))" "$TUT/narracao/cap$c.json" "$DOMI/rec/$N/$N-cap$c-9x16.mp4" \
    --cauda "${CAUDA:-1.2}" --html "$H/cenas_vertical.html"
done
