#!/usr/bin/env bash
# T11 · lote de ensaios, um capítulo por vez (cada um na sua trava, dentro do t11_rodar.sh), retomável:
#   bash rec/t11/t11_lote.sh 09:rapido 13:rapido 07:completo ...
# Cada item feito deixa rec/t11/_ens/.feito-NN-modo e é pulado se o lote for disparado de novo. Na gravação completa, o MP4 é
# apagado logo depois (fica a folha de contato em /dev/shm/t11/ para olhar e apagar; actions/telemetry ficam em rec/t11/).
set -uo pipefail
cd /home/claude/ecoflix
mkdir -p rec/t11/_ens /dev/shm/t11
for item in "$@"; do
  NN=${item%%:*}; MODO=${item#*:}
  feito="rec/t11/_ens/.feito-$NN-$MODO"
  [ -e "$feito" ] && { echo "cap$NN $MODO: já feito"; continue; }
  bash rec/t11/t11_rodar.sh "$NN" "$MODO" > "/dev/shm/t11/lote-$NN-$MODO.log" 2>&1
  rc=$?
  if [ "$MODO" = completo ]; then
    for f in rec/t11/t11-cap$NN.mp4 rec/t11/cap$NN.mp4; do [ -e "$f" ] && rm -f -- "/home/claude/ecoflix/$f"; done
    for f in rec/t11/t11-cap$NN.contact.jpg rec/t11/cap$NN.contact.jpg; do [ -e "$f" ] && mv -f -- "$f" /dev/shm/t11/; done
    r="rec/t11/.resumo-$NN.txt"; o="rec/t11/.rec-$NN.out"
  else
    if [ "$MODO" = rapidomp4 ]; then
      [ -e "rec/t11/_ens/t11-cap$NN.mp4" ] && rm -f -- "/home/claude/ecoflix/rec/t11/_ens/t11-cap$NN.mp4"
      [ -e "rec/t11/_ens/t11-cap$NN.contact.jpg" ] && mv -f -- "rec/t11/_ens/t11-cap$NN.contact.jpg" /dev/shm/t11/
      python3 -I rec/t11/prever.py "$NN" --ens > "rec/t11/.prever-$NN.txt" 2>&1
    fi
    r="rec/t11/_ens/.resumo-$NN.txt"; o="rec/t11/_ens/.ens-$NN.out"
  fi
  [ "$rc" = 0 ] && touch "$feito"
  echo "cap$NN $MODO rc=$rc falhas=$(grep -c FALHOU "$o" 2>/dev/null) $(grep -o 'maxLate [0-9.]*' "$o" 2>/dev/null | tail -1) $(grep 'conferências' "$r" 2>/dev/null) $(grep -o 'maior atraso.*' "rec/t11/.prever-$NN.txt" 2>/dev/null | head -1)"
done
