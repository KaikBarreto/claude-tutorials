#!/usr/bin/env bash
# Fila justa da trava pesada. O flock acorda quem espera em ordem quase aleatória: com 100 tarefas na fila (EcoFlix,
# 11/11), uma tarefa esperava mais de 2 h sem nunca ser a escolhida e morria no prazo. Aqui cada tarefa tira uma senha e
# espera a vez dela: a fila anda pela hora de chegada mais 3 min por nível de prioridade (use o número da aula: a T01 passa
# à frente da T15 que chegou até 42 min antes, mas ninguém espera mais de ~80 min a mais por causa da prioridade; com a
# prioridade pura, a T00 e a T01, que voltam à fila logo depois de cada tarefa, deixavam as outras paradas). Na vez, pega
# a trava de verdade (o mesmo flock de quem ainda chama o flock direto), a senha sai e o comando roda. Senha de tarefa que
# morreu sai sozinha.
# uso: bash rec/fila.sh [--prio NN] [--trava ARQ] -- comando arg...     (padrão: prioridade 50, $TUT_HOME/.heavy.lock)
#      bash rec/fila.sh --ver                                            (a fila agora, na ordem em que vai andar)
set -u
TUT_HOME=${TUT_HOME:-/home/claude/ecoflix}
D="$TUT_HOME/.fila"
PRIO=50
TRAVA="$TUT_HOME/.heavy.lock"
vivas() {   # senhas de tarefa viva, na ordem da fila; apaga as de tarefa morta
  local s pid
  for s in $(ls -1 "$D" 2>/dev/null | sort); do
    pid=${s##*-}
    if kill -0 "$pid" 2>/dev/null; then echo "$s"; else rm -f "$D/$s"; fi
  done
}
while [ $# -gt 0 ]; do
  case "$1" in
    --prio) PRIO=$2; shift 2 ;;
    --trava) TRAVA=$2; shift 2 ;;
    --ver) for s in $(vivas); do printf '%s  %s\n' "$s" "$(head -c 160 "$D/$s")"; done; exit 0 ;;
    --) shift; break ;;
    *) break ;;
  esac
done
[ $# -gt 0 ] || { echo "uso: bash rec/fila.sh [--prio NN] -- comando ..." >&2; exit 2; }
mkdir -p "$D"
# "50-" deixa na frente as senhas do formato antigo (NN-hora-pid, prioridade pura) até elas acabarem
SENHA="50-$(printf '%020d' "$(( $(date +%s%N) + 10#$PRIO * 180000000000 ))")-$$"
printf '%s\n' "$*" > "$D/$SENHA"
trap 'rm -f "$D/$SENHA"' EXIT
trap 'rm -f "$D/$SENHA"; exit 143' INT TERM
# Só a primeira senha tenta a trava, e sem bloquear (flock -n): se chegar alguém de prioridade maior enquanto a trava está
# ocupada, ele passa a ser o primeiro e esta senha volta a esperar. Na vez, a senha sai quando a trava é pega.
while :; do
  if [ "$(vivas | head -n 1)" = "$SENHA" ]; then
    flock -n -E 222 "$TRAVA" bash -c 'rm -f "$1"; shift; exec "$@"' _ "$D/$SENHA" "$@"
    rc=$?
    [ "$rc" -ne 222 ] && exit "$rc"
  fi
  sleep 1
done
