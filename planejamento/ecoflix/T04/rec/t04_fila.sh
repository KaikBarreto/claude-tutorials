#!/usr/bin/env bash
# T04 · fila de ensaios na ordem dada, uma trava por item (dentro do t04_ensaio.sh). Itens: NNr (rápido), NNs (rápido que grava a semente
# apos-capNN) ou NNc (completo). Item feito (0 passo falho) ganha a marca rec/t04/_ens/feito-<item> e é pulado se a fila for
# relançada (o segundo plano morre em 2 h). Uso: bash rec/t04/t04_fila.sh 9r 7r 7c ...   Não editar enquanto roda: copie para outro nome.
cd "$(dirname "$0")/../.."
for it in "$@"; do
  M=rec/t04/_ens/feito-$it
  [ -f "$M" ] && { echo "##### $it já feito"; continue; }
  n=$((10#${it%[rcs]})); NN=$(printf '%02d' "$n")
  if [ "${it: -1}" != c ]; then MODO=rapido; DIR=rec/t04/_ens; else MODO=completo; DIR=rec/t04; fi
  SEM=""; [ "${it: -1}" = s ] && SEM=--semente
  echo "##### $it $(date +%H:%M:%S)"
  touch "rec/t04/_ens/.inicio-$it"
  bash rec/t04/t04_ensaio.sh "$n" "$MODO" $SEM
  F=$(python3 -c "import json;a=json.load(open('$DIR/t04-cap$NN.actions.json'))['actions'];print(sum(1 for x in a if x.get('error') or x.get('ok') is False))" 2>/dev/null)
  if [ "$F" = 0 ] && [ "$DIR/t04-cap$NN.actions.json" -nt "rec/t04/_ens/.inicio-$it" ]; then
    touch "$M"; echo "##### $it ok"
  else
    echo "##### $it FALHOU (falhos=$F)"
    [ -n "$SEM" ] && { echo "##### PAROU: semente do cap$NN não saiu"; break; }
  fi
done
echo "##### fim $(date +%H:%M:%S)"
