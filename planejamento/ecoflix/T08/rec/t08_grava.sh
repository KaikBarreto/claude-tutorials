#!/bin/bash
# T08 · ensaio de UM capítulo na instância do T08 (porta 54308), com o FAKE_NOW do capítulo (rec/t08/fake_now.json, do gerar.py).
# Os capítulos do T08 entram na fila da trava ao mesmo tempo (cada um parte da própria semente): por isso a instância é conferida e
# religada (FAKE_NOW do capítulo; handler/hook/lib novos) DENTRO da trava, logo antes de gravar. O `rec/run.sh fake` fecha os
# descritores da trava antes de subir o servidor (fecha_trava, docs/08), então o servidor não fica com ela.
# Modos: --rapido (só o ensaio rápido) · --os-dois (rápido e, com 0 passo falho, a gravação completa; se a completa sair com
# lateBy >= 0,8 s, mais uma completa) · sem modo (só a completa).
# Uso: bash rec/t08/t08_grava.sh NN [--rapido|--os-dois]   (rodar FORA de outro flock: a trava é pega aqui)
set -u
cd /home/claude/ecoflix
NN=$(printf '%02d' "$((10#$1))"); MODO=${2:-}
export NN MODO
FN=$(python3 -I -c "import json,sys;print(json.load(open('rec/t08/fake_now.json'))[sys.argv[1]])" "$NN") || exit 2
export FAKE_URL=http://127.0.0.1:54308 FAKE_NOW=$FN TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
[ "$MODO" = "--rapido" ] || [ "$MODO" = "--os-dois" ] && { python3 -I rec/t08/ensaio.py "$NN" || exit 2; }
echo "cap$NN FAKE_NOW=$FN fila $(date +%H:%M:%S)"
flock .heavy.lock bash -c '
  PIDF=rec/.runtime/fake54308.pid; PID=$(cat "$PIDF" 2>/dev/null || true); ATUAL=""; PORTA=""
  if [ -n "$PID" ] && [ -r /proc/$PID/environ ]; then
    ATUAL=$(tr "\0" "\n" < /proc/$PID/environ | grep "^FAKE_NOW=" | cut -d= -f2-)
    PORTA=$(tr "\0" "\n" < /proc/$PID/environ | grep "^FAKE_PORT=" | cut -d= -f2-)
    [ "$PORTA" != 54308 ] && rm -f /home/claude/ecoflix/rec/.runtime/fake54308.pid
  fi
  MUDOU=$(find rec/mundo/handlers rec/mundo/hooks rec/mundo/lib rec/mundo/schema.json -newer "$PIDF" 2>/dev/null | head -1)
  if [ "$ATUAL" != "$FAKE_NOW" ] || [ "$PORTA" != 54308 ] || [ -n "$MUDOU" ]; then FAKE_PORT=54308 bash rec/run.sh fake | tail -1; fi
  tr "\0" "\n" < /proc/$(cat "$PIDF")/environ | grep -q "^FAKE_PORT=54308$" || { echo "instância 54308 não é a minha"; exit 3; }
  echo "trava $(date +%H:%M:%S)"
  if [ "$MODO" = "--rapido" ] || [ "$MODO" = "--os-dois" ]; then
    node rec/record.mjs rec/t08/_ens/cap$NN.json --rapido > rec/t08/_ens/.cap$NN.out 2>&1
    python3 -I rec/t08/resumo.py $NN --ens > rec/t08/_ens/cap$NN.resumo 2>&1
    [ "$MODO" = "--rapido" ] && exit 0
    grep -q "!!ERRO" rec/t08/_ens/cap$NN.resumo && exit 4
  fi
  for vez in 1 2; do
    node rec/record.mjs rec/t08/cap$NN.json > rec/t08/.cap$NN.out 2>&1
    python3 -I rec/t08/resumo.py $NN > rec/t08/cap$NN.resumo 2>&1
    python3 -I -c "import re,sys;l=open(\"rec/t08/cap$NN.resumo\").readline();m=re.search(r\"maxLate ([0-9.]+)\",l);f=re.search(r\"falhos (\d+)\",l);sys.exit(0 if m and f and float(m.group(1))<0.8 and f.group(1)==\"0\" else 1)" && break
    [ $vez = 1 ] && echo "completa $vez: $(head -1 rec/t08/cap$NN.resumo) -> de novo"
  done
'
RC=$?
echo "fim cap$NN $(date +%H:%M:%S) exit $RC"; exit $RC
