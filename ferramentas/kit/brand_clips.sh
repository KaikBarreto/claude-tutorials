#!/usr/bin/env bash
# Renderiza vinheta (com o título da aula) e cartela final do projeto, com áudio, na identidade da marca
# (<TUT_HOME>/marca/marca.json ou $MARCA_JSON; sem arquivo, padrão neutro: modelos/MARCA.md).
# uso: bash kit/brand_clips.sh [--sem-domiflix] <projeto> "<título da aula>" ["<frase da cartela>"]   (sem frase: a do marca.json)
#   --sem-domiflix  tira o rótulo "▶ DOMIFLIX" (série do marca.json) da vinheta e da cartela; padrão: com (identidade congelada)
set -euo pipefail
SEMS=""; if [ "${1:-}" = "--sem-domiflix" ]; then SEMS="&sem_serie=1"; shift; fi
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(dirname "$KIT")"
PROJ="$(cd "${1}" && pwd)"; TITLE="${2}"
PORT="${PORT:-8790}"
# publica a marca em web/_marca/<hash>/ (o servidor da página só enxerga web/) e lê a frase padrão da cartela
MARCA_WEB="$(python3 "$KIT/ui.py" --web "$ROOT/web")"
OUTRO_LINE="${3:-$(printf '%s\n' "$MARCA_WEB" | sed -n 2p)}"; MARCA_WEB="$(printf '%s\n' "$MARCA_WEB" | sed -n 1p)"
# o servidor da porta tem de servir ESTA pasta web/ (a marca acabou de ser publicada nela); se for de outra área de
# trabalho (ou não houver), sobe um próprio numa porta livre e derruba no fim
SRV=""
if ! curl -sf -o /dev/null "http://127.0.0.1:${PORT}/${MARCA_WEB}"; then
  PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')"
  (cd "$ROOT/web" && exec python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1) & SRV=$!
  trap '[ -n "$SRV" ] && kill "$SRV" 2>/dev/null || true' EXIT
  for _ in $(seq 1 30); do curl -sf -o /dev/null "http://127.0.0.1:${PORT}/${MARCA_WEB}" && break; sleep 0.2; done
fi
enc() { python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1]))' "$1"; }
mkdir -p "$PROJ/build"
M="marca=$(enc "$MARCA_WEB")$SEMS"
node "$KIT/render_page.cjs" "http://127.0.0.1:${PORT}/intro.html?title=$(enc "$TITLE")&$M" "$PROJ/build/intro_v.mp4" --grain 7 --meta "$PROJ/build/intro_meta.json" & P1=$!
node "$KIT/render_page.cjs" "http://127.0.0.1:${PORT}/intro.html?mode=outro&title=$(enc "$OUTRO_LINE")&$M" "$PROJ/build/outro_v.mp4" --grain 7 --meta "$PROJ/build/outro_meta.json" & P2=$!
wait "$P1" "$P2"  # só os dois renders (o servidor da página, se for nosso, segue até o fim)
python3 "$ROOT/audio/intro_audio.py" "$PROJ/build/intro_meta.json" "$PROJ/build/intro_audio.wav"
python3 "$ROOT/audio/intro_audio.py" "$PROJ/build/outro_meta.json" "$PROJ/build/outro_audio.wav"
echo "brand_clips_done"
