#!/bin/bash
# T12 · fila de ensaios/gravações, UM capítulo por trava (docs/04: nunca um lote sob um flock só), na instância 54312.
# Para cada capítulo: (re)gera o roteiro, grava (--rapido = ensaio rápido; sem = completo) pelo t12_grava.sh, tira a semente apos-capNN
# do estado da instância quando o capítulo é da cadeia (antes de outro capítulo meu resetar a instância) e escreve o resumo.
# Uso: bash rec/t12/t12_fila.sh [--rapido] NN [NN ...]    (rodar FORA de outro flock; não editar este arquivo com uma fila rodando)
set -u
cd /home/claude/ecoflix
MODO=""; CAPS=()
for a in "$@"; do if [ "$a" = "--rapido" ]; then MODO="--rapido"; else CAPS+=("$(printf '%02d' "$((10#$a))")"); fi; done
SEMEIA=" 05 06 07 08 09 "   # capítulos que deixam estado para o seguinte (apos-capNN)
for NN in "${CAPS[@]}"; do
  echo "##### cap$NN $MODO $(date +%H:%M:%S)"
  python3 -I rec/t12/gerar.py "$NN" | tail -1
  bash rec/t12/t12_grava.sh "$NN" $MODO
  RC=$?
  OUT=rec/t12/.cap$NN.out; [ "$MODO" = "--rapido" ] && OUT=rec/t12/_ens/.cap$NN.out
  FALHOS=$(grep -c "FALHOU" "$OUT" 2>/dev/null); SEMALVO=$(grep -c "SEM ALVO" "$OUT" 2>/dev/null)
  echo "cap$NN exit $RC falhos ${FALHOS:-?} sem_alvo ${SEMALVO:-?}"
  if [ "$RC" = "0" ] && [ "${FALHOS:-1}" = "0" ] && [[ "$SEMEIA" == *" $NN "* ]]; then
    python3 -I rec/t12/t12_semente.py "apos-cap$NN" | tail -12
  fi
  if [ "$MODO" = "--rapido" ]; then python3 -I rec/t12/resumo.py "$NN" --ens > "rec/t12/_ens/resumo$NN.txt" 2>&1
  else python3 -I rec/t12/resumo.py "$NN" > "rec/t12/resumo$NN.txt" 2>&1; fi
  echo "fim cap$NN $(date +%H:%M:%S)"
done
echo "##### fila terminou $(date +%H:%M:%S)"
