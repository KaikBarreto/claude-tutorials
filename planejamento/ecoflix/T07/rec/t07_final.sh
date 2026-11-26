#!/bin/bash
# T07 · gravação FINAL (com a voz real 1.60.22) de uma lista de capítulos, um por vez, pela fila (prio 07). Qualidade padrão do record.mjs.
# Uso: bash rec/t07/t07_final.sh 00 01 ...   (VEZES=1 para uma tentativa só; padrão 2)
# Quadros em /dev/shm/t07_rec (o disco é curto); depois move mp4, actions, telemetria, folha e impressões para rec/t07/.
# Saída: rec/t07/capNN.resumo e rec/t07/final.log. Molde: rec/t06/t06_final.sh. Instância 54307 religada a cada tentativa.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54307 FAKE_PORT=54307 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-2}
export FAKE_NOW=2026-11-10T08:35:00-03:00
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
for C in "$@"; do
  NN=$(printf '%02d' "$((10#$C))"); export NN
  bash rec/fila.sh --prio 07 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      mkdir -p /dev/shm/t07_rec /dev/shm/t07_velho; mv -f rec/t07/t07-cap$NN.actions.json /dev/shm/t07_velho/ 2>/dev/null; mv -f /dev/shm/t07_rec/t07-cap$NN.* /dev/shm/t07_velho/ 2>/dev/null
      timeout 900 node rec/record.mjs rec/t07/cap$NN.json --out /dev/shm/t07_rec > rec/t07/.cap$NN.out 2>&1
      for e in mp4 actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t07_rec/t07-cap$NN.$e ] && mv /dev/shm/t07_rec/t07-cap$NN.$e rec/t07/; done
      [ -d /dev/shm/t07_rec/t07-cap$NN.impressoes ] && cp -rf /dev/shm/t07_rec/t07-cap$NN.impressoes rec/t07/
      python3 -I rec/t07/resumo.py $NN --tudo > rec/t07/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t07/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t07/cap$NN.resumo | cut -c1-200) | SEM ALVO $(grep -c "SEM ALVO" rec/t07/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t07/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t07/final.log
done
FAKE_PORT=54307 bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t07/final.log
