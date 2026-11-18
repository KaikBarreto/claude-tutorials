#!/bin/bash
# T17 · lote de ensaios RÁPIDOS (ou completos) em sequência, um capítulo por vez na fila (rec/fila.sh --prio 17, pelo t17_fila.sh), com
# o resumo.py e o prever.py de cada capítulo gravados em arquivo e uma linha por capítulo em rec/t17/_ens/<nome>.txt.
# Capítulo que grava estado regrava a semente cumulativa quando passa (02, 04, 05, 08, 09, 10, 13).
# Uso (segundo plano, prazo 7200000): bash rec/t17/t17_lote.sh lote1 [NN[:c] ...]   (sem capítulos = todos, no rápido)
set -u
cd /home/claude/ecoflix
NOME=$1; shift
[ $# -gt 0 ] || set -- 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19
declare -A SEED=( [02]=apos-cap02 [04]=apos-cap04 [05]=apos-cap05 [08]=apos-cap08 [09]=apos-cap09 [10]=apos-cap10 [13]=apos-cap13 )
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
SAIDA=rec/t17/_ens/$NOME.txt
FIM=$(( $(date +%s) + 6500 ))   # o segundo plano morre em 2 h: não começa capítulo novo depois de 1 h 48
mkdir -p rec/t17/_ens
python3 -I rec/t17/gerar.py > rec/t17/_ens/$NOME.gerar.txt 2>&1 || { echo "gerar.py falhou" | tee -a $SAIDA; exit 2; }
echo "== $NOME $(date '+%d/%m %H:%M') ==" >> $SAIDA
for it in "$@"; do
  IFS=: read -r NN MODO <<< "$it"; NN=$(printf '%02d' "$((10#$NN))"); MODO=${MODO:-r}
  if [ "$(date +%s)" -ge "$FIM" ]; then echo "PARADA antes de cap$NN (prazo do lote): relançar daqui" >> $SAIDA; break; fi
  ITEM="$NN:$MODO"; [ -n "${SEED[$NN]:-}" ] && ITEM="$ITEM:${SEED[$NN]}"
  bash rec/t17/t17_fila.sh "$ITEM" > rec/t17/_ens/$NOME.cap$NN.fila.txt 2>&1; RC=$?
  if [ "$MODO" = "r" ]; then DIR=rec/t17/_ens; OUT=$DIR/.cap$NN.out; FLAG=--ens; else DIR=rec/t17; OUT=$DIR/.cap$NN.out; FLAG=; fi
  python3 -I rec/t17/resumo.py $NN $FLAG > $DIR/cap$NN.resumo.txt 2>&1
  python3 -I rec/t17/prever.py $NN $FLAG > $DIR/cap$NN.prever.txt 2>&1
  rm -f /home/claude/ecoflix/rec/t17/_ens/t17-cap$NN.mp4 2>/dev/null
  [ "$MODO" = "c" ] && rm -f /home/claude/ecoflix/rec/t17/t17-cap$NN.mp4 2>/dev/null
  SEMALVO=$(grep -c 'SEM ALVO' "$OUT" 2>/dev/null); DIF=$(grep -c 'DIFERENTE' $DIR/cap$NN.resumo.txt 2>/dev/null)
  echo "cap$NN:$MODO rc=$RC semalvo=$SEMALVO diferente=$DIF $(grep -m1 -iE 'falh|passos' $DIR/cap$NN.resumo.txt | cut -c1-200)" >> $SAIDA
  if [ "$RC" = "4" ] || [ "$RC" = "3" ]; then echo "PARADA em cap$NN (rc=$RC): relançar daqui" >> $SAIDA; break; fi
done
echo "== fim $NOME $(date '+%H:%M') ==" >> $SAIDA
FAKE_PORT=54317 bash rec/run.sh down > /dev/null 2>&1
