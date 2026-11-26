#!/bin/bash
# T01 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 1). Qualidade padrão do record.mjs.
# Uso: bash rec/t01/t01_final.sh 00 01 ...   (VEZES=1 por padrão: cada chamada é UMA rodada; a regravação é decidida à mão)
# Saída: rec/t01/capNN.final.resumo e rec/t01/final.log. Molde: rec/t06/t06_final.sh. Instância 54301 religada a cada tentativa.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54301 FAKE_PORT=54301 FAKE_NOW=2026-11-10T08:30:00-03:00 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-1}
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="ReciclaVale#26"   # senha fictícia do ambiente (5 requisitos: o cap01 mostra "Senha forte"); só no ambiente
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  bash rec/fila.sh --prio 1 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      mkdir -p /dev/shm/t01_rec; rm -f rec/t01/t01-cap$NN.actions.json
      timeout 1200 node rec/record.mjs rec/t01/cap$NN.json --out /dev/shm/t01_rec > rec/t01/.cap$NN.out 2>&1
      for e in mp4 actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t01_rec/t01-cap$NN.$e ] && mv /dev/shm/t01_rec/t01-cap$NN.$e rec/t01/; done
      rm -rf /dev/shm/t01_rec/_frames
      python3 -I rec/t01/resumo.py $NN --tudo > rec/t01/cap$NN.final.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t01/cap$NN.final.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t01/cap$NN.final.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t01/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t01/cap$NN.final.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t01/final.log
done
bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t01/final.log
