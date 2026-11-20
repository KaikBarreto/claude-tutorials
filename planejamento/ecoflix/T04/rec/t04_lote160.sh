#!/usr/bin/env bash
# T04 · lote de ensaio rápido dos 18 capítulos (1.60.18), em sequência pela fila (--prio 04). Captura cada semente logo depois do capítulo
# que a produz (só com 0 passo falho). Uso: bash rec/t04/t04_lote160.sh [caps...]   (sem argumento: 0..17). Resultado: rec/t04/_ens/lote160.txt
cd "$(dirname "$0")/../.."
CAPS=${*:-0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17}
OUT=rec/t04/_ens/lote160.txt
mkdir -p rec/t04/_ens
: > $OUT
for n in $CAPS; do
  NN=$(printf '%02d' "$n")
  echo "=== cap$NN $(date +%H:%M:%S)" >> $OUT
  bash rec/t04/t04_ensaio.sh $NN rapido > rec/t04/_ens/lote-cap$NN.log 2>&1
  tail -3 rec/t04/_ens/lote-cap$NN.log >> $OUT
  python3 -I rec/t04/prever.py $NN --ens > rec/t04/_ens/t04-cap$NN.prever.txt 2>&1
  if grep -q "rc=0 falhos=0$" rec/t04/_ens/lote-cap$NN.log; then
    case $n in
      2|4) python3 -I rec/t04/t04_sementes.py captura $n --porta 54304 >> $OUT 2>&1 ;;
      7) python3 -I rec/t04/t04_sementes.py captura $n --porta 54304 --nome apos-cap05 >> $OUT 2>&1 ;;
      12) python3 -I rec/t04/t04_sementes.py captura $n --porta 54304 --nome apos-cap09 >> $OUT 2>&1 ;;
      5) python3 -I rec/t04/t04_sementes.py captura $n --porta 54304 --nome apos-n1 >> $OUT 2>&1 ;;
      8) python3 -I rec/t04/t04_sementes.py captura $n --porta 54304 --nome apos-cap06 --sem entity_custom_prices >> $OUT 2>&1 ;;
    esac
  else
    echo "  (falhou: sem captura de semente)" >> $OUT
  fi
done
echo "=== FIM $(date +%H:%M:%S)" >> $OUT
