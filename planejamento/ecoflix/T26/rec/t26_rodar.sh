#!/usr/bin/env bash
# T26 · ensaio e/ou gravação de UM capítulo na instância própria (54326), sob a trava pesada (uma trava por capítulo), e a semente
# do estado final para o capítulo seguinte.
#   bash rec/t26/t26_rodar.sh NN --ens      ensaio rápido (ensaio.py: sem os `at`) -> rec/t26/_ens/t26-capNN.*
#   bash rec/t26/t26_rodar.sh NN            gravação com os `at` (ensaio completo / gravação final) -> rec/t26/t26-capNN.*
#   bash rec/t26/t26_rodar.sh NN --ambos    os dois na MESMA trava (o completo só roda se o rápido saiu com 0 passo falho)
#   --sem-semente  não grava seeds-extra/t26/apos-capNN (padrão: grava nos capítulos de GRAVA_SEMENTE do gerar.py)
# FAKE_NOW vem do "fakeNow" do capNN.json; se a instância estiver com outro, ela é religada ANTES da trava (serviço nunca sobe dentro
# do flock). TUT_USER/TUT_SENHA: do ambiente (a senha nunca vai para arquivo; o falso aceita qualquer uma).
set -euo pipefail
TUT_HOME="${T26_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"   # T26_HOME: quando a fila roda uma cópia do script
cd "$TUT_HOME"
NN=$(printf %02d "$((10#$1))"); shift
MODO=final; SEMENTE=1
for a in "$@"; do case "$a" in --ens) MODO=ens ;; --ambos) MODO=ambos ;; --sem-semente) SEMENTE=0 ;; esac; done
PORTA=54326
export FAKE_URL="http://127.0.0.1:$PORTA"
: "${TUT_USER:?defina TUT_USER}"; : "${TUT_SENHA:?defina TUT_SENHA}"
export TUT_USER TUT_SENHA
# a junção do mundo pode mudar a fala: antes da gravação com os tempos, refaz os capNN.json estimados e o roteiro
if [ "$MODO" != ens ]; then bash /home/claude/claude-tutorials/planejamento/ecoflix/preparar_aula.sh T26 | tail -n 1; fi
python3 -I rec/t26/gerar.py "$((10#$NN))" | grep -v "^  aviso" || true
FN=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['fakeNow'])" "rec/t26/cap$NN.json")
export FAKE_NOW="$FN"
# a instância é a minha e está no FAKE_NOW do capítulo?
PID=$(cat "rec/.runtime/fake$PORTA.pid" 2>/dev/null || true)
ATUAL=""
if [ -n "$PID" ] && [ -r "/proc/$PID/environ" ]; then
  ATUAL=$(tr '\0' '\n' < "/proc/$PID/environ" | sed -n 's/^FAKE_NOW=//p')
  tr '\0' '\n' < "/proc/$PID/environ" | grep -qx "FAKE_PORT=$PORTA" || ATUAL="(outra)"
fi
if [ "$ATUAL" != "$FN" ]; then
  echo "== religando a instância $PORTA com FAKE_NOW=$FN (estava: ${ATUAL:-parada})"
  FAKE_NOW="$FN" FAKE_PORT=$PORTA bash rec/run.sh fake
fi
GRAVA=$(python3 -c "import runpy,sys;g=runpy.run_path('rec/t26/gerar.py');print(1 if int(sys.argv[1]) in g['GRAVA_SEMENTE'] else 0)" "$((10#$NN))")
[ "$SEMENTE" = 1 ] || GRAVA=0
[ "$MODO" = final ] || python3 -I rec/t26/ensaio.py "$((10#$NN))"
echo "== $(date +%H:%M:%S) cap$NN ($MODO) esperando a trava..."
# fila justa da trava pesada (rec/fila.sh, prioridade 26 = o número da aula; no máximo UMA tarefa da T26 na fila)
bash rec/fila.sh --prio 26 -- bash -c '
  set -e
  NN=$1; MODO=$2; GRAVA=$3
  grava() {  # $1 roteiro, $2 log
    # MP4 de ensaio: só para a folha de contato (x264 ultrafast, crf 30)
    node rec/record.mjs "$1" --preset ultrafast --crf 30 > "$2" 2>&1 || { echo "FALHOU $1 (log: $2)"; grep -E "FALHOU|Error" "$2" | tail -n 3; return 1; }
    grep -E "^\s+mp4|\"durationS\"" "$2" | head -n 1 || true
  }
  echo "== $(date +%H:%M:%S) trava ok (cap$NN $MODO)"
  if [ "$MODO" != final ]; then
    grava "rec/t26/_ens/cap$NN.json" "rec/t26/.cap$NN.ens.out"   # com o MP4: a folha de contato do rápido é obrigatória (_BRIEF_ROBO item 3, 11/11 18:46)
    [ "$GRAVA" = 1 ] && node rec/t26/aux/t26_semente.mjs "apos-cap$NN"
  fi
  if [ "$MODO" != ens ]; then
    grava "rec/t26/cap$NN.json" "rec/t26/.cap$NN.final.out"
    [ "$GRAVA" = 1 ] && node rec/t26/aux/t26_semente.mjs "apos-cap$NN"
  fi
  echo "== $(date +%H:%M:%S) solta a trava (cap$NN)"
' _ "$NN" "$MODO" "$GRAVA"
echo "== $(date +%H:%M:%S) cap$NN ($MODO) pronto"
