#!/usr/bin/env bash
# T7 · confere o recorte da tela do celular numa posse só da trava (CPU pesada):
#   1. testes/recorte_celular.sh da skill: código novo passa, código ANTIGO é acusado (um teste que não pode falhar não vale nada)
#      e o 16:9 de computador sai idêntico bit a bit;
#   2. o mesmo no capítulo de verdade: auditar_recorte.py com o código ANTIGO (scratchpad, `pad = 0`) acusa canto reto nos quadros
#      de risco do cap. 1, e com o código NOVO passa;
# (testes/identidade_domiflix.sh roda à parte, ~2 min: a cópia de baixo é a do arquivo identidade_base.log)
# uso: rec/t7/testes_recorte.sh [cap01 ...]      (padrão: cap01)
set -uo pipefail
export TUT_HOME=/home/claude/domiflix
S=/tmp/claude-0/-home-claude/5ab7153e-b0bb-5f91-8e7e-f0df5c647505/scratchpad/clip
CAPS=("${@:-cap01}")
rm -rf "${S:?}/home"; mkdir -p "$S/home/t/edit"
cp /home/claude/domiflix/t7/edit/*.py "$S/home/t/edit/"; ln -s /home/claude/domiflix/kit "$S/home/kit"
sed -i 's/pad = c if self.phone else 0/pad = 0/' "$S/home/t/edit/stage.py"
grep -q 'pad = 0' "$S/home/t/edit/stage.py" || { echo "!!! não consegui montar a cópia antiga do palco"; exit 2; }
corpo=$(cat <<'EOS'
set -uo pipefail
cd /home/claude/domiflix
RC=0
echo "=== 1. testes/recorte_celular.sh (sem gravação: celular novo x antigo, 16:9 idêntico)"
bash /home/claude/claude-tutorials/testes/recorte_celular.sh || RC=1
for c in "$@"; do
  echo "=== 2a. $c com o código ANTIGO (deve acusar canto reto)"
  python3 -I "$S/home/t/edit/auditar_recorte.py" "/home/claude/domiflix/t7/edit/caps/$c.chapter.json" --n 12 | tail -4
  echo "=== 2b. $c com o código NOVO (deve passar)"
  python3 -I t7/edit/auditar_recorte.py "t7/edit/caps/$c.chapter.json" --n 40 | tail -4 || RC=1
done
echo "FIM testes rc=$RC"
EOS
)
flock "$TUT_HOME/.heavy.lock" nice -n 10 env TUT_LOCKED=1 S="$S" bash -c "$corpo" _ "${CAPS[@]}"
