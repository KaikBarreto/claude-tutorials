#!/usr/bin/env bash
# Varredura do app novo: ensaio rápido (sem MP4) de todos os capítulos de uma lista de aulas, uma aula por vez, sem agente.
# Saída: rec/varredura/tNN.txt (uma linha por capítulo). uso: bash rec/varredura/varrer.sh t00 t03 ...
set -u
cd /home/claude/ecoflix || exit 1
export TUT_USER=rafael@reciclavalemetais.example TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -d '/+=')x9"
for T in "$@"; do
  NN=${T#t}; PORTA=543$NN; OUT=rec/varredura/$T.txt; : > "$OUT"
  ATUAL=""
  for R in $(ls rec/$T/cap[0-9][0-9]*.json | sort); do
    C=$(basename "$R" .json); C=${C#cap}
    NOW=$(python3 -I -c "import json,sys,os;p='rec/$T/fake_now.json';d=json.load(open(p)) if os.path.exists(p) else {};print(d.get(sys.argv[1][:2],'2026-11-10T08:30:00-03:00') if isinstance(d,dict) else '2026-11-10T08:30:00-03:00')" "$C")
    if [ "$NOW" != "$ATUAL" ]; then
      [ -n "$ATUAL" ] && curl -s http://127.0.0.1:$PORTA/__dev/unknowns >> rec/varredura/$T.unknowns-parcial.json 2>/dev/null
      FAKE_PORT=$PORTA bash rec/run.sh down >/dev/null 2>&1
      FAKE_NOW=$NOW FAKE_PORT=$PORTA bash rec/run.sh fake >/dev/null 2>&1; ATUAL=$NOW
    fi
    python3 -I rec/$T/ensaio.py "$C" >/dev/null 2>&1 || { echo "$C SEM-ENSAIO" >> "$OUT"; continue; }
    rm -f rec/$T/_ens/$T-cap$C.actions.json
    FAKE_NOW=$NOW FAKE_URL=http://127.0.0.1:$PORTA timeout 480 node rec/record.mjs rec/$T/_ens/cap$C.json --rapido --no-encode > rec/$T/_ens/cap$C.out 2>&1
    RC=$?
    python3 -I rec/varredura/linha.py "$T" "$C" "$RC" >> "$OUT"
  done
  curl -s http://127.0.0.1:$PORTA/__dev/unknowns > rec/varredura/$T.unknowns.json 2>/dev/null
  FAKE_PORT=$PORTA bash rec/run.sh down >/dev/null 2>&1
  echo "FIM $T $(date +%T)" >> rec/varredura/andamento.log
done
