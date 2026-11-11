#!/usr/bin/env bash
# T06 · ensaio ou gravação de UM capítulo na instância do T06 (porta 54306), com o FAKE_NOW do capítulo (08:30 nos caps 0 a 9 e no 8b,
# 17:40 nos caps 10 a 12). Uso: bash rec/t06/t06_rodar.sh NN|8b [--ens]
#   --ens: ensaio rápido (ensaio.py + --rapido + resumo.py --ens); sem ele, gravação completa (+ resumo.py).
# A instância sobe FORA da trava (lição 82/140); só o robô roda sob `flock` (uma trava por capítulo). TUT_USER/TUT_SENHA vêm do ambiente.
set -euo pipefail
cd "$(dirname "$0")/../.."          # $TUT_HOME
CAP="$1"; MODO="${2:-}"
PORTA=54306
N="${CAP%b}"; N=$((10#$N))
if [ "$N" -ge 10 ]; then NOW=2026-11-10T17:40:00-03:00; else NOW=2026-11-10T08:30:00-03:00; fi
NN=$(printf '%02d' "$N"); [ "${CAP: -1}" = b ] && NN="${NN}b"
PIDF=rec/.runtime/fake${PORTA}.pid
atual=""
if [ -f "$PIDF" ] && [ -r "/proc/$(cat "$PIDF")/environ" ]; then
  atual=$(tr '\0' '\n' < "/proc/$(cat "$PIDF")/environ" | sed -n 's/^FAKE_NOW=//p')
  porta=$(tr '\0' '\n' < "/proc/$(cat "$PIDF")/environ" | sed -n 's/^FAKE_PORT=//p')
  [ "$porta" = "$PORTA" ] || atual=""
fi
if [ "$atual" != "$NOW" ]; then
  echo "== instância $PORTA com FAKE_NOW=$NOW (era: ${atual:-nenhuma})"
  FAKE_NOW=$NOW FAKE_PORT=$PORTA bash rec/run.sh fake 9>&- | tail -1
fi
export FAKE_URL=http://127.0.0.1:$PORTA FAKE_NOW=$NOW
: "${TUT_USER:?defina TUT_USER}"; : "${TUT_SENHA:?defina TUT_SENHA}"
python3 -I rec/t06/gerar.py "$CAP" >/dev/null
if [ "$MODO" = "--ens" ]; then
  python3 -I rec/t06/ensaio.py "$CAP"
  flock .heavy.lock node rec/record.mjs "rec/t06/_ens/cap$NN.json" --rapido > "rec/t06/_ens/.cap$NN.out" 2>&1 || echo "robô saiu com erro $?"
  python3 -I rec/t06/resumo.py "$CAP" --ens --tudo > "rec/t06/_ens/cap$NN.resumo.txt" 2>&1 || true
  grep -c "SEM ALVO" "rec/t06/_ens/.cap$NN.out" | sed 's/^/SEM ALVO: /' || true
  head -3 "rec/t06/_ens/cap$NN.resumo.txt"
else
  flock .heavy.lock node rec/record.mjs "rec/t06/cap$NN.json" > "rec/t06/.cap$NN.out" 2>&1 || echo "robô saiu com erro $?"
  python3 -I rec/t06/resumo.py "$CAP" > "rec/t06/cap$NN.resumo.txt" 2>&1 || true
  grep -c "SEM ALVO" "rec/t06/.cap$NN.out" | sed 's/^/SEM ALVO: /' || true
  head -3 "rec/t06/cap$NN.resumo.txt"
fi
curl -s "$FAKE_URL/__dev/unknowns" | head -c 600; echo
