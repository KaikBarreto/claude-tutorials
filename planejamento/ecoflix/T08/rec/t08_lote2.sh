#!/bin/bash
# T08 · lote em cadeia, UM capítulo por trava: ensaio rápido + gravação completa (t08_grava.sh --os-dois), os dois resumos, a semente
# apos-capNN do estado da gravação completa (só com 0 passo falho nas duas; senão o lote para) e o PDF do cap08. Apaga os MP4 (disco curto);
# a folha de contato da completa fica para ser olhada. Uso: bash rec/t08/t08_lote2.sh 03 04 ...  (copie antes de editar com lote rodando)
cd /home/claude/ecoflix
for NN in "$@"; do
  bash rec/t08/t08_grava.sh "$NN" --os-dois; RC=$?
  python3 -I rec/t08/resumo.py "$NN" > "rec/t08/cap$NN.resumo" 2>&1
  FE=$(grep -c '!!ERRO' "rec/t08/_ens/cap$NN.resumo"); FC=$(grep -c '!!ERRO' "rec/t08/cap$NN.resumo")
  S=$(cat "rec/t08/_ens/.cap$NN.out" "rec/t08/.cap$NN.out" 2>/dev/null | grep -c 'SEM ALVO')
  echo "cap$NN rc=$RC falhos ens=$FE completa=$FC semalvo=$S | $(head -1 "rec/t08/cap$NN.resumo")"
  rm -f "/home/claude/ecoflix/rec/t08/_ens/t08-cap$NN.mp4" "/home/claude/ecoflix/rec/t08/_ens/t08-cap$NN.contact.jpg" "/home/claude/ecoflix/rec/t08/t08-cap$NN.mp4"
  [ "$NN" = 08 ] && python3 -I rec/t08/t08_pdf.py > rec/t08/cap08.pdf.txt 2>&1
  case $NN in
    02|03|04|05|06|07|09)
      if [ "$FE" = 0 ] && [ "$FC" = 0 ] && [ "$RC" = 0 ]; then python3 -I rec/t08/t08_semente.py "apos-cap$NN"; else echo "semente apos-cap$NN NAO gravada: lote parado"; break; fi;;
  esac
done
echo "lote fim $(date +%H:%M:%S)"
