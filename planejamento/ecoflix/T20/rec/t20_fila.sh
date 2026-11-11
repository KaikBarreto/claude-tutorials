#!/bin/bash
# T20 · fila de ensaios/gravações, UM capítulo por trava (docs/04), na instância 54320. Para cada capítulo: (re)gera o roteiro, grava
# (--rapido = ensaio rápido; sem = completo) pelo t20_grava.sh e escreve o resumo. As sementes apos-capNN saem de t20_sementes.py
# (determinístico); a conferência de que o estado vivo bate com elas é feita à parte (t20_confere.py).
# Uso: bash rec/t20/t20_fila.sh [--rapido] NN [NN ...]    (rodar FORA de outro flock; não editar este arquivo com uma fila rodando)
set -u
cd /home/claude/ecoflix
MODO=""; CAPS=()
for a in "$@"; do if [ "$a" = "--rapido" ]; then MODO="--rapido"; else CAPS+=("$(printf '%02d' "$((10#$a))")"); fi; done
for NN in "${CAPS[@]}"; do
  echo "##### cap$NN $MODO $(date +%H:%M:%S)"
  python3 -I rec/t20/gerar.py "$NN" | tail -1
  bash rec/t20/t20_grava.sh "$NN" $MODO
  RC=$?
  OUT=rec/t20/.cap$NN.out; [ "$MODO" = "--rapido" ] && OUT=rec/t20/_ens/.cap$NN.out
  FALHOS=$(grep -c "FALHOU" "$OUT" 2>/dev/null); SEMALVO=$(grep -c "SEM ALVO" "$OUT" 2>/dev/null)
  echo "cap$NN exit $RC falhos ${FALHOS:-?} sem_alvo ${SEMALVO:-?}"
  if [ "$MODO" = "--rapido" ]; then python3 -I rec/t20/resumo.py "$NN" --ens > "rec/t20/_ens/resumo$NN.txt" 2>&1
  else python3 -I rec/t20/resumo.py "$NN" > "rec/t20/resumo$NN.txt" 2>&1; fi
  echo "fim cap$NN $(date +%H:%M:%S)"
done
echo "##### fila terminou $(date +%H:%M:%S)"
