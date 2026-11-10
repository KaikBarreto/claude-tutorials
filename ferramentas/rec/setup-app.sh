#!/usr/bin/env bash
# Prepara a copia de trabalho do app para o modo fakebase e instala as dependencias.
# O codigo-fonte original e SOMENTE LEITURA: aqui so copiamos, nunca escrevemos nele.
#   APP_SRC=/codigo/do/app rec/setup-app.sh
#       copia para <TUT_HOME>/app (sem .git, node_modules, dist e .env) e roda `npm ci` se faltar node_modules
#   APP_SRC=/dev/shm/x APP_WORK=/dev/shm/x rec/setup-app.sh
#       trabalha NA PROPRIA pasta (uma copia descartavel, ex.: `git archive` em /dev/shm; recusa pasta com .git):
#       node_modules e build ficam fora do disco; o `rec/run.sh build` (com o mesmo APP_WORK) leva so o dist
#       para <TUT_HOME>/app
#   APP_WORK=/outra/pasta  copia para la em vez de <TUT_HOME>/app
#   DOMINEX_SRC=...        nome antigo de APP_SRC (continua valendo)
# Com um mundo (rec/mundo ou FAKE_MUNDO) que tenha app/ajustes.json, aplica os ajustes na copia (rec/ajustar-app.mjs).
# Depois: rec/run.sh build   (gera o build de producao)   e   rec/run.sh up
set -euo pipefail

REC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${APP_SRC:-${DOMINEX_SRC:-}}"  # pasta com o código do app (somente leitura; o build roda numa cópia)
[ -n "$SRC" ] || { echo "defina APP_SRC (ou DOMINEX_SRC) com a pasta do código do app" >&2; exit 1; }
[ -f "$SRC/package.json" ] || { echo "codigo-fonte nao encontrado em $SRC (defina APP_SRC)" >&2; exit 1; }
SRC="$(cd "$SRC" && pwd)"
DEST="${APP_WORK:-$(dirname "$REC")/app}"
mkdir -p "$DEST"
DEST="$(cd "$DEST" && pwd)"

if [ "$DEST" = "$SRC" ]; then
  [ ! -e "$SRC/.git" ] || { echo "$SRC tem .git (repositorio do app): use uma copia (git archive) como APP_WORK" >&2; exit 1; }
  echo "trabalhando na propria pasta $SRC (copia descartavel)"
else
  echo "copiando $SRC -> $DEST (sem .git, node_modules, dist e arquivos .env)"
  tar -C "$SRC" \
    --exclude=./.git --exclude=./node_modules --exclude=./dist --exclude='./.env' --exclude='./.env.*' \
    -cf - . | tar -C "$DEST" -xf -
fi

# ajustes do mundo na copia (endereco do Supabase fixado no codigo etc.)
node "$REC/ajustar-app.mjs" "$DEST"

if [ ! -d "$DEST/node_modules" ]; then
  echo "instalando dependencias (npm ci)..."
  (cd "$DEST" && npm ci --no-audit --no-fund >"$DEST/../npm-ci.log" 2>&1) || { tail -n 20 "$DEST/../npm-ci.log" >&2; exit 1; }
fi
echo "app pronto em $DEST"
