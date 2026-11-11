#!/usr/bin/env bash
# T16 · um capítulo por vez na fila justa (rec/fila.sh --prio 16; coordenador, 11/11), regra do coordenador de 11/11 18:46: o ensaio rápido COM o MP4 (folha de contato para olhar), o
# resumo e o prever.py; o completo (tempos estimados) só no mesmo embalo e só quando o capítulo pede: --completo (gesto sensível a
# espera: menu ou lista aberta com a fala andando, tela que muda sozinha, aviso que some), prever com atraso >= 0,4 s ou aviso no rápido.
# Uso: bash rec/t16/t16_lote2.sh NN [--semente] [--completo] [--so-completo]
# A senha do login é aleatória, só no ambiente deste processo (o falso aceita qualquer uma); nunca vai para arquivo.
set -u
cd "$(dirname "$0")/../.."
NN=$(printf '%02d' "$((10#$1))"); shift
SEM=0; COMP=0; SO=0
for a in "$@"; do case "$a" in --semente) SEM=1;; --completo) COMP=1;; --so-completo) SO=1; COMP=1;; esac; done
PORTA=54316
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:$PORTA TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14); export TUT_SENHA
PID=$(cat rec/.runtime/fake$PORTA.pid 2>/dev/null)
tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -qx "FAKE_PORT=$PORTA" || { echo "instância $PORTA fora do ar"; exit 3; }
tr '\0' '\n' < /proc/$PID/environ | grep -qx "FAKE_NOW=$FAKE_NOW" || { echo "instância $PORTA sem FAKE_NOW"; exit 3; }
mkdir -p rec/t16/_ens; [ -e rec/t16/_ens/assets ] || ln -s ../assets rec/t16/_ens/assets
bash /home/claude/ecoflix/rec/fila.sh --prio 16 -- bash -c '
  NN=$1; SEM=$2; COMP=$3; SO=$4
  echo "trava $(date +%T)"
  if [ "$SO" = 0 ]; then
    python3 -I rec/t16/ensaio.py "$NN" > /dev/null || exit 2
    timeout 600 node rec/record.mjs rec/t16/_ens/cap$NN.json --rapido --preset ultrafast --crf 30 > rec/t16/_ens/.t16-cap$NN.out 2>&1
    rm -f rec/t16/_ens/t16-cap$NN.mp4
    python3 -I rec/t16/resumo.py "$NN" --ens > rec/t16/_ens/t16-cap$NN.resumo.txt 2>&1
    python3 -I rec/t16/prever.py "$NN" --ens > rec/t16/_ens/t16-cap$NN.prever.txt 2>&1
    VER=$(python3 -I rec/t16/t16_veredito.py "$NN")
    echo "rapido $VER $(date +%T)"
    case "$VER" in falhos=0*) ;; *) exit 4;; esac
    if [ "$SEM" = 1 ]; then python3 -I rec/t16/t16_sementes.py captura "$((10#$NN))" --porta 54316; fi
    case "$VER" in *precisa=1*) COMP=1;; esac
  fi
  if [ "$COMP" = 1 ]; then
    timeout 900 node rec/record.mjs rec/t16/cap$NN.json --preset ultrafast --crf 30 > rec/t16/.t16-cap$NN.out 2>&1
    python3 -I rec/t16/resumo.py "$NN" > rec/t16/t16-cap$NN.resumo.txt 2>&1
    rm -f rec/t16/t16-cap$NN.mp4
    echo "completo $(head -1 rec/t16/t16-cap$NN.resumo.txt | cut -c1-140) $(date +%T)"
  fi' _ "$NN" "$SEM" "$COMP" "$SO"
echo "fim rc=$?"
