#!/usr/bin/env bash
# T11 · lote do 1.60.18 (20/11): ensaia os 19 capítulos em sequência, rápido COM MP4 (folha de contato em /dev/shm/t11), um por vez pela fila
# (--prio 11, dentro do t11_rodar.sh). Caps 0 a 6 com a instância 54311 em 08:30; sobe de novo em 17:30 para os caps 7 a 18.
#   bash rec/t11/t11_lote160.sh [NN ...]   (sem argumentos: todos)   resumo: rec/t11/_ens/.lote160.txt
set -uo pipefail
cd /home/claude/ecoflix
export TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)}"
CAPS=("$@"); [ ${#CAPS[@]} -eq 0 ] && CAPS=(00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18)
OUT=rec/t11/_ens/.lote160.txt; : > "$OUT"; mkdir -p /dev/shm/t11
ATUAL=""
for NN in "${CAPS[@]}"; do
  if [ "$((10#$NN))" -ge 7 ]; then NOW=2026-11-10T17:30:00-03:00; else NOW=2026-11-10T08:30:00-03:00; fi
  if [ "$NOW" != "$ATUAL" ]; then
    FAKE_NOW=$NOW FAKE_PORT=54311 bash rec/run.sh fake > /dev/null 2>&1; sleep 4; ATUAL=$NOW
  fi
  bash rec/t11/t11_rodar.sh "$NN" rapidomp4 > "/dev/shm/t11/lote-$NN.log" 2>&1
  rc=$?
  rm -f -- "/home/claude/ecoflix/rec/t11/_ens/t11-cap$NN.mp4"
  [ -e "rec/t11/_ens/t11-cap$NN.contact.jpg" ] && mv -f -- "rec/t11/_ens/t11-cap$NN.contact.jpg" "/dev/shm/t11/cap$NN.contact.jpg"
  echo "cap$NN rc=$rc | $(head -1 rec/t11/_ens/.resumo-$NN.txt 2>/dev/null) | falhas=$(grep -c FALHOU rec/t11/_ens/.ens-$NN.out 2>/dev/null) diferente=$(grep -c DIFERENTE rec/t11/_ens/.resumo-$NN.txt 2>/dev/null)" >> "$OUT"
done
echo FIM >> "$OUT"
