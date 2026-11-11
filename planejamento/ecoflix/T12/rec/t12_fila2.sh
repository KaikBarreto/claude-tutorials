#!/bin/bash
# T12 · fila de ensaios/gravações, UM capítulo por trava (docs/04: nunca um lote sob um flock só), na instância 54312.
# Para cada capítulo: (re)gera o roteiro, grava (--rapido = ensaio rápido; sem = completo) pelo t12_grava.sh, tira a semente apos-capNN
# do estado da instância quando o capítulo é da cadeia (antes de outro capítulo meu resetar a instância) e escreve o resumo.
# Uso: bash rec/t12/t12_fila2.sh r04 f00 r05 ...   (r = ensaio rápido, f = ensaio completo; FORA de outro flock; não editar com a fila rodando)
set -u
cd /home/claude/ecoflix
SEMEIA=" 05 06 07 08 09 "   # capítulos que deixam estado para o seguinte (apos-capNN)
for ITEM in "$@"; do
  MODO=""; [ "${ITEM:0:1}" = "r" ] && MODO="--rapido"
  NN=$(printf '%02d' "$((10#${ITEM:1}))")
  echo "##### cap$NN $MODO $(date +%H:%M:%S)"
  python3 -I rec/t12/gerar.py "$NN" | tail -1
  bash rec/t12/t12_grava.sh "$NN" $MODO
  RC=$?
  OUT=rec/t12/.cap$NN.out; [ "$MODO" = "--rapido" ] && OUT=rec/t12/_ens/.cap$NN.out
  FALHOS=$(grep -c "FALHOU" "$OUT" 2>/dev/null); SEMALVO=$(grep -c "SEM ALVO" "$OUT" 2>/dev/null)
  echo "cap$NN exit $RC falhos ${FALHOS:-?} sem_alvo ${SEMALVO:-?}"
  [ -z "$MODO" ] && rm -f "/home/claude/ecoflix/rec/t12/t12-cap$NN.mp4"   # disco curto: o MP4 do ensaio sai na hora (fica a folha de contato)
  if [ "$RC" = "0" ] && [ "${FALHOS:-1}" = "0" ] && [[ "$SEMEIA" == *" $NN "* ]]; then
    python3 -I rec/t12/t12_semente.py "apos-cap$NN" | tail -12
  fi
  if [ "$MODO" = "--rapido" ]; then python3 -I rec/t12/resumo.py "$NN" --ens > "rec/t12/_ens/resumo$NN.txt" 2>&1
  else python3 -I rec/t12/resumo.py "$NN" > "rec/t12/resumo$NN.txt" 2>&1; fi
  echo "fim cap$NN $(date +%H:%M:%S)"
done
echo "##### fila terminou $(date +%H:%M:%S)"
