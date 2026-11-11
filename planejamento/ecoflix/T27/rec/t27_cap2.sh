#!/usr/bin/env bash
# T27 · ensaio rápido + ensaio completo de UM capítulo sob UMA trava (o completo só roda se o rápido passou: 0 falho, 0 "SEM ALVO"):
#   bash rec/t27/t27_cap.sh NN [ambos|completo|rapido]     (TUT_USER e TUT_SENHA no ambiente; a senha nunca vai para arquivo)
# Saídas: rec/t27/_ens/capNN.out (rápido) e rec/t27/capNN.grav.out (completo), com o resumo.py; ficam actions.json e telemetry.json;
# o MP4 é apagado (disco curto) e as folhas de contato vão para /dev/shm/t27-[ens-]capNN.contact.jpg (olhar e apagar).
set -u
cd /home/claude/ecoflix
export FAKE_URL=http://127.0.0.1:54327 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:?}" "${TUT_SENHA:?}"
nn=$1; modo=${2:-ambos}
ens=rec/t27/_ens/cap$nn.out; grv=rec/t27/cap$nn.grav.out
mkdir -p rec/t27/_ens
python3 -I rec/t27/ensaio.py "$nn" > "$ens" 2>&1
exec 9>.heavy.lock
flock -w 6300 9 || { echo "TRAVA: não veio em 105 min (relançar)" | tee -a "$ens" >> "$grv"; exit 3; }
pid=$(cat rec/.runtime/fake54327.pid 2>/dev/null)
env_ok() { tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -q "^$1$"; }
if ! env_ok FAKE_PORT=54327 || ! env_ok FAKE_NOW=2026-11-10T08:30:00-03:00; then echo "INSTANCIA 54327 FORA OU FAKE_NOW ERRADO" | tee -a "$ens" > "$grv"; exit 2; fi
if [ "$modo" != completo ]; then
  timeout 600 node rec/record.mjs "rec/t27/_ens/cap$nn.json" --rapido >> "$ens" 2>&1 9>&-
  echo "### exit $?" >> "$ens"
  python3 -I rec/t27/resumo.py "$nn" --ens >> "$ens" 2>&1
  sa=$(grep -c "SEM ALVO" "rec/t27/_ens/t27-cap$nn.actions.json" 2>/dev/null || echo X)
  echo "SEM ALVO no actions.json: $sa" >> "$ens"
  rm -f "/home/claude/ecoflix/rec/t27/_ens/t27-cap$nn.mp4"
  [ -f "rec/t27/_ens/t27-cap$nn.contact.jpg" ] && mv -f "rec/t27/_ens/t27-cap$nn.contact.jpg" "/dev/shm/t27-ens-cap$nn.contact.jpg"
  falhos=$(grep -oE "falhos [0-9]+" "$ens" | tail -1 | awk '{print $2}')
  [ "$modo" = rapido ] && { echo "cap$nn rápido pronto"; exit 0; }
  if [ "${falhos:-X}" != 0 ] || [ "$sa" != 0 ]; then echo "rápido não passou (falhos ${falhos:-?}, SEM ALVO $sa): sem o completo" > "$grv"; exit 1; fi
fi
timeout 600 node rec/record.mjs "rec/t27/cap$nn.json" > "$grv" 2>&1 9>&-
echo "### exit $?" >> "$grv"
python3 -I rec/t27/resumo.py "$nn" >> "$grv" 2>&1
grep -c "SEM ALVO" "rec/t27/t27-cap$nn.actions.json" 2>/dev/null | sed 's/^/SEM ALVO no actions.json: /' >> "$grv"
rm -f "/home/claude/ecoflix/rec/t27/t27-cap$nn.mp4"
[ -f "rec/t27/t27-cap$nn.contact.jpg" ] && mv -f "rec/t27/t27-cap$nn.contact.jpg" "/dev/shm/t27-cap$nn.contact.jpg"
echo "cap$nn pronto"
