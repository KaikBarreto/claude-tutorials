#!/usr/bin/env bash
# T04 · lote de ensaios RÁPIDOS na ordem da cadeia (uma trava por capítulo, dentro do t04_ensaio.sh). Uso: bash rec/t04/t04_lote.sh [NN ...]
# Para quando um capítulo que grava semente (2, 4, 5, 6, 9) não fecha com 0 falho: os seguintes partiriam de uma semente velha.
# Não editar enquanto roda (o bash lê o script aos poucos): copie para outro nome.
cd "$(dirname "$0")/../.."
CAPS=${*:-"0 1 2 3 4 5 6 7 8 9 10 11 12 13"}
for n in $CAPS; do
  NN=$(printf '%02d' "$n")
  SEM=""; case " 2 4 5 6 9 " in *" $n "*) SEM=--semente;; esac
  echo "##### cap$NN $(date +%H:%M:%S)"
  bash rec/t04/t04_ensaio.sh "$n" rapido $SEM
  if [ -n "$SEM" ]; then
    F=rec/mundo/seeds-extra/t04/apos-cap$NN.json
    if [ ! -f "$F" ] || [ "$F" -ot rec/t04/_ens/t04-cap$NN.actions.json ]; then echo "##### PAROU: cap$NN sem semente nova"; break; fi
  fi
done
echo "##### fim $(date +%H:%M:%S)"
