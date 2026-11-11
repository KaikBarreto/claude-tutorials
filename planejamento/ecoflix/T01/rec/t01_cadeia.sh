#!/usr/bin/env bash
# Ensaios COMPLETOS do T1 em sequência, um capítulo por trava, dentro do prazo de uma tarefa em segundo plano (2 h): cada
# capítulo espera a trava só o que sobra do prazo menos 15 min para gravar; sem trava no prazo, para e diz o que falta.
# Uso: TUT_USER=... TUT_SENHA=... [T01_MODO=rapido] bash rec/t01/t01_cadeia.sh 02 03 ...   (a senha só no ambiente)
# T01_MODO=rapido: ensaio rápido COM o MP4 (folha de contato em /dev/shm/t01_rec/_ens); o padrão é o completo.
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1   # $TUT_HOME
INI=$(date +%s); PRAZO=${T01_PRAZO:-7000}
while [ $# -gt 0 ]; do
  n=$1
  rest=$(( PRAZO - ($(date +%s) - INI) - 900 ))
  if [ "$rest" -lt 60 ]; then echo "PAUSA (prazo): faltam $*"; break; fi
  echo "== cap$n $(date +%T) (espera a trava até ${rest} s)"
  T01_ESPERA=$rest bash rec/t01/t01_ens.sh "${T01_MODO:-completo}" "$n" > /dev/null 2>&1
  if [ $? = 75 ]; then echo "SEM TRAVA no prazo: faltam $*"; break; fi
  d=rec/t01; [ "${T01_MODO:-completo}" = rapido ] && d=rec/t01/_ens
  r=$d/cap$n.resumo.txt
  echo "RES cap$n | $(tail -1 $d/cap$n.log) | $(tail -1 $d/cap$n.prever.txt 2>/dev/null | sed 's/.*maior atraso/maior atraso/') | $(head -1 "$r") | $(sed -n 2p "$r" | tr -s ' ') | $(grep -h 'conferências' "$r") | $(grep -h '^SEM ALVO' "$r") | avisos: $(grep -h 'avisos de erro na tela' "$r" | sed 's/.*=> //')"
  shift
done
echo "CADEIA FIM $(date +%T)"
