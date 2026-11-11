#!/usr/bin/env bash
# T22 · fila dos ensaios (supervisor; roda solto com setsid, sem o limite de 2 h das tarefas de fundo). A cada 20 s, para cada capítulo:
#   rápido: se rec/t22/_fila/rapNN existe, o log rec/t22/_fila/rapNN.log ainda não tem "=== capNN" (nem o do lote antigo,
#           rec/t22/_ens/rN.log) e o ticket que esta fila pôs não está vivo, põe um ticket na trava
#           (t22_ens.sh NN --se-faltar [--estado nos caps 9 a 11]);
#   completo: o mesmo com rec/t22/_fila/comNN e rec/t22/_fila/comNN.log (t22_ens.sh NN --completo --se-faltar).
# Pré-requisitos: os caps 10 e 11 entram na fila já; dentro da trava, sem a semente apos-cap09 / apos-cap10, o ticket sai na hora
# (FALTA-SEMENTE) e a fila põe outro no fim. No máximo T22_MAX (11)
# tickets desta fila vivos ao mesmo tempo. --se-faltar: um ticket reserva cujo ensaio já passou só atravessa a trava (0,1 s).
# Pedir um ensaio = `touch rec/t22/_fila/rapNN` (ou comNN); repetir = apagar o log e o ok-MODO-NN (rm com caminho absoluto).
# Parar = rm rec/t22/_fila/LIGADA (ou kill do PID em rec/t22/_fila/supervisor.pid). Cada ticket é um processo próprio esperando a trava.
cd /home/claude/ecoflix || exit 1
F=rec/t22/_fila
SEM=rec/mundo/seeds-extra/t22
mkdir -p $F
echo $$ > $F/supervisor.pid
touch $F/LIGADA
vivo() { local p; p=$(cat $F/pid-$1 2>/dev/null) || return 1; [ -n "$p" ] && kill -0 "$p" 2>/dev/null; }
pronto() { true; }   # o t22_ens.sh confere as sementes DENTRO da trava (FALTA-SEMENTE: sai na hora e a fila põe outro ticket)
nvivos() { local k=0 f; for f in $F/pid-*; do [ -f "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && k=$((k+1)); done; echo $k; }
while [ -f $F/LIGADA ]; do
  for nn in 00 01 02 03 04 05 06 07 08 09 10 11; do
    n=$((10#$nn))
    for modo in rap com; do
      [ -f $F/$modo$nn ] || continue
      grep -q "=== cap$nn " $F/$modo$nn.log 2>/dev/null && continue
      grep -q "^FALTA-SEMENTE" $F/$modo$nn.log 2>/dev/null && { kill -0 "$(cat $F/pid-$modo$nn 2>/dev/null)" 2>/dev/null || mv -f $F/$modo$nn.log $F/$modo$nn.falta.log; continue; }
      [ $modo = rap ] && grep -q "=== cap$nn (rapido) rc=0" rec/t22/_ens/r$n.log 2>/dev/null && continue   # o lote antigo também vale
      vivo $modo$nn && continue
      pronto $nn || continue
      [ "$(nvivos)" -ge "${T22_MAX:-11}" ] && continue
      if [ $modo = rap ]; then extra="--se-faltar"; [ $n -ge 9 ] && extra="--se-faltar --estado"; else extra="--completo --se-faltar"; fi
      setsid bash rec/t22/t22_ens.sh $n $extra > $F/$modo$nn.log 2>&1 < /dev/null &
      echo $! > $F/pid-$modo$nn
      echo "$(date +%T) ticket cap$nn $modo $extra (pid $!)" >> $F/supervisor.log
      sleep 1
    done
  done
  sleep 20
done
echo "$(date +%T) supervisor parou" >> $F/supervisor.log
