#!/usr/bin/env bash
# Prévia da cena de Windows do EcoTray (pedido do Kaik, 10/11): a pessoa abre o EcoTray pela bandeja, vê a balança
# conectada e o peso subindo, e o mesmo peso aparece no campo PESO (KG) da tela de compra. Sai um MP4 1920x1080 no palco
# da EcoFlix, com o cursor e a câmera da edição (render_chapter.py), sem áudio.
#
# uso: APP_SRC=<código do app> bash previa.sh <pasta de destino>
#   APP_SRC   pasta com ecotray/ e src/ do EcoSistema na versão gravada (somente leitura)
#   TRABALHO  pasta de trabalho (padrão $CENA_WIN_CACHE/previa, em /dev/shm)
#   LOCK      trava de tarefa pesada (padrão $TUT_HOME/.heavy.lock)
# Etapas: capturas do EcoTray (capturar_ecotray.py) -> cena (cena_windows.cjs) -> palco, cursor e câmera (render_chapter.py).
set -euo pipefail
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; SKILL="$(cd "$H/../.." && pwd)"; F="$SKILL/ferramentas"
DEST="${1:?uso: APP_SRC=<app> bash previa.sh <pasta de destino>}"; : "${APP_SRC:?defina APP_SRC (pasta do código do app)}"
export CENA_WIN_CACHE="${CENA_WIN_CACHE:-/dev/shm/cena-windows}"
T="${TRABALHO:-$CENA_WIN_CACHE/previa}"; P="$T/previa"
LOCK="${LOCK:-${TUT_HOME:-$HOME}/.heavy.lock}"; touch "$LOCK"
pesado() { flock "$LOCK" nice -n 10 "$@"; }

# área de trabalho mínima no formato do TUT_HOME (kit + marca + edit), para o render_chapter.py
mkdir -p "$P/app" "$P/rec" "$DEST"
ln -sfn "$F/kit" "$T/kit"
[ -f "$T/marca/marca.json" ] || { mkdir -p "$T/marca" && cp -r "$SKILL/perfis/ecoflix/marca/." "$T/marca/"; }
[ -f "$P/edit/render_chapter.py" ] || cp -r "$F/edit" "$P/edit"
ln -sf "$APP_SRC/src/assets/features/feature-pedidos.png" "$P/app/feature-pedidos.png"
ln -sf "$APP_SRC/ecotray/assets/icon.png" "$P/app/icon.png"
cp "$H/previa.json" "$H/previa.chapter.json" "$P/"
export MARCA_JSON="$T/marca/marca.json"

echo "== 1/3 janelas do EcoTray (código do app num display virtual)"
pesado python3 "$F/windows/capturar_ecotray.py" "$H/capturas.json" "$P/capturas" --app "$APP_SRC/ecotray"
echo "== 2/3 cena de Windows"
pesado node "$F/windows/cena_windows.cjs" "$P/previa.json" "$P/rec/previa-ecotray.mp4"
echo "== 3/3 palco, cursor e câmera"
[ -f "$P/edit/assets/fundo_escuro.png" ] || python3 "$P/edit/fundo_escuro.py" "$P/edit/assets/fundo_escuro.png" >/dev/null
pesado env TUT_LOCKED=1 python3 -I "$P/edit/render_chapter.py" "$P/previa.chapter.json" --no-audio --partes 1
cp "$P/out/previa/previa.mp4" "$DEST/EcoTray - cena de Windows (prévia).mp4"
echo "pronto: $DEST/EcoTray - cena de Windows (prévia).mp4"
