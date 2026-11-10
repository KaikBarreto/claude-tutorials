#!/usr/bin/env bash
# Vinheta de abertura (com o título da aula) e cartela final no formato VERTICAL 9:16 (1080x1920), com áudio, na identidade
# da marca (<TUT_HOME>/marca/marca.json ou $MARCA_JSON). Faz o que o kit/brand_clips.sh faz no 16:9, com a página
# web/intro_vertical.html: a mesma linha do tempo e os mesmos CUES, então o som sai idêntico bit a bit ao do 16:9
# (a vinheta e a cartela têm a mesma duração: 4,42 s e 3,85 s). Estilos: "dominex-capacete" (Domiflix) e
# "ecosistema-reciclagem" (EcoFlix: símbolo, o EcoFlix sai de trás dele para baixo, título); o "logo" não tem vertical.
# uso: bash kit/brand_clips_vertical.sh <projeto> "<título da aula>" ["<frase da cartela>"]   (sem frase: a do marca.json)
#   SERIE_LOGO=assets/<logo>.png   opcional: logo da série todo branco entre o DOMINEX e o título (ex.: assets/domiflix_logo_branco.png).
#                                  Padrão (pedido do Kaik): sem logo nem rótulo da série; o título sobe logo abaixo do DOMINEX.
#                                  Só no capacete: na EcoFlix o nome já é o logo (a página ignora).
# Saídas em <projeto>/build: intro_v.mp4, outro_v.mp4, intro_audio.wav, outro_audio.wav (+ *_meta.json), como no 16:9,
# para o edit/finish.py (--formato 9x16) montar a aula sem outro caminho. Pesado (dois Chromium): rode sob
# `flock $TUT_HOME/.heavy.lock nice -n 10` (o finish.py já roda assim).
set -euo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(dirname "$KIT")"
PROJ="$(cd "${1}" && pwd)"; TITLE="${2}"
PORT="${PORT:-8790}"
SERIE_LOGO="${SERIE_LOGO-}"   # padrão (pedido do Kaik): sem logo da série, só capacete + DOMINEX + título
[ -z "$SERIE_LOGO" ] || [ -f "$ROOT/web/$SERIE_LOGO" ] || { echo "SERIE_LOGO=$SERIE_LOGO não existe em $ROOT/web"; exit 1; }
[ -f "$ROOT/web/intro_vertical.html" ] || { echo "falta $ROOT/web/intro_vertical.html (rode o instalar.sh da skill de novo)"; exit 1; }
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
M="marca=$(enc "$MARCA_WEB")"; if [ -n "$SERIE_LOGO" ]; then M="$M&serie_logo=$(enc "$SERIE_LOGO")"; else M="$M&sem_serie=1"; fi
node "$KIT/render_page.cjs" "http://127.0.0.1:${PORT}/intro_vertical.html?title=$(enc "$TITLE")&$M" "$PROJ/build/intro_v.mp4" --w 1080 --h 1920 --grain 7 --meta "$PROJ/build/intro_meta.json" & P1=$!
node "$KIT/render_page.cjs" "http://127.0.0.1:${PORT}/intro_vertical.html?mode=outro&title=$(enc "$OUTRO_LINE")&$M" "$PROJ/build/outro_v.mp4" --w 1080 --h 1920 --grain 7 --meta "$PROJ/build/outro_meta.json" & P2=$!
wait "$P1" "$P2"  # só os dois renders (o servidor da página, se for nosso, segue até o fim)
python3 "$ROOT/audio/intro_audio.py" "$PROJ/build/intro_meta.json" "$PROJ/build/intro_audio.wav"
python3 "$ROOT/audio/intro_audio.py" "$PROJ/build/outro_meta.json" "$PROJ/build/outro_audio.wav"
echo "brand_clips_done"
