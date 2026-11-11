#!/usr/bin/env bash
# T22 · lote de ensaios, UM de cada vez na fila justa (regra de 11/11: no máximo uma tarefa minha na fila). Lê a lista
# rec/t22/_lote/lista.txt a cada volta ("<id> <args do t22_ens.sh>", uma por linha; # comenta) e roda a primeira linha que ainda não tem
# rec/t22/_lote/<id>.fim; a saída vai para rec/t22/_lote/<id>.log e uma linha "=== <id> rc=N" sai aqui (a notificação). A lista pode
# ser mexida enquanto o lote anda (pôr, tirar, reordenar); repetir um ensaio = apagar o <id>.fim. Para quando não sobra linha.
# Uso (tarefa de fundo, prazo máximo 2 h): bash rec/t22/t22_lote.sh
cd /home/claude/ecoflix || exit 1
L=rec/t22/_lote
mkdir -p $L
while :; do
  prox=""
  while read -r id args; do
    case "$id" in ''|\#*) continue ;; esac
    [ -f "$L/$id.fim" ] && continue
    prox="$id"; pargs="$args"; break
  done < $L/lista.txt
  [ -z "$prox" ] && { echo "=== lote vazio $(date +%H:%M)"; exit 0; }
  echo "--- $prox ($pargs) entra na fila $(date +%H:%M:%S)"
  bash rec/t22/t22_ens.sh $pargs > "$L/$prox.log" 2>&1
  rc=$?
  echo "$rc $(date +%H:%M:%S)" > "$L/$prox.fim"
  echo "=== $prox rc=$rc $(date +%H:%M:%S): $(grep -m1 -o 'falhos [0-9]*, atrasos>=0.3: [0-9]*, maxLate [0-9.]*' "$L/$prox.log")"
done
