#!/usr/bin/env bash
# Gera dist/tutorial-em-video.zip para enviar como skill no app Claude (Customize > Skills).
# O zip precisa ter a pasta da skill na raiz, com o mesmo nome do campo `name` do SKILL.md.
#   bash empacotar.sh            -> dist/tutorial-em-video.zip
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
NOME=$(sed -n 's/^name: *//p' SKILL.md | head -1)
TMP=$(mktemp -d); trap 'rm -rf "${TMP:?}"' EXIT
mkdir -p "$TMP/$NOME" dist
tar --exclude=.git --exclude=dist --exclude='__pycache__' --exclude='node_modules' --exclude='.runtime' -cf - . | tar -xf - -C "$TMP/$NOME"
rm -f "dist/$NOME.zip"
(cd "$TMP" && zip -qr "$OLDPWD/dist/$NOME.zip" "$NOME")
echo "dist/$NOME.zip ($(du -h "dist/$NOME.zip" | cut -f1))"
