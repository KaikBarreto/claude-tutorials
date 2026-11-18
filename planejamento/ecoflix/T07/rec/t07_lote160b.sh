#!/usr/bin/env bash
# T07 · lote 2: rápido dos que falharam (-r "NN ...") e depois o COMPLETO (-c "NN ...") dos que têm rápido sem falho.  TUT_SENHA no ambiente.
cd /home/claude/ecoflix || exit 1
export TUT_USER=rafael@reciclavalemetais.example FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_URL=http://127.0.0.1:54307
R="$1"; C="$2"
for n in $R; do
  echo "===== rapido cap$n $(date +%H:%M:%S)"
  bash rec/t07/t07_ens.sh "$n" 2>&1 | grep -v "^t07-\|^  }\|^}\|^video\|^cap[0-9]*\.\(json\|out\|resumo\|prever\|check\|semente\)" | cut -c1-600
  python3 -I rec/t07/prever.py "$n" --ens > "rec/t07/_ens/cap$n.prever.txt" 2>&1
done
for n in $C; do
  echo "===== completo cap$n $(date +%H:%M:%S)"
  head -1 "rec/t07/_ens/cap$n.resumo.txt" | grep -q "falhos 0," || { echo "pulado: rápido com falha"; continue; }
  python3 -I rec/t07/gerar.py "$n" | tail -1
  bash rec/fila.sh --prio 07 -- node rec/record.mjs "rec/t07/cap$n.json" --preset ultrafast --crf 30 > "rec/t07/cap$n.out" 2>&1
  echo "record rc=$?"
  python3 -I rec/t07/resumo.py "$n" > "rec/t07/cap$n.resumo.txt" 2>&1
  head -1 "rec/t07/cap$n.resumo.txt" | cut -c1-200
  grep -n "ERRO\|DIFERENTE\|SEM ALVO" "rec/t07/cap$n.resumo.txt" | cut -c1-300 | head -8
  python3 -c "
from PIL import Image
im=Image.open('/home/claude/ecoflix/rec/t07/t07-cap$n.contact.jpg'); im.thumbnail((1500,1500)); im.save('/dev/shm/t07_g$n.jpg',quality=72)" 2>&1 | tail -1
  rm -f "/home/claude/ecoflix/rec/t07/t07-cap$n.mp4" "/home/claude/ecoflix/rec/t07/t07-cap$n.contact.jpg"
done
echo "===== fim $(date +%H:%M:%S)"
