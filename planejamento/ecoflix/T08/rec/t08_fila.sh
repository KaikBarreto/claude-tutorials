#!/bin/bash
# T08 · capítulos em sequência, cada um na sua trava (t08_grava.sh --os-dois ou o modo dado em MODO=...), sem semente: cada capítulo
# parte da própria semente (t08_sementes_e3.py). Vários destes podem esperar a trava ao mesmo tempo. Apaga os MP4; a folha de contato
# da completa fica para ser olhada. Uma tarefa por vez na fila (rec/fila.sh). Uso: bash rec/t08/t08_fila.sh 03:--auto 04:--os-dois ...
cd /home/claude/ecoflix
for ITEM in "$@"; do
  NN=${ITEM%%:*}; M=${ITEM#*:}; [ "$M" = "$ITEM" ] && M=${MODO:---os-dois}
  bash rec/t08/t08_grava.sh "$NN" "$M"; RC=$?
  FE=$(grep -c '!!ERRO' "rec/t08/_ens/cap$NN.resumo" 2>/dev/null); FC=$(grep -c '!!ERRO' "rec/t08/cap$NN.resumo" 2>/dev/null)
  S=$(cat "rec/t08/_ens/.cap$NN.out" "rec/t08/.cap$NN.out" 2>/dev/null | grep -c 'SEM ALVO')
  echo "cap$NN rc=$RC falhos ens=$FE completa=$FC semalvo=$S | $(head -1 "rec/t08/cap$NN.resumo" 2>/dev/null)"
  rm -f "/home/claude/ecoflix/rec/t08/_ens/t08-cap$NN.mp4" "/home/claude/ecoflix/rec/t08/t08-cap$NN.mp4"   # as folhas de contato ficam para serem olhadas
  [ "$NN" = 08 ] && python3 -I rec/t08/t08_pdf.py > rec/t08/cap08.pdf.txt 2>&1
done
echo "fila fim $(date +%H:%M:%S)"
