#!/usr/bin/env bash
# T15 · capítulos pedidos, NA ORDEM, uma trava por capítulo (o rodar.sh pega e solta a trava de cada um: flock + nice -n 10).
#   ensaio --rapido:  rec/t15/lote.sh 0 1 2 ... 9 9b 10 11 12   (5, 6, 7, 8, 9 e 9b gravam a semente do seguinte, apos-capNN); resumo em rec/t15/_debug/ens-NN.log
#   gravação (G):     rec/t15/lote.sh --gravar 0 1 2 3 4 5 6 7 8 9 9b 10, depois (falso em 12/11 08:30) rec/t15/lote.sh --gravar 11 12
#                     sem --seed (as sementes apos-capNN de 05/11 valem); resumo em rec/t15/_debug/rec-NN.log
cd /home/claude/domiflix
mkdir -p rec/t15/_debug
GRAVAR=""
if [ "${1:-}" = "--gravar" ]; then GRAVAR=1; shift; fi
for n in "$@"; do
  case "$n" in *b) NN="$(printf '%02d' "$((10#${n%b}))")b" ;; *) NN=$(printf '%02d' "$((10#$n))") ;; esac
  if [ -n "$GRAVAR" ]; then
    LOG=rec/t15/_debug/rec-$NN.log
    echo "início $(date +%T)" > "$LOG"
    rec/t15/rodar.sh "$NN" >> "$LOG" 2>&1
    rc=$?
  else
    LOG=rec/t15/_debug/ens-$NN.log
    S=""
    case "$NN" in 05|06|07|08|09|09b) S="--seed" ;; esac
    rec/t15/rodar.sh "$NN" --rapido $S > "$LOG" 2>&1
    rc=$?
  fi
  curl -s http://127.0.0.1:54336/__dev/unknowns | head -c 600 >> "$LOG"
  printf '\nfim %s rc=%s %s\n' "$NN" "$rc" "$(date +%T)" >> "$LOG"
  case "$rc" in 3|4|5) echo "parado no $NN (rc=$rc): veja $LOG"; exit "$rc" ;; esac   # disco, falso ou app: não segue o lote
done
