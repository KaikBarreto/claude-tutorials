#!/bin/bash
# T10 · lote de ensaio RÁPIDO de todos os capítulos (20/11, app 1.60.18): um capítulo por vez pela fila (--prio 10), MP4 ultrafast/crf 30 só para a
# folha de contato, resumo.py --ens e prever.py gravados em rec/t10/_ens/lote_NN.txt. Não grava completo (a voz ainda é estimada).
#   bash rec/t10/t10_lote.sh 00 01 02 ...      (sem argumento: 00 a 14)
cd /home/claude/ecoflix || exit 2
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54310 TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc A-Za-z0-9)Aa1}"; export TUT_SENHA
LISTA="$*"; [ -z "$LISTA" ] && LISTA="00 01 02 03 04 05 06 07 08 09 10 11 12 13 14"
for n in $LISTA; do
  nn=$(printf %02d $((10#$n)))
  P=$(cat rec/.runtime/fake54310.pid 2>/dev/null)
  if ! tr '\0' '\n' < /proc/$P/environ 2>/dev/null | grep -qx 'FAKE_PORT=54310'; then echo "cap$nn: a instância 54310 não é a minha (pid $P)"; exit 3; fi
  python3 -I rec/t10/ensaio.py $nn >/dev/null
  export nn
  bash rec/fila.sh --prio 10 -- bash -c '
    timeout 900 node rec/record.mjs rec/t10/_ens/cap$nn.json --rapido --preset ultrafast --crf 30 > rec/t10/.cap$nn.ens.out 2>&1
    echo "##### cap$nn RÁPIDO exit $? ($(date +%H:%M:%S))"
    python3 -I rec/t10/resumo.py $nn --ens > rec/t10/.cap$nn.ens.resumo 2>&1; cat rec/t10/.cap$nn.ens.resumo
    echo "SEM ALVO: $(grep -c "SEM ALVO" rec/t10/.cap$nn.ens.out)"
    python3 -I rec/t10/prever.py $nn --ens > rec/t10/.cap$nn.prever 2>&1; grep -E "ATRASO|maior atraso" rec/t10/.cap$nn.prever | head -5
  ' > rec/t10/_ens/lote_$nn.txt 2>&1
  rm -f rec/t10/_ens/t10-cap$nn.mp4
done
echo "LOTE FIM $(date +%H:%M:%S)" > rec/t10/_ens/lote_fim.txt
