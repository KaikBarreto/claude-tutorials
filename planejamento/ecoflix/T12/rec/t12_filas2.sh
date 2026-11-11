#!/bin/bash
# T12 · uma fila de capítulos pelo t12_cap.sh (cada capítulo na sua trava). Itens: NN ou NN:--so-rapido / NN:--so-completo.
# Na cadeia (05 a 09), um ensaio rápido com passo falho para a fila (o capítulo seguinte partiria de semente velha).
# Uso: bash rec/t12/t12_filas.sh 05 06 07:--so-rapido ...   (não editar com uma fila rodando)
cd /home/claude/ecoflix
for ITEM in "$@"; do
  NN=${ITEM%%:*}; MODO=""; [ "$ITEM" != "$NN" ] && MODO=${ITEM#*:}
  echo "##### cap$NN $MODO $(date +%H:%M:%S)"
  bash rec/t12/t12_cap2.sh "$NN" $MODO
  if [[ " 05 06 07 08 09 " == *" $NN "* ]] && [ "$MODO" != "--so-completo" ] && ! grep -q "^cap$NN rapido falhos 0 " <(bash -c "tail -40 /proc/$$/fd/1" 2>/dev/null) ; then
    grep -q "FALHOU" "rec/t12/_ens/.cap$NN.out" && { echo "cadeia parada em cap$NN"; break; }
  fi
done
echo "##### fila terminou $(date +%H:%M:%S)"
