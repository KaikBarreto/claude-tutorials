#!/usr/bin/env bash
# T07 · ensaio rápido de UM capítulo na instância 54307 (pela fila), com resumo e, nos capítulos que mudam o banco, a semente.
# uso: bash rec/t07/t07_ens.sh NN        (TUT_SENHA no ambiente, 8+ caracteres)
set -u
N=$(printf '%02d' "$((10#$1))")
cd /home/claude/ecoflix || exit 1
export TUT_USER=rafael@reciclavalemetais.example FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_URL=http://127.0.0.1:54307
curl -sf "$FAKE_URL/health" >/dev/null || { echo "instância 54307 fora do ar"; exit 2; }
python3 -I rec/t07/gerar.py "$N" | tail -2
python3 -I rec/t07/ensaio.py "$N"
bash rec/fila.sh --prio 07 -- node rec/record.mjs "rec/t07/_ens/cap$N.json" --rapido --preset ultrafast --crf 30 > "rec/t07/_ens/cap$N.out" 2>&1
echo "record rc=$?"; tail -3 "rec/t07/_ens/cap$N.out" | cut -c1-300
python3 -I rec/t07/resumo.py "$N" --ens > "rec/t07/_ens/cap$N.resumo.txt" 2>&1
grep -n "FALH\|SEM ALVO\|DIFERENTE\|pageIssues\|erro\|avisos de erro\|falho\|lido" "rec/t07/_ens/cap$N.resumo.txt" | cut -c1-420 | head -30
case "$N" in 03|11|15|17|18) python3 -I rec/t07/t07_semente.py "$N" 2>&1 | tail -6 ;; esac
curl -s "$FAKE_URL/__dev/unknowns" | cut -c1-600
ls rec/t07/_ens/ | grep "cap$N" | head
# folha de contato reduzida em /dev/shm (para olhar) e limpeza do MP4 e da folha grande (disco quase cheio)
python3 -c "
from PIL import Image
im=Image.open('/home/claude/ecoflix/rec/t07/_ens/t07-cap$N.contact.jpg'); im.thumbnail((1500,1500)); im.save('/dev/shm/t07_c$N.jpg',quality=72)" 2>&1 | tail -1
rm -f "/home/claude/ecoflix/rec/t07/_ens/t07-cap$N.mp4" "/home/claude/ecoflix/rec/t07/_ens/t07-cap$N.contact.jpg"
