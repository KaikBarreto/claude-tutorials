#!/bin/bash
# T08 · lote de ensaios RÁPIDOS em cadeia (um capítulo por vez; cada um pega a trava sozinho no t08_grava.sh) e a semente apos-capNN
# logo depois do ensaio que a produz (só com 0 passo falho; senão o lote para). Apaga o MP4 do ensaio (o disco é curto).
# Uso: bash rec/t08/t08_lote.sh 00 01 02 ...   (não editar este arquivo com um lote rodando: copie antes)
cd /home/claude/ecoflix
for NN in "$@"; do
  bash rec/t08/t08_grava.sh "$NN" --rapido; RC=$?
  python3 -I rec/t08/resumo.py "$NN" --ens > "rec/t08/_ens/cap$NN.resumo" 2>&1
  F=$(grep -c '!!ERRO' "rec/t08/_ens/cap$NN.resumo")
  S=$(grep -c 'SEM ALVO' "rec/t08/_ens/.cap$NN.out")
  echo "cap$NN rc=$RC erros=$F semalvo=$S | $(head -1 "rec/t08/_ens/cap$NN.resumo")"
  rm -f "/home/claude/ecoflix/rec/t08/_ens/t08-cap$NN.mp4"
  case $NN in
    02|03|04|05|06|07|09)
      if [ "$F" = 0 ] && [ "$RC" = 0 ]; then python3 -I rec/t08/t08_semente.py "apos-cap$NN"; else echo "semente apos-cap$NN NAO gravada: lote parado"; break; fi;;
  esac
done
echo "lote fim $(date +%H:%M:%S)"
