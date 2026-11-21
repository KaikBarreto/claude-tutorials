#!/bin/bash
# T06 · gravação FINAL (com a voz real) de uma lista de capítulos, um por vez, pela fila (prio 06). Qualidade padrão do record.mjs.
# Uso: bash rec/t06/t06_final.sh 00 01 ... 09b ... 13a ...   (VEZES=1 para uma tentativa só; padrão 2)
# Saída: rec/t06/capNN.resumo e rec/t06/final.log. Molde: rec/t03/t03_final.sh. Instância 54306 religada no FAKE_NOW do capítulo.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54306 FAKE_PORT=54306 TUT_USER=rafael@reciclavalemetais.example VEZES=${VEZES:-2}
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
for C in "$@"; do
  S=""; case "$C" in *a|*b) S="${C: -1}"; C="${C%[ab]}";; esac
  N=$((10#$C)); NN="$(printf '%02d' "$N")$S"; export NN
  case "$N" in
    0|1) NOW=08:30:00 ;; 2) NOW=08:30:55 ;; 3|4|5) NOW=08:41:50 ;; 6) NOW=08:43:30 ;; 7|8|9|10) NOW=08:45:00 ;;
    11) NOW=08:55:00 ;; 12) NOW=17:30:00 ;; 13) NOW=17:40:00 ;; 14) NOW=17:42:40 ;; *) NOW=17:44:00 ;;
  esac
  export FAKE_NOW=2026-11-10T$NOW-03:00
  bash rec/fila.sh --prio 06 -- bash -c '
    for vez in $(seq 1 $VEZES); do
      bash rec/run.sh fake | tail -1
      mkdir -p /dev/shm/t06_rec; rm -f rec/t06/t06-cap$NN.actions.json
      timeout 900 node rec/record.mjs rec/t06/cap$NN.json --out /dev/shm/t06_rec > rec/t06/.cap$NN.out 2>&1   # quadros na memória: o cap13 (162 s) encheu o disco
      for e in mp4 actions.json telemetry.json contact.jpg; do [ -f /dev/shm/t06_rec/t06-cap$NN.$e ] && mv /dev/shm/t06_rec/t06-cap$NN.$e rec/t06/; done
      python3 -I rec/t06/resumo.py $NN --tudo > rec/t06/cap$NN.resumo 2>&1
      python3 -I -c "import re,sys;l=open(\"rec/t06/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    done'
  echo "cap$NN $(date +%H:%M:%S) $(head -1 rec/t06/cap$NN.resumo) | SEM ALVO $(grep -c "SEM ALVO" rec/t06/.cap$NN.out) DIFERENTE $(grep -c DIFERENTE rec/t06/cap$NN.resumo) | livre $(df -m / | awk "NR==2{print \$4}") MB" >> rec/t06/final.log
done
bash rec/run.sh down >/dev/null 2>&1
echo fim >> rec/t06/final.log
