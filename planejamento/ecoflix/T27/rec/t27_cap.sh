#!/usr/bin/env bash
# T27 · ensaio de UM capítulo pela fila da trava pesada (rec/fila.sh, prioridade 27; uma tarefa por vez na fila):
#   bash rec/t27/t27_cap.sh NN [rapido|ambos|completo]     (TUT_USER e TUT_SENHA no ambiente; a senha nunca vai para arquivo)
# rapido = só o ensaio rápido (sem os `at`); ambos = rápido e, se ele passou (0 falho, 0 "SEM ALVO"), o completo com os tempos da voz
# estimada; completo = só o completo. MP4 de ensaio em ultrafast/crf 30 (só para a folha de contato) e apagado logo depois.
# Saídas: rec/t27/_ens/capNN.out (rápido) e rec/t27/capNN.grav.out (completo), com o resumo.py; ficam actions.json e telemetry.json;
# as folhas de contato vão para /dev/shm/t27-[ens-]capNN.contact.jpg (olhar e apagar).
set -u
cd /home/claude/ecoflix
if [ "${T27_NA_TRAVA:-}" != 1 ]; then
  exec bash rec/fila.sh --prio 27 -- env T27_NA_TRAVA=1 bash rec/t27/t27_cap.sh "$@"
fi
export FAKE_URL=http://127.0.0.1:54327 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:?}" "${TUT_SENHA:?}"
nn=$1; modo=${2:-rapido}
ens=rec/t27/_ens/cap$nn.out; grv=rec/t27/cap$nn.grav.out
ENC=(--preset ultrafast --crf 30)
# "SEM ALVO" no VALOR devolvido por um `eval` (o actions.json guarda também o começo do js, que traz o texto 'SEM ALVO' do próprio teste)
semalvo() { python3 -I -c "import json,sys; a=json.load(open(sys.argv[1]))['actions']; print(sum(1 for x in a if x.get('do')=='eval' and 'SEM ALVO' in json.dumps(x.get('value'), ensure_ascii=False)))" "$1" 2>/dev/null || echo X; }
mkdir -p rec/t27/_ens
pid=$(cat rec/.runtime/fake54327.pid 2>/dev/null)
env_ok() { tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -q "^$1$"; }
if ! env_ok FAKE_PORT=54327 || ! env_ok FAKE_NOW=2026-11-10T08:30:00-03:00; then echo "INSTANCIA 54327 FORA OU FAKE_NOW ERRADO" | tee "$ens" > "$grv"; exit 2; fi
if [ "$modo" != completo ]; then
  python3 -I rec/t27/ensaio.py "$nn" > "$ens" 2>&1
  timeout 600 node rec/record.mjs "rec/t27/_ens/cap$nn.json" --rapido "${ENC[@]}" >> "$ens" 2>&1
  echo "### exit $?" >> "$ens"
  python3 -I rec/t27/resumo.py "$nn" --ens >> "$ens" 2>&1
  sa=$(semalvo "rec/t27/_ens/t27-cap$nn.actions.json")
  echo "SEM ALVO no actions.json: $sa" >> "$ens"
  rm -f "/home/claude/ecoflix/rec/t27/_ens/t27-cap$nn.mp4"
  [ -f "rec/t27/_ens/t27-cap$nn.contact.jpg" ] && mv -f "rec/t27/_ens/t27-cap$nn.contact.jpg" "/dev/shm/t27-ens-cap$nn.contact.jpg"
  falhos=$(grep -oE "falhos [0-9]+" "$ens" | tail -1 | awk '{print $2}')
  [ "$modo" = rapido ] && { echo "cap$nn rápido pronto"; exit 0; }
  if [ "${falhos:-X}" != 0 ] || [ "$sa" != 0 ]; then echo "rápido não passou (falhos ${falhos:-?}, SEM ALVO $sa): sem o completo" > "$grv"; exit 1; fi
fi
timeout 600 node rec/record.mjs "rec/t27/cap$nn.json" "${ENC[@]}" > "$grv" 2>&1
echo "### exit $?" >> "$grv"
python3 -I rec/t27/resumo.py "$nn" >> "$grv" 2>&1
echo "SEM ALVO no actions.json: $(semalvo "rec/t27/t27-cap$nn.actions.json")" >> "$grv"
rm -f "/home/claude/ecoflix/rec/t27/t27-cap$nn.mp4"
[ -f "rec/t27/t27-cap$nn.contact.jpg" ] && mv -f "rec/t27/t27-cap$nn.contact.jpg" "/dev/shm/t27-cap$nn.contact.jpg"
echo "cap$nn pronto"
