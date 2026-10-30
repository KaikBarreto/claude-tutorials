#!/usr/bin/env bash
# Baixa a(s) gravação(ões) de um link do Google Drive (arquivo ou pasta compartilhada "qualquer pessoa com o link").
# uso: bash kit/fetch.sh "<link do drive>" <pasta_destino>
set -euo pipefail
URL="${1}"; DEST="${2:-/home/user/domiflix/raw}"; mkdir -p "$DEST"
if [[ "$URL" == *"/folders/"* ]]; then gdown --folder "$URL" -O "$DEST" --remaining-ok; else gdown --fuzzy "$URL" -O "$DEST/"; fi
ls -la "$DEST"
