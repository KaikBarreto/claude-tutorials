#!/usr/bin/env bash
# Cria (ou atualiza) a copia de trabalho do app da Dominex em <domiflix>/app e instala as dependencias.
# O codigo-fonte original e SOMENTE LEITURA: aqui so copiamos, nunca escrevemos nele.
#   rec/setup-app.sh                 copia por cima (sem apagar nada) e roda `npm ci` se faltar node_modules
#   DOMINEX_SRC=/outro/caminho rec/setup-app.sh
# Depois: rec/run.sh build   (gera o build de producao)   e   rec/run.sh up
set -euo pipefail

SRC="${DOMINEX_SRC:-${APP_SRC:-}}"  # pasta com o código do app (somente leitura; o build roda numa cópia em ../app)
[ -n "$SRC" ] || { echo "defina DOMINEX_SRC (ou APP_SRC) com a pasta do código do app" >&2; exit 1; }
DEST="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/app"

[ -f "$SRC/package.json" ] || { echo "codigo-fonte nao encontrado em $SRC (defina DOMINEX_SRC)" >&2; exit 1; }
mkdir -p "$DEST"

echo "copiando $SRC -> $DEST (sem .git, node_modules, dist e arquivos .env)"
tar -C "$SRC" \
  --exclude=./.git --exclude=./node_modules --exclude=./dist --exclude='./.env' --exclude='./.env.*' \
  -cf - . | tar -C "$DEST" -xf -

if [ ! -d "$DEST/node_modules" ]; then
  echo "instalando dependencias (npm ci)..."
  (cd "$DEST" && npm ci --no-audit --no-fund >"$DEST/../npm-ci.log" 2>&1) || { tail -n 20 "$DEST/../npm-ci.log" >&2; exit 1; }
fi
echo "app pronto em $DEST"
