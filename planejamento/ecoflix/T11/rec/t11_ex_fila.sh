#!/usr/bin/env bash
# T11: roda explorações em fila, cada uma sob a própria trava (uma por vez; os outros agentes entram entre elas).
#   bash rec/t11/t11_ex_fila.sh e3 e4 e5
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54311
for e in "$@"; do
  case "$e" in e4|e5|e6|e7) export FAKE_NOW=2026-11-10T17:30:00-03:00 ;; *) export FAKE_NOW=2026-11-10T08:30:00-03:00 ;; esac
  flock .heavy.lock timeout 600 node rec/t11/explorar.mjs rec/t11/_ex/$e.json --out /dev/shm/t11ex > rec/t11/_ex/$e.out 2>&1
  echo "fim $e $?" >> rec/t11/_ex/$e.out
done
