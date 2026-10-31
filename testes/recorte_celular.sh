#!/usr/bin/env bash
# Confere o recorte da tela do celular no palco (Stage._render), SEM gravação nenhuma, em ~1 min:
#   1. celular, código novo: com a borda da tela já fora do quadro e o canto arredondado ainda invadindo (zoom entrando/saindo,
#      deslizes, desfoque de movimento), a tela é o retângulo arredondado: sem canto reto por cima da moldura;
#   2. celular, código ANTIGO (`pad = 0`): o teste tem de ACUSAR o canto reto (um teste que não pode falhar não vale nada);
#   3. computador 16:9: quadros do palco IDÊNTICOS bit a bit ao código antigo (o conserto vale só para o celular).
#   bash testes/recorte_celular.sh        (Python + numpy/OpenCV; sem rede; toma a trava $TUT_HOME/.heavy.lock se TUT_HOME existir)
# Rode depois de mexer em ferramentas/edit/stage.py, junto de testes/identidade_domiflix.sh.
set -euo pipefail
if [ -n "${TUT_HOME:-}" ] && [ -z "${TUT_LOCKED:-}" ]; then exec flock "$TUT_HOME/.heavy.lock" nice -n 10 env TUT_LOCKED=1 bash "$0" "$@"; fi
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "${TMP:?}"' EXIT
# mesma árvore do identidade_domiflix.sh: o stage.py acha o kit em ../../kit (links, nada é copiado)
H="$TMP/home"; mkdir -p "$H/t"; ln -s "$SKILL/ferramentas/kit" "$H/kit"; ln -s "$SKILL/ferramentas/edit" "$H/t/edit"
python3 -I "$SKILL/testes/recorte_celular.py" "$H/t/edit"
