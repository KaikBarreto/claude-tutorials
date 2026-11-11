#!/usr/bin/env bash
# T27 · ensaio RÁPIDO (sem os `at`) de cada capítulo pedido, UMA trava por capítulo:
#   bash rec/t27/t27_ens.sh 00 01 ...     (TUT_USER e TUT_SENHA no ambiente; a senha nunca vai para arquivo)
# Saída de cada capítulo em rec/t27/_ens/capNN.out (gravação + resumo + "SEM ALVO"); o MP4 do ensaio é apagado (disco curto),
# a folha de contato fica em /dev/shm/t27-ens-capNN.contact.jpg para olhar e apagar.
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54327 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:?}" "${TUT_SENHA:?}"
for nn in "$@"; do
  out=rec/t27/_ens/cap$nn.out
  mkdir -p rec/t27/_ens
  python3 -I rec/t27/ensaio.py "$nn" > "$out" 2>&1
  # a instância é minha? (docs/04: conferir antes de cada gravação)
  pid=$(cat rec/.runtime/fake54327.pid 2>/dev/null)
  if ! tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -q '^FAKE_PORT=54327$'; then echo "INSTANCIA 54327 FORA" >> "$out"; continue; fi
  flock .heavy.lock timeout 600 node rec/record.mjs "rec/t27/_ens/cap$nn.json" --rapido >> "$out" 2>&1   # prazo só da gravação, não da fila
  echo "### exit $?" >> "$out"
  python3 -I rec/t27/resumo.py "$nn" --ens >> "$out" 2>&1
  grep -c "SEM ALVO" "rec/t27/_ens/t27-cap$nn.actions.json" 2>/dev/null | sed 's/^/SEM ALVO no actions.json: /' >> "$out"
  rm -f "/home/claude/ecoflix/rec/t27/_ens/t27-cap$nn.mp4"
  [ -f "rec/t27/_ens/t27-cap$nn.contact.jpg" ] && mv -f "rec/t27/_ens/t27-cap$nn.contact.jpg" "/dev/shm/t27-ens-cap$nn.contact.jpg"
  echo "cap$nn pronto"
done
