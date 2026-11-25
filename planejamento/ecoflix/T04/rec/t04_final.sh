#!/bin/bash
# T04 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 12). Qualidade padrão do record.mjs.
# Uso: bash rec/t04/t04_final.sh 00 01 ... 17   (VEZES=1 para uma tentativa só; padrão 2)
# Saída: rec/t04/capNN.resumo e rec/t04/final.log. Molde: rec/t12/t12_final.sh. Instância 54304 religada no FAKE_NOW (08:30 em todos).
# Os quadros ficam em /dev/shm/t04_rec (capítulo de 100 s gera ~1 GB de JPEG); para se o disco ficar abaixo de 600 MB.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54304 FAKE_PORT=54304 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-2}
export FAKE_NOW=2026-11-10T08:30:00-03:00
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
for C in "$@"; do
  NN="$(printf '%02d' "$((10#$C))")"; export NN
  L=$(df -m / | awk 'NR==2{print $4}'); [ "$L" -ge 600 ] || { echo "DISCO BAIXO ($L MB) antes do cap$NN" >> rec/t04/final.log; break; }
  bash rec/fila.sh --prio 12 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      mkdir -p /dev/shm/t04_rec; rm -f rec/t04/t04-cap$NN.actions.json
      timeout 900 node rec/record.mjs rec/t04/cap$NN.json --out /dev/shm/t04_rec > rec/t04/.cap$NN.out 2>&1
      for e in mp4 actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t04_rec/t04-cap$NN.$e ] && mv /dev/shm/t04_rec/t04-cap$NN.$e rec/t04/; done
      python3 -I rec/t04/resumo.py $NN --tudo > rec/t04/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t04/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t04/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t04/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t04/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t04/final.log
done
bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t04/final.log
