#!/usr/bin/env bash
# T27 · ensaio COMPLETO (com os `at` da voz estimada) de cada capítulo pedido, UMA trava por capítulo:
#   bash rec/t27/t27_grav.sh 00 01 ...     (TUT_USER e TUT_SENHA no ambiente; a senha nunca vai para arquivo)
# Antes: python3 -I rec/t27/gerar.py e python3 -I rec/t27/prever.py NN --ens. Saída de cada capítulo em rec/t27/capNN.grav.out
# (gravação + resumo + "SEM ALVO"); fica o actions.json e o telemetry.json; o MP4 é apagado (disco curto) e a folha de contato vai
# para /dev/shm/t27-capNN.contact.jpg (olhar e apagar).
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54327 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:?}" "${TUT_SENHA:?}"
for nn in "$@"; do
  out=rec/t27/cap$nn.grav.out
  pid=$(cat rec/.runtime/fake54327.pid 2>/dev/null)
  if ! tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -q '^FAKE_PORT=54327$'; then echo "INSTANCIA 54327 FORA" > "$out"; continue; fi
  if ! tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -q '^FAKE_NOW=2026-11-10T08:30:00-03:00$'; then echo "FAKE_NOW ERRADO" > "$out"; continue; fi
  flock .heavy.lock timeout 600 node rec/record.mjs "rec/t27/cap$nn.json" > "$out" 2>&1   # prazo só da gravação, não da fila
  echo "### exit $?" >> "$out"
  python3 -I rec/t27/resumo.py "$nn" >> "$out" 2>&1
  grep -c "SEM ALVO" "rec/t27/t27-cap$nn.actions.json" 2>/dev/null | sed 's/^/SEM ALVO no actions.json: /' >> "$out"
  rm -f "/home/claude/ecoflix/rec/t27/t27-cap$nn.mp4"
  [ -f "rec/t27/t27-cap$nn.contact.jpg" ] && mv -f "rec/t27/t27-cap$nn.contact.jpg" "/dev/shm/t27-cap$nn.contact.jpg"
  echo "cap$nn pronto"
done
